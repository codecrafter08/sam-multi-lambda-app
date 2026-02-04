import os

from db_models import Base

from alembic.config import Config
from alembic import command

def run_migrations(db_url):
    alembic_cfg = Config('alembic.ini')
    alembic_cfg.set_main_option('sqlalchemy.url', db_url)
    command.upgrade(alembic_cfg, 'head')

def lambda_handler(event, context):
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    try:
        print("--> running migrations")
        run_migrations(DATABASE_URL)
        print("--> migration complete")

    except Exception as e:
        print("Error while migrating: ", e)

    return "Script complete"
