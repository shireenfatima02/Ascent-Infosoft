import os
from pathlib import Path
from uuid import uuid4
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename: str) -> bool:
    allowed = current_app.config.get("ALLOWED_EXTENSIONS", set())
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in allowed


def _uploads_base() -> Path:
    base = current_app.config.get("UPLOAD_FOLDER")
    if base:
        return Path(base)
    return Path(current_app.instance_path) / "uploads"


def _deleted_base() -> Path:
    return Path(current_app.instance_path) / "deleted"


def org_upload_dir(org_id: int) -> Path:
    d = _uploads_base() / str(org_id)
    d.mkdir(parents=True, exist_ok=True)
    return d


def org_deleted_dir(org_id: int) -> Path:
    d = _deleted_base() / str(org_id)
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_upload(file_storage, org_id: int) -> tuple[str, int, str]:
    filename = secure_filename(file_storage.filename or "")
    if not filename or not allowed_file(filename):
        raise ValueError("File type not allowed")
    ext = "." + filename.rsplit(".", 1)[1].lower() if "." in filename else ""
    stored_name = f"{uuid4().hex}{ext}"
    dest_dir = org_upload_dir(org_id)
    dest_path = dest_dir / stored_name
    file_storage.save(str(dest_path))
    size = dest_path.stat().st_size
    mime = file_storage.mimetype or ""
    return stored_name, size, mime


def file_path(org_id: int, stored_name: str, deleted: bool = False) -> Path:
    base = org_deleted_dir(org_id) if deleted else org_upload_dir(org_id)
    return base / stored_name


def soft_delete_file(org_id: int, stored_name: str):
    src = file_path(org_id, stored_name, deleted=False)
    dst_dir = org_deleted_dir(org_id)
    dst = dst_dir / stored_name
    if src.exists():
        dst_dir.mkdir(parents=True, exist_ok=True)
        src.replace(dst)


def restore_file(org_id: int, stored_name: str):
    src = file_path(org_id, stored_name, deleted=True)
    dst_dir = org_upload_dir(org_id)
    dst = dst_dir / stored_name
    if src.exists():
        dst_dir.mkdir(parents=True, exist_ok=True)
        src.replace(dst)
