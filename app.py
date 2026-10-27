
from flask import Flask, jsonify, request
from flask_cors import CORS
from pathlib import Path
import subprocess
import sys
import os
import sqlite3

import database

app = Flask(__name__)
CORS(app)

ROOT_DIR = Path(__file__).resolve().parent


# ---------- DATABASE STARTUP ----------

def initialize_app_database():
    """Create database tables and load initial competition data."""
    database.initialize_db()

    records = database.get_competitions()

    if not records:
        candidates = [
            ROOT_DIR / "Clean_data.json",
            ROOT_DIR / "clean_data.json",
        ]

        clean_file = next(
            (path for path in candidates if path.exists()),
            None
        )

        if clean_file:
            imported = database.import_clean_data(clean_file)
            app.logger.info("Imported %s competition records", imported)
        else:
            app.logger.warning(
                "No cleaned data file found; database is initialized but empty."
            )


try:
    initialize_app_database()
except Exception:
    app.logger.exception("Database startup initialization failed")


# ---------- HELPERS ----------

def format_competition(item):
    """Convert a database row to the API response format."""
    return {
        "id": item["id"],
        "name": item["title"],
        "platform": item["platform"],
        "category": item["category"],
        "start_date": item["start_time"],
        "duration_minutes": item["duration_minutes"],
        "link": item["url"],
        "source_api": item["source_api"],
        "status": item["status"],
        "timezone": item["timezone"],
    }


def ensure_database():
    """Ensure the table exists before handling database requests."""
    database.initialize_db()


# ---------- HEALTH ----------

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "ContestRadar API is running",
    })


# ---------- LIST COMPETITIONS ----------

@app.route("/api/competitions", methods=["GET"])
def competitions():
    try:
        ensure_database()

        platform = request.args.get("platform")
        status = request.args.get("status")
        limit_value = request.args.get("limit")

        try:
            limit = int(limit_value) if limit_value else None
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Limit must be an integer",
            }), 400

        if limit is not None and limit < 1:
            return jsonify({
                "status": "error",
                "message": "Limit must be greater than zero",
            }), 400

        records = database.get_competitions(
            platform=platform,
            status=status,
            limit=limit,
        )

        items = [format_competition(item) for item in records]

        return jsonify({
            "status": "success",
            "count": len(items),
            "competitions": items,
        })

    except Exception:
        app.logger.exception("Could not retrieve competitions")
        return jsonify({
            "status": "error",
            "message": "Could not retrieve competitions",
        }), 500


# ---------- COMPETITION DETAILS ----------

@app.route("/api/competitions/<int:competition_id>", methods=["GET"])
def competition_detail(competition_id):
    try:
        ensure_database()
        record = database.get_competition_by_id(competition_id)

        if record is None:
            return jsonify({
                "status": "error",
                "message": "Competition not found",
            }), 404

        return jsonify({
            "status": "success",
            "competition": format_competition(record),
        })

    except Exception:
        app.logger.exception("Could not retrieve competition details")
        return jsonify({
            "status": "error",
            "message": "Could not retrieve competition details",
        }), 500


# ---------- STATISTICS ----------

@app.route("/api/stats", methods=["GET"])
def stats():
    try:
        ensure_database()
        records = database.get_competitions()

        platform_counts = {}
        category_counts = {}
        status_counts = {}

        for item in records:
            platform = item["platform"]
            category = item["category"]
            status = item["status"]

            platform_counts[platform] = platform_counts.get(platform, 0) + 1
            category_counts[category] = category_counts.get(category, 0) + 1
            status_counts[status] = status_counts.get(status, 0) + 1

        return jsonify({
            "status": "success",
            "total": len(records),
            "by_platform": platform_counts,
            "by_category": category_counts,
            "by_status": status_counts,
        })

    except Exception:
        app.logger.exception("Could not retrieve statistics")
        return jsonify({
            "status": "error",
            "message": "Could not retrieve statistics",
        }), 500


# ---------- REFRESH COMPETITIONS ----------

@app.route("/api/refresh", methods=["POST"])
def refresh_competitions():
    try:
        database.initialize_db()

        result = subprocess.run(
            [sys.executable, str(ROOT_DIR / "run_pipeline.py")],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            app.logger.error("Pipeline failed: %s", result.stderr)
            return jsonify({
                "status": "error",
                "message": "Competition refresh failed",
                "details": result.stderr[-1000:],
            }), 500

        candidates = [
            ROOT_DIR / "Clean_data.json",
            ROOT_DIR / "clean_data.json",
        ]

        clean_file = next(
            (path for path in candidates if path.exists()),
            None
        )

        if clean_file is None:
            return jsonify({
                "status": "error",
                "message": "Cleaned competition data file was not created",
                "pipeline_output": result.stdout[-1000:],
            }), 500

        imported = database.import_clean_data(clean_file)
        total = len(database.get_competitions())

        return jsonify({
            "status": "success",
            "message": "Competition refresh completed",
            "records_processed": imported,
            "database_total": total,
            "pipeline_output": result.stdout,
        })

    except subprocess.TimeoutExpired:
        return jsonify({
            "status": "error",
            "message": "Refresh timed out",
        }), 504

    except Exception:
        app.logger.exception("Competition refresh failed")
        return jsonify({
            "status": "error",
            "message": "Could not refresh competitions",
        }), 500


# ---------- LOCAL SERVER ----------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False,
    )
