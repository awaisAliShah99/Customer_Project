"""Analytical SQL queries: har sawal ki apni .sql file reports/sql/ mein hai."""

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Connection

from src.config import PROJECT_ROOT

SQL_DIR = PROJECT_ROOT / "reports" / "sql"


def prepare_analytical_queries() -> dict[str, str]:
    """Load every q*.sql file from reports/sql as {query_name: sql_text}."""
    return {path.stem: path.read_text(encoding="utf-8") for path in sorted(SQL_DIR.glob("q*.sql"))}


def run_analytical_query(name: str, connection: Connection) -> pd.DataFrame:
    """Run one prepared query (e.g. 'q01_cities_orders_revenue') and return its result."""
    queries = prepare_analytical_queries()
    if name not in queries:
        raise KeyError(f"Unknown query: {name}")
    return pd.read_sql(text(queries[name]), connection)