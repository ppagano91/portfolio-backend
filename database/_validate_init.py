"""Validate profile/experience/education DML from init.sql against the local DB."""

from pathlib import Path

import psycopg2

INIT_PATH = Path(__file__).with_name("init.sql")

SECTION_MARKERS = [
    "-- PROFILE & EXPERIENCES",
    "-- EDUCATION",
    "-- PROJECTS",
]


def extract_section(sql: str, start_marker: str, end_marker: str | None) -> str:
    start = sql.index(start_marker)
    if end_marker:
        end = sql.index(end_marker, start)
        chunk = sql[start:end]
    else:
        chunk = sql[start:]
    return chunk.strip().rstrip(";")


def main() -> None:
    sql = INIT_PATH.read_text(encoding="utf-8")
    profile_exp = extract_section(sql, SECTION_MARKERS[0], SECTION_MARKERS[1])
    education = extract_section(sql, SECTION_MARKERS[1], SECTION_MARKERS[2])

    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5433,
        user="postgres",
        password="123456",
        dbname="portfolio",
    )
    conn.autocommit = False
    cur = conn.cursor()
    try:
        cur.execute("BEGIN")
        cur.execute(profile_exp)
        cur.execute(education)
        cur.execute("ROLLBACK")
        print("OK: profile, experiences and education DML executed without errors")
    except Exception as exc:
        conn.rollback()
        raise SystemExit(f"SQL validation failed: {exc}") from exc
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
