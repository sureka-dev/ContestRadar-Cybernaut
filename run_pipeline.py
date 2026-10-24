
import json
from datetime import datetime, timezone
from pathlib import Path

from parser import parse_competitions

ROOT_DIR = Path(__file__).resolve().parent
RAW_FILE = ROOT_DIR / "fixtures" / "raw_data.json"
CLEAN_FILE = ROOT_DIR / "Clean_data.json"


def main():
    # Read the collector's output
    with RAW_FILE.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)

    records = raw_data.get("competitions", [])

    # Clean and validate the records
    cleaned = parse_competitions(records)

    # Save the cleaned output
    output = {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "count": len(cleaned),
        "competitions": cleaned
    }

    with CLEAN_FILE.open("w", encoding="utf-8") as file:
        json.dump(output, file, indent=2, ensure_ascii=False)

    print(f"Raw records: {len(records)}")
    print(f"Clean records: {len(cleaned)}")
    print(f"Rejected records: {len(records) - len(cleaned)}")
    print(f"Saved to: {CLEAN_FILE}")


if __name__ == "__main__":
    main()
