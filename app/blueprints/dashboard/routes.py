from flask import render_template, request, redirect, url_for, abort, send_from_directory, flash
from flask_login import login_required, current_user

from . import bp
from ...extensions import db
from ...models.file import File
from ...services import storage


@bp.route("/files", methods=["GET"], endpoint="files")
@login_required
def files_list():
    q = File.query
    if not current_user.is_admin:
        q = q.filter_by(org_id=current_user.org_id, is_deleted=False)
    files = q.order_by(File.created_at.desc()).all()
    return render_template("dashboard/files.html", files=files)


@bp.route("/upload", methods=["POST"])
@login_required
def upload_file():
    f = request.files.get("file")
    if not f:
        flash("No file uploaded", "error")
        return redirect(url_for("dashboard.files"))
    try:
        org_id = current_user.org_id
        stored_name, size, mime = storage.save_upload(f, org_id)
        rec = File(
            org_id=org_id,
            uploader_id=current_user.id,
            original_name=f.filename,
            stored_name=stored_name,
            size=size,
            mime=mime,
        )
        db.session.add(rec)
        db.session.commit()
        flash("File uploaded", "success")
    except ValueError as ve:
        db.session.rollback()
        flash(str(ve) or "Only .zip or .rar files are allowed.", "error")
    except Exception as e:  # pragma: no cover
        db.session.rollback()
        flash("Upload failed", "error")
    return redirect(url_for("dashboard.files"))


@bp.route("/files/<int:file_id>/download")
@login_required
def download_file(file_id: int):
    rec = File.query.get_or_404(file_id)
    if not current_user.is_admin and (rec.org_id != current_user.org_id or rec.is_deleted):
        abort(404)
    directory = str(storage.org_upload_dir(rec.org_id))
    return send_from_directory(directory, rec.stored_name, as_attachment=True, download_name=rec.original_name)
