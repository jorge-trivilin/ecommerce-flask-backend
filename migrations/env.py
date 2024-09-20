"""
Alembic environment configuration for Flask-SQLAlchemy.

This module sets up the Alembic environment for database migrations.
It integrates with Flask-SQLAlchemy to use the application's database configuration
and provides functions for running migrations in both online and offline modes.
"""

import logging
from logging.config import fileConfig

from flask import current_app

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# fileConfig(config.config_file_name)
if config.config_file_name:
    fileConfig(config.config_file_name)
else:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("alembic.env")
    logger.warning("Config file name is None. Using basic logging configuration.")


def get_engine():
    """
    Retrieve the SQLAlchemy engine from the Flask application.

    This function attempts to get the engine using different methods
    to support various versions of Flask-SQLAlchemy.

    Returns:
        SQLAlchemy engine instance
    """
    try:
        # this works with Flask-SQLAlchemy<3 and Alchemical
        return current_app.extensions["migrate"].db.get_engine()
    except TypeError:
        # this works with Flask-SQLAlchemy>=3
        return current_app.extensions["migrate"].db.engine


def get_engine_url():
    """
    Get the database URL from the SQLAlchemy engine.

    This function retrieves the URL as a string, handling different
    SQLAlchemy versions and escaping percent signs.

    Returns:
        str: The database URL
    """
    try:
        return get_engine().url.render_as_string(hide_password=False).replace("%", "%%")
    except AttributeError:
        return str(get_engine().url).replace("%", "%%")


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option("sqlalchemy.url", get_engine_url())
target_db = current_app.extensions["migrate"].db

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_metadata():
    """
    Retrieve the metadata from the SQLAlchemy database instance.

    This function handles different versions of Flask-SQLAlchemy
    to get the correct metadata object.

    Returns:
        MetaData: The SQLAlchemy metadata object
    """
    if hasattr(target_db, "metadatas"):
        return target_db.metadatas[None]
    return target_db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=get_metadata(), literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        """
        Prevent auto-migration when there are no changes to the schema.

        This callback is used to check if any schema changes are detected.
        If no changes are found, it clears the directives to skip the migration.

        Args:
            context: The migration context
            revision: The revision object
            directives: List of directives for the migration
        """
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No changes in schema detected.")

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            process_revision_directives=process_revision_directives,
            **current_app.extensions["migrate"].configure_args
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
