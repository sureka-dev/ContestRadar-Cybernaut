
import json
import sqlite3
from pathlib import Path
from contextlib import contextmanager


# Project folders
DATABASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = DATABASE_DIR.parent

DB_PATH = DATABASE_DIR / "contestradar.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"


@contextmanager
def get_connection():
    """Create, use, and close a database connection."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        with connection:
            yield connection
    finally:
        connection.close()


def initialize_db():
    """Create the database table and indexes."""
    with get_connection() as connection:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)


def upsert_competition(record):
    """Insert or update one competition."""
    if not isinstance(record, dict):
        raise ValueError("Competition must be a dictionary.")

    title = record.get("name", record.get("title"))
    start_time = record.get("start_date", record.get("start_time"))
    url = record.get(
        "link", record.get("competition_url", record.get("url"))
    )
    source_api = record.get("source_api", record.get("_source_api"))

    required = {
        "title": title,
        "platform": record.get("platform"),
        "category": record.get("category"),
        "start_time": start_time,
        "url": url,
        "source_api": source_api,
    }

    for field, value in required.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Missing or invalid field: {field}")

    duration = record.get("duration_minutes")

    if (
        isinstance(duration, bool)
        or not isinstance(duration, int)
        or duration <= 0
    ):
        raise ValueError("duration_minutes must be a positive integer.")

    values = (
        title.strip(),
        record["platform"].strip(),
        record["category"].strip(),
        start_time.strip(),
        duration,
        url.strip(),
        source_api.strip(),
        record.get("status", "upcoming"),
        record.get("timezone", "UTC"),
    )

    sql = """
        INSERT INTO competitions (
            title, platform, category, start_time,
            duration_minutes, url, source_api, status, timezone
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(platform, title, start_time, url)
        DO UPDATE SET
            category = excluded.category,
            duration_minutes = excluded.duration_minutes,
            source_api = excluded.source_api,
            status = excluded.status,
            timezone = excluded.timezone,
            updated_at = CURRENT_TIMESTAMP
    """

    with get_connection() as connection:
        connection.execute(sql, values)

        row = connection.execute(
            """
            SELECT id FROM competitions
            WHERE platform = ? AND title = ?
              AND start_time = ? AND url = ?
            """,
            (values[1], values[0], values[3], values[5]),
        ).fetchone()

        return row["id"]


def upsert_competitions(records):
    """Insert or update multiple competitions."""
    if not isinstance(records, list):
        raise ValueError("records must be a list.")

    # Validate records before writing to the database.
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each competition must be a dictionary.")

        title = record.get("name", record.get("title"))
        start_time = record.get("start_date", record.get("start_time"))
        url = record.get(
            "link", record.get("competition_url", record.get("url"))
        )
        source_api = record.get("source_api", record.get("_source_api"))
        duration = record.get("duration_minutes")

        required_values = [
            title,
            record.get("platform"),
            record.get("category"),
            start_time,
            url,
            source_api,
        ]

        if any(
            not isinstance(value, str) or not value.strip()
            for value in required_values
        ):
            raise ValueError("A competition has missing required fields.")

        if (
            isinstance(duration, bool)
            or not isinstance(duration, int)
            or duration <= 0
        ):
            raise ValueError("Invalid competition duration.")

    # Import all records in one transaction.
    with get_connection() as connection:
        for record in records:
            title = record.get("name", record.get("title"))
            start_time = record.get(
                "start_date", record.get("start_time")
            )
            url = record.get(
                "link", record.get("competition_url", record.get("url"))
            )
            source_api = record.get(
                "source_api", record.get("_source_api")
            )

            connection.execute(
                """
                INSERT INTO competitions (
                    title, platform, category, start_time,
                    duration_minutes, url, source_api, status, timezone
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(platform, title, start_time, url)
                DO UPDATE SET
                    category = excluded.category,
                    duration_minutes = excluded.duration_minutes,
                    source_api = excluded.source_api,
                    status = excluded.status,
                    timezone = excluded.timezone,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    title.strip(),
                    record["platform"].strip(),
                    record["category"].strip(),
                    start_time.strip(),
                    record["duration_minutes"],
                    url.strip(),
                    source_api.strip(),
                    record.get("status", "upcoming"),
                    record.get("timezone", "UTC"),
                ),
            )

    return len(records)


def get_competitions(platform=None, status=None, limit=None):
    """Retrieve competitions with optional filters."""
    sql = "SELECT * FROM competitions WHERE 1=1"
    params = []

    if platform:
        sql += " AND platform = ?"
        params.append(platform)

    if status:
        sql += " AND status = ?"
        params.append(status)

    sql += " ORDER BY start_time ASC, title COLLATE NOCASE ASC"

    if limit is not None:
        if (
            isinstance(limit, bool)
            or not isinstance(limit, int)
            or limit <= 0
        ):
            raise ValueError("limit must be a positive integer.")

        sql += " LIMIT ?"
        params.append(limit)

    with get_connection() as connection:
        rows = connection.execute(sql, params).fetchall()
        return [dict(row) for row in rows]


def get_competition_by_id(competition_id):
    """Retrieve one competition by its ID."""
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM competitions WHERE id = ?",
            (competition_id,),
        ).fetchone()

        return dict(row) if row else None


def import_clean_data(json_path=None):
    """Import cleaned competition records into SQLite."""
    if json_path is None:
        json_path = PROJECT_DIR / "Clean_data.json"

    json_path = Path(json_path)

    with json_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    records = data.get("competitions", [])

    if not isinstance(records, list):
        raise ValueError("'competitions' must be a list.")

    return upsert_competitions(records)


if __name__ == "__main__":
    initialize_db()
    imported = import_clean_data()

    print("ContestRadar database initialized successfully.")
    print(f"Records processed: {imported}")
    print(f"Total competitions: {len(get_competitions())}")

    for competition in get_competitions(limit=5):
        print(
            competition["id"],
            competition["title"],
            competition["platform"],
            competition["start_time"],
        )
