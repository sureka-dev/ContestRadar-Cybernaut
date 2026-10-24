CREATE TABLE IF NOT EXISTS competitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    platform TEXT NOT NULL,
    category TEXT NOT NULL,
    start_time TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
    url TEXT NOT NULL,
    source_api TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'upcoming',
    timezone TEXT NOT NULL DEFAULT 'UTC',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (platform, title, start_time, url)
);

CREATE INDEX IF NOT EXISTS idx_competitions_start_time
ON competitions(start_time);

CREATE INDEX IF NOT EXISTS idx_competitions_status
ON competitions(status);