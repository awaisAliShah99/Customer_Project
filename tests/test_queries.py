"""Tests for the analytical SQL query files."""

from src.analytics.queries import prepare_analytical_queries


def test_all_ten_query_files_are_found() -> None:
    queries = prepare_analytical_queries()
    assert len(queries) == 10


def test_every_query_is_a_select_on_a_known_table() -> None:
    for name, sql in prepare_analytical_queries().items():
        body = "\n".join(line for line in sql.splitlines() if not line.strip().startswith("--"))
        assert body.strip().upper().startswith(("SELECT", "WITH")), name
        assert "customer_orders" in body or "validation_summary" in body, name
        assert not any(word in body.upper() for word in ("DROP ", "DELETE ", "UPDATE ", "INSERT ")), name


def test_query_names_are_unique_and_numbered() -> None:
    names = list(prepare_analytical_queries())
    assert len(names) == len(set(names))
    assert [name[:3] for name in names] == [f"q{n:02d}" for n in range(1, 11)]