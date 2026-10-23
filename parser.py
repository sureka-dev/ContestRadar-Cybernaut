
import re
from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit, urlunsplit


DAYS_AHEAD = 180

ALLOWED_PLATFORMS = {
    "Codeforces": "Programming",
    "CTFtime": "Cybersecurity"
}

ALLOWED_APIS = {
    "https://codeforces.com/api/contest.list",
    "https://ctftime.org/api/v1/events/"
}


def clean_name(value):
    if not isinstance(value, str):
        return None

    name = re.sub(r"\s+", " ", value).strip()

    if not name or name.casefold() in {
        "unknown", "untitled", "none", "null"
    }:
        return None

    return name


def normalize_url(value):
    if not isinstance(value, str) or not value.strip():
        return None

    try:
        parts = urlsplit(value.strip())

        if (
            parts.scheme.lower() not in {"http", "https"}
            or not parts.hostname
            or parts.username is not None
            or parts.password is not None
            or any(char.isspace() for char in parts.netloc)
        ):
            return None

        host = parts.hostname.lower()
        port = parts.port

        if port and not (
            (parts.scheme.lower() == "http" and port == 80)
            or (parts.scheme.lower() == "https" and port == 443)
        ):
            host = f"{host}:{port}"

        return urlunsplit((
            parts.scheme.lower(),
            host,
            parts.path.rstrip("/"),
            "",
            ""
        ))

    except (ValueError, TypeError):
        return None


def parse_datetime(value):
    if not isinstance(value, str) or not value.strip():
        return None

    try:
        result = datetime.fromisoformat(
            value.strip().replace("Z", "+00:00")
        )

        if result.tzinfo is None:
            result = result.replace(tzinfo=timezone.utc)

        return result.astimezone(timezone.utc)

    except (ValueError, TypeError, OverflowError):
        return None


def utc_string(value):
    return (
        value.astimezone(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )



def normalize_competition(record):
    from datetime import datetime, timezone, timedelta
    from urllib.parse import urlparse

    if not isinstance(record, dict):
        return None

    name = clean_name(record.get("name", ""))
    platform = record.get("platform", "")
    start_date = parse_datetime(record.get("start_date"))
    duration = record.get("duration_minutes")
    url = normalize_url(record.get("competition_url", record.get("link", "")))

    if not name or platform not in ALLOWED_PLATFORMS:
        return None

    if not start_date:
        return None

    now = datetime.now(timezone.utc)
    if start_date < now or start_date > now + timedelta(days=DAYS_AHEAD):
        return None

    if isinstance(duration, bool) or not isinstance(duration, int) or duration <= 0:
        return None

    parsed_url = urlparse(url)
    host = (parsed_url.hostname or "").lower()

    if platform == "Codeforces" and not (
        host == "codeforces.com" or host.endswith(".codeforces.com")
    ):
        return None

    if platform == "CTFtime" and not (
        host == "ctftime.org" or host.endswith(".ctftime.org")
        or host.endswith(".hitcon.org")
        or host.endswith(".rstcon.org")
        or host.endswith(".org")
        or host.endswith(".com")
        or host.endswith(".net")
        or host.endswith(".io")
    ):
        return None
    
    source_api = record.get("source_api", record.get("_source_api"))

    if source_api is None:
      if platform == "Codeforces":
        source_api = "https://codeforces.com/api/contest.list"
      elif platform == "CTFtime":
        source_api = "https://ctftime.org/api/v1/events/"

    if source_api not in ALLOWED_APIS:
       return None


    return {
        "name": name,
        "platform": platform,
        "category": ALLOWED_PLATFORMS[platform],
        "start_date": utc_string(start_date),
        "duration_minutes": duration,
        "link": url,
        "source_api": source_api,
        "status": "upcoming",
        "timezone": "UTC"
    }




def deduplicate(records):
    unique = {}
    
    for record in records:
        if not isinstance(record, dict):
            continue

        url = record.get("competition_url") or record.get("link")
        name = record.get("name", "")
        start_date = record.get("start_date", "")

        if not url or not name:
            continue

        key = (
            str(url).strip().lower(),
            str(name).strip().lower(),
            str(start_date).strip()
        )

        if key not in unique:
            unique[key] = record

    return sorted(
        unique.values(),
        key=lambda item: item.get("start_date", "")
    )


def parse_competitions(records):
    cleaned_records = []

    for record in records:
        cleaned = normalize_competition(record)

        if cleaned is not None:
            cleaned_records.append(cleaned)

    unique_records = deduplicate(cleaned_records)

    return sorted(
        unique_records,
        key=lambda item: (
            item["start_date"],
            item["name"].casefold()
        )
    )
