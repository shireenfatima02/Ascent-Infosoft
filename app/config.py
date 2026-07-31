import os
from pathlib import Path


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-secret")

    # Database (PostgreSQL required)
    _db_url = os.environ.get("DATABASE_URL")
    if not _db_url:
        raise RuntimeError(
            "DATABASE_URL is required and must be a PostgreSQL DSN (e.g., postgresql+psycopg://user:pass@host:port/dbname)."
        )
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploads
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 120 * 1024 * 1024))
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")  # default: instance/uploads
    # Only allow archive uploads
    ALLOWED_EXTENSIONS = {"zip", "rar"}

    # Email
    SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))
    SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
    # Comma-separated recipient list; defaults to SMTP_USERNAME
    SMTP_TO = os.environ.get("SMTP_TO", "")
    SMTP_USE_SSL = True

    # Data path for static JSON
    DATA_PATH = os.environ.get("DATA_PATH")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False


def get_config(name: str | None = None):
    name = (name or os.environ.get("FLASK_ENV", "production")).lower()
    if name in ("dev", "development"):
        return DevelopmentConfig
    if name in ("test", "testing"):
        return TestingConfig
    return ProductionConfig
