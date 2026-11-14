"""Tests for database integration."""

import pandas as pd
import pytest
from sqlalchemy import text

from src.database.connection import build_database_url, get_database_connection
from src.database.load_to_sql import (
    SUMMARY_TABLE_NAME,
    load_clean_data_to_sql,
    load_validation_summary,
)

SETTINGS = {
    "DB_HOST": "db-container",
    "DB_PORT": "3306",
    "DB_NAME": "customer_db",
    "DB_USER": "tester",
    "DB_PASSWORD": "secret",
}


@pytest.fixture
def connection():
    """Har test ko khali in-memory SQLite database milta hai (MySQL ki zaroorat nahi)."""
    conn = get_database_connection("sqlite:///:memory:")
    yield conn
    conn.close()


def sample_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "customer_id": ["CUST1", "CUST2"],
            "order_id": ["ORD1", "ORD2"],
            "city": ["Lahore", pd.NA],
            "order_date": pd.to_datetime(["2024-01-02", "2024-02-03"]),
            "total_amount_pkr": [200.0, 450.5],
        }
    )


def test_database_url_is_built_from_environment(monkeypatch) -> None:
    for name, value in SETTINGS.items():
        monkeypatch.setenv(name, value)
    url = build_database_url()
    assert url.host == "db-container"  # localhost nahi, container ka naam
    assert url.port == 3306
    assert url.database == "customer_db"
    assert url.username == "tester"
    assert url.drivername == "mysql+pymysql"


def test_missing_environment_settings_raise(monkeypatch) -> None:
    for name in SETTINGS:
        monkeypatch.setenv(name, "")
    with pytest.raises(ValueError, match="DB_HOST"):
        build_database_url()


def test_database_connection(connection) -> None:
    assert connection.execute(text("SELECT 1")).scalar() == 1


def test_sql_loading_behavior(connection) -> None:
    load_clean_data_to_sql(sample_data(), connection)
    rows = connection.execute(text("SELECT COUNT(*) FROM customer_orders")).scalar()
    total = connection.execute(text("SELECT SUM(total_amount_pkr) FROM customer_orders")).scalar()
    nulls = connection.execute(text("SELECT COUNT(*) FROM customer_orders WHERE city IS NULL")).scalar()
    assert rows == 2
    assert total == pytest.approx(650.5)
    assert nulls == 1


def test_loading_twice_does_not_duplicate_rows(connection) -> None:
    load_clean_data_to_sql(sample_data(), connection)
    load_clean_data_to_sql(sample_data(), connection)
    assert connection.execute(text("SELECT COUNT(*) FROM customer_orders")).scalar() == 2


def test_loading_empty_data_raises(connection) -> None:
    with pytest.raises(ValueError):
        load_clean_data_to_sql(sample_data().iloc[0:0], connection)


def test_validation_summary_is_loaded(connection) -> None:
    summary = pd.DataFrame({"outcome": ["accepted", "rejected"], "records": [10, 2]})
    load_validation_summary(summary, connection)
    rows = connection.execute(text(f"SELECT outcome, records FROM {SUMMARY_TABLE_NAME}")).fetchall()
    assert dict(rows) == {"accepted": 10, "rejected": 2}