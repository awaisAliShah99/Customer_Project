"""Orchestrate the customer data engineering pipeline."""

from src.analytics.queries import prepare_analytical_queries
from src.config import CLEAN_DATA_PATH
from src.database.connection import get_database_connection
from src.database.load_to_sql import load_clean_data_to_sql
from src.ingestion.load_data import load_raw_data
from src.transformations.clean_data import transform_data
from src.validation.validate_data import validate_data


def run_pipeline() -> None:
    """Run ingestion, transformation, validation, file output, and SQL loading."""
    raw_data = load_raw_data()
    transformed_data = transform_data(raw_data)
    validated_data = validate_data(transformed_data)

    # TODO: Save validated_data to CLEAN_DATA_PATH after implementing validation.
    _ = CLEAN_DATA_PATH

    connection = get_database_connection()
    load_clean_data_to_sql(validated_data, connection)
    prepare_analytical_queries()
    print("Pipeline orchestration complete. Implement the TODO sections before running.")


if __name__ == "__main__":
    run_pipeline()
