"""Orchestrate the customer data engineering pipeline."""

import pandas as pd

from src.analytics.queries import prepare_analytical_queries
from src.config import CLEAN_DATA_PATH
from src.database.connection import get_database_connection
from src.database.load_to_sql import load_clean_data_to_sql, load_validation_summary
from src.ingestion.load_data import load_raw_data
from src.transformations.clean_data import transform_data
from src.validation.validate_data import validate_data


def build_validation_summary(raw_count: int, summary: dict) -> pd.DataFrame:
    """Turn the validation counts into a small table (outcome, records)."""
    return pd.DataFrame(
        {
            "outcome": ["duplicate_removed", "accepted", "corrected", "rejected"],
            "records": [
                raw_count - summary["total"],
                summary["accepted"],
                summary["corrected"],
                summary["rejected"],
            ],
        }
    )


def run_pipeline() -> None:
    """Run ingestion, transformation, validation, file output, and SQL loading."""
    raw_data = load_raw_data()
    transformed_data = transform_data(raw_data)
    validated_data = validate_data(transformed_data)

    CLEAN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    validated_data.to_csv(CLEAN_DATA_PATH, index=False)

    summary = build_validation_summary(len(raw_data), validated_data.attrs["summary"])

    with get_database_connection() as connection:
        load_clean_data_to_sql(validated_data, connection)
        load_validation_summary(summary, connection)

    prepare_analytical_queries()
    print(f"Raw records: {len(raw_data)}")
    print(summary.to_string(index=False))
    print(f"Cleaned CSV saved to: {CLEAN_DATA_PATH}")
    print("Pipeline complete.")


if __name__ == "__main__":
    run_pipeline()