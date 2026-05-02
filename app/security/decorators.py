from functools import wraps
from flask import abort
from flask_login import current_user, login_required


def roles_required(*roles):
    roles_set = {r.upper() for r in roles}

    def decorator(view):
        @wraps(view)
        @login_required
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            # Admin bypasses checks
            if getattr(current_user, "is_admin", False):
                return view(*args, **kwargs)
            if (current_user.role or "").upper() in roles_set:
                return view(*args, **kwargs)
            abort(403)

        return wrapped

    return decorator

