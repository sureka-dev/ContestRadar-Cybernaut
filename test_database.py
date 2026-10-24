import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import database

class TestContestRadarDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_file = Path(self.temp_dir.name) / "test.db"

        self.db_patch = patch.object(
            database, "DB_PATH", self.db_file
        )
        self.db_patch.start()
        self.addCleanup(self.db_patch.stop)

        database.initialize_db()

        self.record = {
            "name": "Python Coding Contest",
            "platform": "Codeforces",
            "category": "Programming",
            "start_date": "2026-11-01T10:00:00Z",
            "duration_minutes": 120,
            "link": "https://codeforces.com/contests/1234",
            "source_api": (
                "https://codeforces.com/api/contest.list"
            ),
            "status": "upcoming",
            "timezone": "UTC",
        }

        self.addCleanup(self.temp_dir.cleanup)

    def test_database_initialization(self):
        records = database.get_competitions()
        self.assertEqual(records, [])

    def test_insert_competition(self):
        competition_id = database.upsert_competition(
            self.record
        )

        result = database.get_competition_by_id(
            competition_id
        )

        self.assertIsNotNone(result)
        self.assertEqual(
            result["title"], "Python Coding Contest"
        )
        self.assertEqual(result["platform"], "Codeforces")

    def test_prevent_duplicate_competitions(self):
        database.upsert_competition(self.record)
        database.upsert_competition(self.record)

        records = database.get_competitions()

        self.assertEqual(len(records), 1)

    def test_update_existing_competition(self):
        first_id = database.upsert_competition(self.record)

        updated = self.record.copy()
        updated["duration_minutes"] = 180
        updated["status"] = "completed"

        second_id = database.upsert_competition(updated)

        records = database.get_competitions()

        self.assertEqual(first_id, second_id)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["duration_minutes"], 180)
        self.assertEqual(records[0]["status"], "completed")

    def test_get_competition_by_id(self):
        competition_id = database.upsert_competition(
            self.record
        )

        result = database.get_competition_by_id(
            competition_id
        )

        self.assertEqual(result["id"], competition_id)

    def test_missing_competition(self):
        self.assertIsNone(
            database.get_competition_by_id(9999)
        )

    def test_filter_by_platform(self):
        database.upsert_competition(self.record)

        results = database.get_competitions(
            platform="Codeforces"
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["platform"], "Codeforces")

        self.assertEqual(
            database.get_competitions(platform="CTFtime"), []
        )

    def test_filter_by_status(self):
        database.upsert_competition(self.record)

        results = database.get_competitions(
            status="upcoming"
        )

        self.assertEqual(len(results), 1)

    def test_invalid_duration(self):
        invalid = self.record.copy()
        invalid["duration_minutes"] = -10

        with self.assertRaises(ValueError):
            database.upsert_competition(invalid)

    def test_bulk_insert_and_duplicates(self):
        database.upsert_competitions(
            [self.record, self.record.copy()]
        )

        self.assertEqual(len(database.get_competitions()), 1)

    def test_invalid_bulk_record(self):
        with self.assertRaises(ValueError):
            database.upsert_competitions([{"name": "Invalid"}])


if __name__ == "__main__":
    unittest.main(verbosity=2)