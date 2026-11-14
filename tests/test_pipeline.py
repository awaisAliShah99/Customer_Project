"""End-to-end test of the pipeline (SQLite use hota hai, MySQL nahi)."""

import pandas as pd
from sqlalchemy import text

import src.pipeline as pipeline
from src.database.connection import get_database_connection


def test_pipeline_saves_csv_and_loads_tables(tmp_path, monkeypatch) -> None:
    clean_path = tmp_path / "cleaned_customers.csv"
    monkeypatch.setattr(pipeline, "CLEAN_DATA_PATH", clean_path)
    monkeypatch.setattr(
        pipeline, "get_database_connection", lambda: get_database_connection(f"sqlite:///{tmp_path / 't.db'}")
    )

    pipeline.run_pipeline()

    saved = pd.read_csv(clean_path)
    assert len(saved) == 946  # 829 accepted + 117 corrected
    assert set(saved["validation_status"]) == {"accepted", "corrected"}

    conn = get_database_connection(f"sqlite:///{tmp_path / 't.db'}")
    assert conn.execute(text("SELECT COUNT(*) FROM customer_orders")).scalar() == 946
    summary = dict(conn.execute(text("SELECT outcome, records FROM validation_summary")).fetchall())
    assert summary == {"duplicate_removed": 20, "accepted": 829, "corrected": 117, "rejected": 34}
    conn.close()