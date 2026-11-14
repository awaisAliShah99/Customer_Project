"""Functions for loading raw source data."""

from pathlib import Path

import pandas as pd

from src.config import RAW_DATA_PATH

REQUIRED_COLUMNS = [
    "customer_id", "first_name", "last_name", "email", "phone", "city",
    "customer_segment", "order_id", "order_date", "product_category",
    "product_name", "quantity", "unit_price_pkr", "total_amount_pkr",
    "payment_method", "order_status",
]


def load_raw_data(file_path: Path | str | None = None) -> pd.DataFrame:
    """Load the raw customer CSV and return it as a DataFrame."""
    path = Path(file_path) if file_path is not None else RAW_DATA_PATH

    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found: {path}")

    try:
        data = pd.read_csv(path, encoding="utf-8-sig")  # utf-8-sig: BOM hata deta hai
    except (pd.errors.EmptyDataError, pd.errors.ParserError) as error:
        raise ValueError(f"Raw data file is empty or not a valid CSV: {path}") from error

    if data.empty:
        raise ValueError(f"Raw data file has no records: {path}")

    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        raise ValueError(f"Raw data is missing required columns: {missing}")

    return data