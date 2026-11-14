"""Tests for student-defined transformations."""

import pandas as pd

from src.transformations.clean_data import transform_data


def make_row(**overrides) -> dict:
    """Ek valid order row banata hai; zaroorat ki cheez override karo."""
    row = {
        "customer_id": "CUST0001",
        "first_name": "Ali",
        "last_name": "Khan",
        "email": "ali.khan@gmail.com",
        "phone": "+923001234567",
        "city": "Lahore",
        "customer_segment": "Regular",
        "order_id": "ORD00001",
        "order_date": "2024-10-12",
        "product_category": "Books",
        "product_name": "Novel",
        "quantity": "2",
        "unit_price_pkr": "100.5",
        "total_amount_pkr": 201.0,
        "payment_method": "Cash",
        "order_status": "Completed",
    }
    row.update(overrides)
    return row


def run(*rows: dict) -> pd.DataFrame:
    return transform_data(pd.DataFrame(list(rows)))


def test_text_columns_are_stripped_and_standardized() -> None:
    out = run(
        make_row(city=" LAHORE ", customer_segment="Vip", payment_method="Jazz cash", order_status="cancel"),
        make_row(order_id="ORD00002", city="islamabd", payment_method="CREDIT CARD", order_status="complete"),
    )
    assert out.loc[0, "city"] == "Lahore"
    assert out.loc[0, "customer_segment"] == "VIP"
    assert out.loc[0, "payment_method"] == "JazzCash"
    assert out.loc[0, "order_status"] == "Cancelled"
    assert out.loc[1, "city"] == "Islamabad"
    assert out.loc[1, "payment_method"] == "Credit Card"
    assert out.loc[1, "order_status"] == "Completed"


def test_blank_text_becomes_missing() -> None:
    out = run(make_row(city="   "))
    assert pd.isna(out.loc[0, "city"])


def test_invalid_numbers_become_missing_and_columns_are_numeric() -> None:
    out = run(make_row(quantity="five"), make_row(order_id="ORD00002", unit_price_pkr="unknown"))
    assert pd.isna(out.loc[0, "quantity"])
    assert pd.isna(out.loc[1, "unit_price_pkr"])
    assert pd.api.types.is_numeric_dtype(out["quantity"])
    assert pd.api.types.is_numeric_dtype(out["unit_price_pkr"])


def test_mixed_date_formats_are_parsed() -> None:
    out = run(
        make_row(order_id="ORD1", order_date="2024-10-12"),
        make_row(order_id="ORD2", order_date="29/06/2026"),
        make_row(order_id="ORD3", order_date="06-03-2024"),
        make_row(order_id="ORD4", order_date="07-19-2025"),
        make_row(order_id="ORD5", order_date="Aug 03, 2026"),
    )
    expected = pd.to_datetime(
        ["2024-10-12", "2026-06-29", "2024-03-06", "2025-07-19", "2026-08-03"]
    )
    assert list(out["order_date"]) == list(expected)


def test_invalid_dates_become_missing() -> None:
    out = run(
        make_row(order_id="ORD1", order_date="31/02/2025"),
        make_row(order_id="ORD2", order_date="not available"),
    )
    assert out["order_date"].isna().all()


def test_invalid_email_and_phone_become_missing() -> None:
    out = run(
        make_row(email="user@@gmail.com", phone="+92-abc-123"),
        make_row(order_id="ORD2", email="not_an_email", phone="123"),
    )
    assert out["email"].isna().all()
    assert out["phone"].isna().all()


def test_valid_email_and_phone_are_cleaned() -> None:
    out = run(make_row(email=" Ali.Khan@Gmail.com ", phone="03001234567"))
    assert out.loc[0, "email"] == "ali.khan@gmail.com"
    assert out.loc[0, "phone"] == "+923001234567"


def test_duplicates_are_removed() -> None:
    row = make_row()
    out = run(row, dict(row), make_row(order_id="ORD00001", product_name="Other"))
    assert len(out) == 1
    assert out["order_id"].is_unique


def test_original_dataframe_is_not_modified() -> None:
    raw = pd.DataFrame([make_row(city=" LAHORE ")])
    transform_data(raw)
    assert raw.loc[0, "city"] == " LAHORE "