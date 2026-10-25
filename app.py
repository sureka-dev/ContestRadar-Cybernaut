
from flask import Flask, jsonify, request
from flask_cors import CORS
from pathlib import Path
import subprocess
import sys

from database import (
    initialize_db,
    get_competitions as db_get_competitions,
    get_competition_by_id,
    import_clean_data,
)

app = Flask(__name__)
CORS(app)

ROOT_DIR = Path(__file__).resolve().parent


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "ContestRadar API is running"
    })


@app.route("/api/competitions", methods=["GET"])
def competitions():
    try:
        platform = request.args.get("platform")
        status = request.args.get("status")
        limit_value = request.args.get("limit")

        limit = int(limit_value) if limit_value else None

        records = db_get_competitions(
            platform=platform,
            status=status,
            limit=limit
        )

        return jsonify({
            "status": "success",
            "count": len(records),
            "competitions": records
        })

    except ValueError as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    except Exception:
        app.logger.exception("Could not retrieve competitions")
        return jsonify({
            "status": "error",
            "message": "Could not retrieve competitions"
        }), 500


@app.route("/api/competitions/<int:competition_id>", methods=["GET"])
def competition_detail(competition_id):
    try:
        record = get_competition_by_id(competition_id)

        if record is None:
            return jsonify({
                "status": "error",
                "message": "Competition not found"
            }), 404

        return jsonify({
            "status": "success",
            "competition": record
        })

    except Exception:
        app.logger.exception("Could not retrieve competition")
        return jsonify({
            "status": "error",
            "message": "Could not retrieve competition"
        }), 500


@app.route("/api/stats", methods=["GET"])
def stats():
    try:
        records = db_get_competitions()

        platform_counts = {}
        status_counts = {}

        for record in records:
            platform = record["platform"]
            status = record["status"]

            platform_counts[platform] = (
                platform_counts.get(platform, 0) + 1
            )
            status_counts[status] = (
                status_counts.get(status, 0) + 1
            )

        return jsonify({
            "status": "success",
            "total": len(records),
            "by_platform": platform_counts,
            "by_status": status_counts
        })

    except Exception:
        app.logger.exception("Could not calculate statistics")
        return jsonify({
            "status": "error",
            "message": "Could not calculate statistics"
        }), 500


@app.route("/api/refresh", methods=["POST"])
def refresh():
    try:
        result = subprocess.run(
            [sys.executable, str(ROOT_DIR / "run_pipeline.py")],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            app.logger.error("Pipeline failed: %s", result.stderr)
            return jsonify({
                "status": "error",
                "message": "Competition refresh failed",
                "details": result.stderr[-1000:]
            }), 500

        # Import the newly cleaned records into SQLite.
        initialize_db()
        imported = import_clean_data(ROOT_DIR / "Clean_data.json")
        total = len(db_get_competitions())

        return jsonify({
            "status": "success",
            "message": "Competition refresh completed",
            "records_processed": imported,
            "database_total": total,
            "pipeline_output": result.stdout
        })

    except subprocess.TimeoutExpired:
        return jsonify({
            "status": "error",
            "message": "Refresh timed out"
        }), 504

    except Exception:
        app.logger.exception("Competition refresh failed")
        return jsonify({
            "status": "error",
            "message": "Could not refresh competitions"
        }), 500


if __name__ == "__main__":
    initialize_db()
    app.run(debug=True, host="127.0.0.1", port=5000)
