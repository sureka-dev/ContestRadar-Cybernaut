# ContestRadar

ContestRadar tracks programming competitions and cybersecurity events.

## Data Sources
- Codeforces API: https://codeforces.com/api/contest.list
- CTFtime API: https://ctftime.org/api/v1/events/

## Main Components
- `collector/api_collector.py` - data collection
- `parser.py` - validation and normalization
- `database.py` and `schema.sql` - database operations and schema
- `run_pipeline.py` - pipeline execution
- `app.py` - application/backend entry point; verify its actual routes before describing the API as complete
- `clean_data.json` - latest cleaned output
- `tests/` - parser and database regression tests
- `docs/` - project documentation and accuracy checks

## Setup
Install dependencies:

```bash
pip install -r requirements.txt
```

Run the pipeline:

```bash
python run_pipeline.py
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Latest Recorded Test Results
- 30 raw records processed
- 26 clean records
- 4 records rejected
- 24 existing parser/database unit tests passed

These are results from one recorded run and may change when the source APIs update.

## Verification Status
Manual verification of ten competition records and full backend/frontend integration testing are pending. See `docs/accuracy_check.csv` and `docs/project_report.md`.
