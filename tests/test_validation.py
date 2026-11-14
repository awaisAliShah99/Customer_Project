"""Tests for student-defined validation."""

import pandas as pd

from src.validation.validate_data import validate_data, validate_records


def make_row(**overrides) -> dict:
    """Ek valid, transformed row; zaroorat ki cheez override karo."""
    row = {
        "order_id": "ORD00001",
        "order_date": pd.Timestamp("2024-10-12"),
        "city": "Lahore",
        "customer_segment": "Regular",
        "product_category": "Books",
        "quantity": 2.0,
        "unit_price_pkr": 100.0,
        "total_amount_pkr": 200.0,
    }
    row.update(overrides)
    return row


def split(*rows: dict):
    return validate_records(pd.DataFrame(list(rows)))


def test_valid_record_is_accepted() -> None:
    kept, rejected = split(make_row())
    assert len(kept) == 1 and rejected.empty
    assert kept.loc[0, "validation_status"] == "accepted"


def test_wrong_total_is_corrected() -> None:
    kept, _ = split(make_row(total_amount_pkr=99_999_999.0))
    assert kept.loc[0, "total_amount_pkr"] == 200.0
    assert kept.loc[0, "validation_status"] == "corrected"


def test_missing_total_is_corrected() -> None:
    kept, _ = split(make_row(total_amount_pkr=float("nan")))
    assert kept.loc[0, "total_amount_pkr"] == 200.0
    assert kept.loc[0, "validation_status"] == "corrected"


def test_missing_quantity_is_recovered_from_total() -> None:
    kept, _ = split(make_row(quantity=float("nan")))
    assert kept.loc[0, "quantity"] == 2.0
    assert kept.loc[0, "validation_status"] == "corrected"


def test_missing_price_is_recovered_from_total() -> None:
    kept, _ = split(make_row(unit_price_pkr=float("nan")))
    assert kept.loc[0, "unit_price_pkr"] == 100.0
    assert kept.loc[0, "validation_status"] == "corrected"


def test_missing_category_fields_are_filled_with_unknown() -> None:
    kept, _ = split(make_row(city=pd.NA, customer_segment=pd.NA, product_category=pd.NA))
    assert kept.loc[0, "city"] == "Unknown"
    assert kept.loc[0, "customer_segment"] == "Unknown"
    assert kept.loc[0, "product_category"] == "Unknown"
    assert kept.loc[0, "validation_status"] == "corrected"


def test_invalid_records_are_rejected_with_reason() -> None:
    kept, rejected = split(
        make_row(order_id="A", quantity=-2.0, total_amount_pkr=-200.0),
        make_row(order_id="B", quantity=0.0, total_amount_pkr=0.0),
        make_row(order_id="C", quantity=999.0, total_amount_pkr=99_900.0),
        make_row(order_id="D", unit_price_pkr=9_999_999.0),
        make_row(order_id="E", unit_price_pkr=-500.0),
        make_row(order_id="F", order_date=pd.NaT),
        make_row(order_id="G", quantity=float("nan"), total_amount_pkr=float("nan")),
    )
    assert kept.empty
    reasons = dict(zip(rejected["order_id"], rejected["rejection_reason"]))
    assert reasons == {
        "A": "non_positive_quantity",
        "B": "non_positive_quantity",
        "C": "quantity_outlier",
        "D": "unit_price_outlier",
        "E": "non_positive_unit_price",
        "F": "missing_order_date",
        "G": "missing_quantity",
    }


def test_validate_data_returns_kept_rows_and_summary_counts() -> None:
    raw = pd.DataFrame(
        [
            make_row(order_id="OK"),
            make_row(order_id="FIX", total_amount_pkr=1.0),
            make_row(order_id="BAD", quantity=-1.0),
        ]
    )
    result = validate_data(raw)
    assert list(result["order_id"]) == ["OK", "FIX"]
    assert result.attrs["summary"] == {"total": 3, "accepted": 1, "corrected": 1, "rejected": 1}