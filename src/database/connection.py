"""Database connection helpers."""

import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Connection

import src.config  # noqa: F401  (import hone par .env load ho jata hai)

REQUIRED_SETTINGS = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]


def build_database_url() -> URL:
    """Build the MySQL URL from environment variables (no secrets in code)."""
    values = {name: os.getenv(name, "") for name in REQUIRED_SETTINGS}
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise ValueError(f"Missing database settings: {', '.join(missing)}")

    return URL.create(
        drivername="mysql+pymysql",
        username=values["DB_USER"],
        password=values["DB_PASSWORD"],
        host=values["DB_HOST"],
        port=int(values["DB_PORT"]),
        database=values["DB_NAME"],
    )


def get_database_connection(url: URL | str | None = None) -> Connection:
    """Create a SQL database connection using environment configuration."""
    engine = create_engine(url if url is not None else build_database_url())
    return engine.connect()