from datetime import datetime
from flask import render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user

from . import bp
from ...extensions import db
from ...models.organization import Organization
from ...models.user import User
from ...models.file import File
from ...security.decorators import roles_required
from ...services import storage


@bp.before_request
def ensure_admin():
    # Protect all routes under /admin
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)


@bp.route("/", endpoint="index")
def admin_index():
    orgs = Organization.query.order_by(Organization.name.asc()).all()
    files_count = File.query.count()
    users_count = User.query.count()
    return render_template("admin/index.html", orgs=orgs, files_count=files_count, users_count=users_count)


@bp.route("/organizations", endpoint="organizations")
def organizations_list():
    orgs = Organization.query.order_by(Organization.name.asc()).all()
    return render_template("admin/organizations.html", orgs=orgs)


@bp.route("/organizations/create", methods=["POST"])
def create_organization():
    def _back():
        return redirect(request.referrer or url_for("admin.index"))

    name = (request.form.get("name") or "").strip()
    slug_in = (request.form.get("slug") or "").strip()
    username = (request.form.get("username") or "").strip().lower()
    password = request.form.get("password") or ""

    if not name:
        flash("Organization abbreviation is required", "error")
        return _back()
    if not slug_in:
        flash("Organization name is required", "error")
        return _back()
    if not username:
        flash("Username is required", "error")
        return _back()
    if not password:
        flash("Password is required", "error")
        return _back()
    if Organization.query.filter(Organization.name == name).first():
        flash("Organization already exists", "error")
        return _back()
    if Organization.query.filter(Organization.slug == slug_in).first():
        flash("Organization name already exists", "error")
        return _back()
    if User.query.filter_by(email=username).first():
        flash("This username already exists", "error")
        return _back()
    try:
        org = Organization(name=name, slug=slug_in)
        db.session.add(org)
        db.session.flush()  # get org.id without committing

        user = User(org_id=org.id, email=username, role="USER", active=True)
        user.set_password(password)
        db.session.add(user)

        db.session.commit()
        flash("Organization and user created", "success")
        return redirect(url_for("admin.index"))
    except Exception:  # pragma: no cover
        db.session.rollback()
        flash("Failed to create organization", "error")
        return _back()


@bp.route("/organizations/<int:org_id>/files", endpoint="org_files")
def org_files(org_id: int):
    org = Organization.query.get_or_404(org_id)
    files = File.query.filter_by(org_id=org.id).order_by(File.created_at.desc()).all()
    return render_template("admin/files.html", org=org, files=files)


@bp.route("/organizations/<int:org_id>/upload", methods=["POST"], endpoint="org_upload")
def org_upload(org_id: int):
    org = Organization.query.get_or_404(org_id)
    f = request.files.get("file")
    if not f:
        flash("No file uploaded", "error")
        return redirect(url_for("admin.org_files", org_id=org.id))
    try:
        stored_name, size, mime = storage.save_upload(f, org.id)
        rec = File(
            org_id=org.id,
            uploader_id=current_user.id,
            original_name=f.filename,
            stored_name=stored_name,
            size=size,
            mime=mime,
        )
        db.session.add(rec)
        db.session.commit()
        flash("File uploaded", "success")
    except Exception:
        db.session.rollback()
        flash("Upload failed", "error")
    return redirect(url_for("admin.org_files", org_id=org.id))


@bp.route("/files/<int:file_id>/delete", methods=["POST"], endpoint="file_delete")
def file_delete(file_id: int):
    rec = File.query.get_or_404(file_id)
    if not rec.is_deleted:
        storage.soft_delete_file(rec.org_id, rec.stored_name)
        rec.is_deleted = True
        rec.deleted_at = datetime.utcnow()
        db.session.commit()
        flash("File soft-deleted", "success")
    return redirect(url_for("admin.org_files", org_id=rec.org_id))


@bp.route("/files/<int:file_id>/restore", methods=["POST"], endpoint="file_restore")
def file_restore(file_id: int):
    rec = File.query.get_or_404(file_id)
    if rec.is_deleted:
        storage.restore_file(rec.org_id, rec.stored_name)
        rec.is_deleted = False
        rec.deleted_at = None
        db.session.commit()
        flash("File restored", "success")
    return redirect(url_for("admin.org_files", org_id=rec.org_id))
