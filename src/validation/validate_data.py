"""Functions for validating transformed customer data."""

import pandas as pd

MAX_QUANTITY = 10            # data mein normal quantity 1-5 hai; 999 outlier hai
MAX_UNIT_PRICE = 500_000     # normal price ~525-84,747; 9,999,999 outlier hai
AMOUNT_TOLERANCE = 0.01      # paisa-level rounding ka farq
FILL_COLUMNS = ["city", "customer_segment", "product_category"]


def _recover_missing_amounts(df: pd.DataFrame) -> pd.Series:
    """Missing quantity/price ko total se nikalo (jahan mumkin ho). Corrected rows ka mask return."""
    recovered = pd.Series(False, index=df.index)

    # quantity = total / price (sirf tab jab whole number bane)
    guess = (df["total_amount_pkr"] / df["unit_price_pkr"]).round()
    can_qty = (
        df["quantity"].isna()
        & df["unit_price_pkr"].gt(0)
        & df["total_amount_pkr"].gt(0)
        & ((df["total_amount_pkr"] / df["unit_price_pkr"] - guess).abs() < AMOUNT_TOLERANCE)
    )
    df.loc[can_qty, "quantity"] = guess[can_qty]
    recovered |= can_qty

    # price = total / quantity
    can_price = (
        df["unit_price_pkr"].isna()
        & df["quantity"].gt(0)
        & df["total_amount_pkr"].gt(0)
    )
    df.loc[can_price, "unit_price_pkr"] = (
        df.loc[can_price, "total_amount_pkr"] / df.loc[can_price, "quantity"]
    ).round(2)
    recovered |= can_price
    return recovered


def validate_records(transformed_data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (kept_records, rejected_records). Kept rows carry validation_status."""
    df = transformed_data.copy()
    corrected = _recover_missing_amounts(df)

    # --- Reject: jin records ko theek karna mumkin ya safe nahi ---
    rules = [
        ("missing_order_date", df["order_date"].isna()),
        ("missing_quantity", df["quantity"].isna()),
        ("non_positive_quantity", df["quantity"].le(0)),
        ("quantity_outlier", df["quantity"].gt(MAX_QUANTITY)),
        ("missing_unit_price", df["unit_price_pkr"].isna()),
        ("non_positive_unit_price", df["unit_price_pkr"].le(0)),
        ("unit_price_outlier", df["unit_price_pkr"].gt(MAX_UNIT_PRICE)),
    ]
    reason = pd.Series(pd.NA, index=df.index, dtype="object")
    for name, mask in rules:
        reason = reason.mask(reason.isna() & mask, name)

    rejected = df[reason.notna()].copy()
    rejected["rejection_reason"] = reason[reason.notna()]

    kept = df[reason.isna()].copy()
    corrected = corrected[kept.index]

    # --- Correct: total ko quantity x price se dobara nikalo ---
    expected_total = (kept["quantity"] * kept["unit_price_pkr"]).round(2)
    bad_total = kept["total_amount_pkr"].isna() | (
        (kept["total_amount_pkr"] - expected_total).abs() > AMOUNT_TOLERANCE
    )
    kept.loc[bad_total, "total_amount_pkr"] = expected_total[bad_total]
    corrected |= bad_total

    # --- Correct: missing city/segment/category ko "Unknown" likho ---
    for column in FILL_COLUMNS:
        missing = kept[column].isna()
        kept[column] = kept[column].fillna("Unknown")
        corrected |= missing

    kept["validation_status"] = corrected.map({True: "corrected", False: "accepted"})
    return kept.reset_index(drop=True), rejected.reset_index(drop=True)


def validate_data(transformed_data: pd.DataFrame) -> pd.DataFrame:
    """Validate transformed records and return accepted + corrected records."""
    kept, rejected = validate_records(transformed_data)
    counts = kept["validation_status"].value_counts()
    kept.attrs["summary"] = {
        "total": len(transformed_data),
        "accepted": int(counts.get("accepted", 0)),
        "corrected": int(counts.get("corrected", 0)),
        "rejected": len(rejected),
    }
    return kept