import sys
from pathlib import Path
from flask import current_app
from flask.cli import with_appcontext
import click

from sqlalchemy import text
from app import create_app
from app.extensions import db
from app.models.organization import Organization
from app.models.user import User


app = create_app()


@click.group()
def cli():
    """Management commands."""


@cli.command("init-db")
@with_appcontext
def init_db():
    """Initialize database schema via SQL or ORM metadata."""
    schema_file = Path("db/schema.sql")
    if schema_file.exists():
        sql = schema_file.read_text(encoding="utf-8")
        # Split on semicolons while preserving statements (simple approach)
        for stmt in [s.strip() for s in sql.split(";") if s.strip()]:
            db.session.execute(text(stmt))
        db.session.commit()
        click.echo("Applied schema.sql")
    else:
        db.create_all()
        click.echo("Created tables via ORM metadata")

@cli.command("create-admin")
@click.option("--email", required=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@click.option("--org", "org_abbr", required=True, help="Organization abbreviation (stored in organizations.name)")
@click.option("--org-name", "org_name", required=True, help="Organization name (stored in organizations.slug)")
@with_appcontext
def create_admin(email: str, password: str, org_abbr: str, org_name: str):
    org = Organization.query.filter_by(name=org_abbr).first()
    if not org:
        if Organization.query.filter_by(slug=org_name).first() is not None:
            click.echo("Organization name already exists")
            return
        org = Organization(name=org_abbr, slug=org_name)
        db.session.add(org)
        db.session.flush()

    user = User.query.filter_by(email=email.lower()).first()
    if user:
        click.echo("User already exists")
        return
    user = User(org_id=org.id, email=email.lower(), role="ADMIN", active=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo("Admin user created")


if __name__ == "__main__":
    cli()
