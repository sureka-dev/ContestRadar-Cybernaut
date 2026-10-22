
"""Collect upcoming competitions from public APIs."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

CODEFORCES_URL = "https://codeforces.com/api/contest.list"
CTFTIME_URL = "https://ctftime.org/api/v1/events/"
ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT_DIR / "fixtures" / "raw_data.json"
TIMEOUT_SECONDS = 20
MAX_RECORDS = 30
DAYS_AHEAD = 180

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def get_json(url: str, params: dict | None = None) -> Any:
    """Fetch JSON from a public API."""
    response = requests.get(
        url,
        params=params,
        timeout=TIMEOUT_SECONDS,
        headers={"User-Agent": "ContestRadar student project"},
    )
    response.raise_for_status()
    return response.json()


def fetch_codeforces() -> list[dict[str, Any]]:
    """Fetch upcoming Codeforces contests."""
    payload = get_json(CODEFORCES_URL, {"gym": "false"})

    if payload.get("status") != "OK":
        raise RuntimeError(payload.get("comment", "Codeforces API error"))

    now = datetime.now(timezone.utc).timestamp()
    latest = now + DAYS_AHEAD * 24 * 60 * 60
    records = []

    for item in payload.get("result", []):
        if item.get("phase") != "BEFORE":
            continue

        start = item.get("startTimeSeconds")
        duration = item.get("durationSeconds")
        if start is None or duration is None or not now <= start <= latest:
            continue

        records.append({
            "name": item.get("name", "Untitled contest"),
            "platform": "Codeforces",
            "start_date": datetime.fromtimestamp(
                start, timezone.utc
            ).isoformat().replace("+00:00", "Z"),
            "duration_minutes": duration // 60,
            "link": f"https://codeforces.com/contests/{item['id']}",
        })

    return records


def fetch_ctftime() -> list[dict[str, Any]]:
    """Fetch upcoming CTFtime events."""
    now = datetime.now(timezone.utc).timestamp()
    latest = now + DAYS_AHEAD * 24 * 60 * 60

    payload = get_json(
        CTFTIME_URL,
        params={
            "limit": 100,
            "start": int(now),
            "finish": int(latest),
        },
    )

    records = []
    for item in payload:
        start = item.get("start")
        finish = item.get("finish")
        if not start or not finish:
            continue

        start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
        finish_dt = datetime.fromisoformat(finish.replace("Z", "+00:00"))
        if start_dt.timestamp() < now or start_dt.timestamp() > latest:
            continue

        duration = max(
            0, int((finish_dt - start_dt).total_seconds() // 60)
        )
        records.append({
            "name": item.get("title", "Untitled event"),
            "platform": "CTFtime",
            "start_date": start_dt.astimezone(
                timezone.utc
            ).isoformat().replace("+00:00", "Z"),
            "duration_minutes": duration,
            "link": item.get("url", ""),
        })

    return records


def main() -> int:
    all_records = []

    for source_name, fetcher in (
        ("Codeforces", fetch_codeforces),
        ("CTFtime", fetch_ctftime),
    ):
        try:
            records = fetcher()
            logger.info("%s: collected %d upcoming records", source_name, len(records))
            all_records.extend(records)
        except (requests.RequestException, ValueError, RuntimeError, TypeError) as exc:
            logger.warning("%s collection failed: %s", source_name, exc)

    # Deduplicate using platform and link.
    unique = {}
    for record in all_records:
        key = (record["platform"], record["link"] or record["name"])
        unique[key] = record

    competitions = sorted(
        unique.values(), key=lambda item: item["start_date"]
    )[:MAX_RECORDS]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    output = {
        "sources": [
            {"name": "Codeforces API", "url": CODEFORCES_URL},
            {"name": "CTFtime API", "url": CTFTIME_URL},
        ],
        "collected_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "count": len(competitions),
        "target_count": MAX_RECORDS,
        "competitions": competitions,
    }

    OUTPUT_FILE.write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    logger.info("Saved %d real records (target: %d) to %s",
                len(competitions), MAX_RECORDS, OUTPUT_FILE)

    if len(competitions) < MAX_RECORDS:
        logger.warning(
            "%d more records are needed. Add more verified sources; "
            "do not create sample records to fill the target.",
            MAX_RECORDS - len(competitions),
        )

    return 0 if competitions else 1


if __name__ == "__main__":
    raise SystemExit(main())
