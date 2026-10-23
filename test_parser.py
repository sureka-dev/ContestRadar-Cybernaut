
import unittest
from datetime import datetime, timedelta, timezone

from parser import (
    clean_name,
    normalize_url,
    parse_datetime,
    normalize_competition,
    deduplicate,
    parse_competitions,
    ALLOWED_APIS
)


class TestParser(unittest.TestCase):

    def setUp(self):
        start = datetime.now(timezone.utc) + timedelta(days=5)
        start = start.replace(microsecond=0)

        self.valid_record = {
            "name": "  Python   Coding Contest  ",
            "platform": "Codeforces",
            "start_date": start.isoformat(),
            "duration_minutes": 120,
            "link": "https://codeforces.com/contests/1234",
            "registration_url": None,
            "_source_api": (
                "https://codeforces.com/api/contest.list"
            )
        }

    def test_clean_name(self):
        self.assertEqual(
            clean_name("  Python   Contest "),
            "Python Contest"
        )

    def test_invalid_name(self):
        self.assertIsNone(clean_name(""))
        self.assertIsNone(clean_name(None))
        self.assertIsNone(clean_name("Unknown"))

    def test_normalize_url(self):
        self.assertEqual(
            normalize_url("HTTPS://CODEFORCES.COM/contests/1234/"),
            "https://codeforces.com/contests/1234"
        )

    def test_invalid_url(self):
        self.assertIsNone(normalize_url("not-a-url"))
        self.assertIsNone(normalize_url(""))
        self.assertIsNone(normalize_url(None))

    def test_parse_datetime(self):
        result = parse_datetime("2027-01-15T10:00:00Z")

        self.assertIsNotNone(result)
        self.assertEqual(result.tzinfo, timezone.utc)

    def test_invalid_datetime(self):
        self.assertIsNone(parse_datetime("invalid-date"))
        self.assertIsNone(parse_datetime(None))

    def test_valid_competition(self):
        result = normalize_competition(self.valid_record)

        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Python Coding Contest")
        self.assertEqual(result["platform"], "Codeforces")
        self.assertEqual(result["category"], "Programming")
        self.assertEqual(result["duration_minutes"], 120)
        self.assertEqual(result["status"], "upcoming")

    def test_invalid_platform(self):
        record = self.valid_record.copy()
        record["platform"] = "Unknown Platform"

        self.assertIsNone(normalize_competition(record))

    def test_invalid_duration(self):
        record = self.valid_record.copy()
        record["duration_minutes"] = -10

        self.assertIsNone(normalize_competition(record))

    def test_invalid_source_api(self):
        record = self.valid_record.copy()
        record["_source_api"] = "https://example.com/api"

        self.assertIsNone(normalize_competition(record))

    def test_duplicate_competitions(self):
        first = normalize_competition(self.valid_record)
        second = first.copy()

        unique = deduplicate([first, second])

        self.assertEqual(len(unique), 1)

    def test_parse_competitions(self):
        results = parse_competitions([
            self.valid_record,
            self.valid_record,
            {"name": "", "platform": "Codeforces"}
        ])

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0]["name"],
            "Python Coding Contest"
        )

    def test_allowed_apis(self):
        self.assertIn(
            "https://codeforces.com/api/contest.list",
            ALLOWED_APIS
        )
        self.assertIn(
            "https://ctftime.org/api/v1/events/",
            ALLOWED_APIS
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
