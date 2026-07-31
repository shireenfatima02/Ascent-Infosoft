import os
from pathlib import Path
from flask import Flask
from flask import flash, redirect, request, url_for
from werkzeug.exceptions import RequestEntityTooLarge

# Ensure .env is loaded before importing config
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from .config import get_config
from .extensions import db, login_manager, csrf


def create_app(config_name: str | None = None) -> Flask:
    base_dir = Path(__file__).resolve().parent.parent  # repo root

    app = Flask(
        __name__,
        template_folder=str(base_dir / "templates"),
        static_folder=str(base_dir / "static"),
    )

    config_class = get_config(config_name)
    app.config.from_object(config_class)

    # Ensure instance subdirectories for storage exist
    for sub in ("uploads", "deleted"):
        target = Path(app.instance_path) / sub
        target.mkdir(parents=True, exist_ok=True)

    # Init extensions
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.client_login"
    # Ensure csrf_token() is available in templates
    try:
        from flask_wtf.csrf import generate_csrf
        app.jinja_env.globals["csrf_token"] = generate_csrf
    except Exception:
        pass

    # User loader
    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):  # pragma: no cover
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None

    # Register blueprints
    from .blueprints.auth.routes import bp as auth_bp
    from .blueprints.main.routes import bp as main_bp
    from .blueprints.dashboard.routes import bp as dashboard_bp
    from .blueprints.admin.routes import bp as admin_bp
    from .blueprints.api.routes import bp as api_bp
    from .blueprints.legacy.routes import bp as legacy_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(legacy_bp)

    # Exempt CSRF for public JSON form posts handled via fetch
    try:
        from .blueprints.main import routes as main_routes
        csrf.exempt(main_routes.contact)
        csrf.exempt(main_routes.index)
    except Exception:
        pass

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(_error):
        flash("File is too large. Maximum allowed size is 120 MB.", "error")
        referrer = request.referrer
        if referrer:
            return redirect(referrer)
        return redirect(url_for("main.index"))

    return app
