"""Tests for raw-data ingestion."""

import pandas as pd
import pytest

from src.ingestion.load_data import REQUIRED_COLUMNS, load_raw_data


def write_csv(path, rows: int = 2) -> None:
    data = {column: [f"{column}{i}" for i in range(rows)] for column in REQUIRED_COLUMNS}
    pd.DataFrame(data).to_csv(path, index=False)


def test_successful_loading(tmp_path) -> None:
    path = tmp_path / "data.csv"
    write_csv(path, rows=3)
    data = load_raw_data(path)
    assert len(data) == 3
    assert list(data.columns) == REQUIRED_COLUMNS


def test_default_raw_file_loads() -> None:
    data = load_raw_data()
    assert len(data) == 1000
    assert "customer_id" in data.columns  # BOM ki wajah se naam kharab nahi hona chahiye


def test_missing_file_raises(tmp_path) -> None:
    with pytest.raises(FileNotFoundError):
        load_raw_data(tmp_path / "does_not_exist.csv")


def test_empty_file_raises(tmp_path) -> None:
    path = tmp_path / "empty.csv"
    path.write_text("")
    with pytest.raises(ValueError):
        load_raw_data(path)


def test_file_without_records_raises(tmp_path) -> None:
    path = tmp_path / "header_only.csv"
    path.write_text(",".join(REQUIRED_COLUMNS) + "\n")
    with pytest.raises(ValueError):
        load_raw_data(path)


def test_missing_required_columns_raises(tmp_path) -> None:
    path = tmp_path / "bad.csv"
    pd.DataFrame({"customer_id": ["C1"], "city": ["Lahore"]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="missing required columns"):
        load_raw_data(path)