"""Functions for loading validated data into SQL."""

import pandas as pd
from sqlalchemy.engine import Connection
from sqlalchemy.types import String

from src.config import SQL_TABLE_NAME

SUMMARY_TABLE_NAME = "validation_summary"


def load_clean_data_to_sql(
    validated_data: pd.DataFrame,
    connection: Connection,
    table_name: str = SQL_TABLE_NAME,
) -> None:
    """Store validated records in the configured SQL table."""
    if validated_data is None or validated_data.empty:
        raise ValueError("No validated records to load.")

    validated_data.to_sql(
        table_name,
        connection,
        if_exists="replace",  # dobara run karne par duplicate rows nahi banti
        index=False,
        dtype={"customer_id": String(20), "order_id": String(20)},
    )
    connection.commit()


def load_validation_summary(summary: pd.DataFrame, connection: Connection) -> None:
    """Store accepted/corrected/rejected counts for the Q9 analytical query."""
    summary.to_sql(SUMMARY_TABLE_NAME, connection, if_exists="replace", index=False)
    connection.commit()