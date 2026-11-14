"""Functions for cleaning and transforming customer data."""

import pandas as pd

# Har column ke liye: "chhota aur saaf likha hua variant" -> "sahi final naam"
CITY_MAP = {
    "islamabd": "Islamabad",
}
SEGMENT_MAP = {
    "vip": "VIP",
}
PAYMENT_MAP = {
    "easypaisa": "EasyPaisa",
    "easy paisa": "EasyPaisa",
    "jazzcash": "JazzCash",
    "jazz cash": "JazzCash",
}
STATUS_MAP = {
    "complete": "Completed",
    "cancel": "Cancelled",
    "return": "Returned",
}


def standardize_text(series: pd.Series, mapping: dict) -> pd.Series:
    """Strip spaces, fix case, and correct known spelling variants."""
    cleaned = series.astype("string").str.strip()
    cleaned = cleaned.replace("", pd.NA)          # khali text ko missing banao
    key = cleaned.str.lower()                      # compare karne ke liye
    fixed = key.map(mapping)                       # agar variant map mein hai to sahi naam
    return fixed.fillna(cleaned.str.title())       # warna Title Case


DATE_FORMATS = [
    "%Y-%m-%d",   # 2024-10-12  (standard)
    "%Y/%m/%d",   # 2025/03/12
    "%d/%m/%Y",   # 29/06/2026
    "%d-%m-%Y",   # 06-03-2024  (pehle day-first try hota hai)
    "%m-%d-%Y",   # 07-19-2025  (day-first fail ho to month-first)
    "%b %d, %Y",  # Aug 03, 2026
]


def parse_dates(series: pd.Series) -> pd.Series:
    """Convert mixed-format date text into real dates; invalid dates become NaT."""
    text = series.astype("string").str.strip()
    result = pd.Series(pd.NaT, index=text.index, dtype="datetime64[ns]")
    for fmt in DATE_FORMATS:
        still_missing = result.isna() & text.notna()
        parsed = pd.to_datetime(text[still_missing], format=fmt, errors="coerce")
        result = result.fillna(parsed)
    return result


EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
PHONE_PATTERN = r"^\+92\d{10}$"


def clean_email(series: pd.Series) -> pd.Series:
    """Lowercase and strip emails; invalid emails become missing."""
    email = series.astype("string").str.strip().str.lower()
    return email.where(email.str.match(EMAIL_PATTERN, na=False), pd.NA)


def clean_phone(series: pd.Series) -> pd.Series:
    """Convert 03XXXXXXXXX to +92XXXXXXXXXX; invalid phones become missing."""
    phone = series.astype("string").str.strip()
    local = phone.str.match(r"^03\d{9}$", na=False)
    phone = phone.where(~local, "+92" + phone.str[1:])
    return phone.where(phone.str.match(PHONE_PATTERN, na=False), pd.NA)


def transform_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform raw customer-order records."""
    df = raw_data.copy()  # original ko kabhi change nahi karte

    df["city"] = standardize_text(df["city"], CITY_MAP)
    df["customer_segment"] = standardize_text(df["customer_segment"], SEGMENT_MAP)
    df["payment_method"] = standardize_text(df["payment_method"], PAYMENT_MAP)
    df["order_status"] = standardize_text(df["order_status"], STATUS_MAP)

    # Numbers: text ('five', 'unknown') ko NaN bana do
    for column in ["quantity", "unit_price_pkr", "total_amount_pkr"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Dates: mixed formats ko ek standard date mein badlo
    df["order_date"] = parse_dates(df["order_date"])

    # Names: extra spaces hatao, Title Case
    for column in ["first_name", "last_name"]:
        df[column] = df[column].astype("string").str.strip().str.title()

    # Email aur phone: format theek karo, invalid ko missing banao
    df["email"] = clean_email(df["email"])
    df["phone"] = clean_phone(df["phone"])

    # Duplicates: pehle poori duplicate rows, phir repeated order_id
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset="order_id", keep="first")

    return df.reset_index(drop=True)