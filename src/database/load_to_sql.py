"""Functions for loading validated data into SQL."""

import pandas as pd
from sqlalchemy.engine import Connection

from src.config import SQL_TABLE_NAME


def load_clean_data_to_sql(
    validated_data: pd.DataFrame,
    connection: Connection,
    table_name: str = SQL_TABLE_NAME,
) -> None:
    """Store validated records in the configured SQL table."""
    # TODO: Load validated_data into the table without embedding credentials.
    pass
