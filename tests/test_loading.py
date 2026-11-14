
"""Tests for raw-data ingestion."""

import pandas as pd
import pytest

from src.ingestion.load_data import load_raw_data


def test_successful_loading(tmp_path):
    """Verify that a valid CSV loads successfully."""

    csv_file = tmp_path / "customers.csv"

    sample_data = pd.DataFrame({
        "customer_id": ["CUST001", "CUST002"],
        "city": ["Peshawar", "Karachi"]
    })

    sample_data.to_csv(csv_file, index=False)

    result = load_raw_data(csv_file)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert list(result.columns) == ["customer_id", "city"]


def test_missing_or_invalid_input(tmp_path):
    """Verify that missing input raises an error."""

    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_raw_data(missing_file)

    with pytest.raises(FileNotFoundError):
        load_raw_data(tmp_path)
