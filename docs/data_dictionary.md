# ContestRadar Data Dictionary

Each cleaned competition record contains the following fields.

| Field | Meaning | Example |
|---|---|---|
| name | Competition name | Codeforces Round 1131 (Div. 3) |
| platform | Source platform | Codeforces |
| category | Competition category | Programming |
| start_date | Start time in ISO 8601 UTC format | 2026-10-31T14:35:00Z |
| duration_minutes | Duration in minutes | 135 |
| link | Competition or event page | https://codeforces.com/contests/2278 |
| source_api | API used to collect the record | https://codeforces.com/api/contest.list |
| status | Current pipeline status label | upcoming |
| timezone | Time zone used for the stored date | UTC |

The cleaned JSON file also contains top-level metadata:
- collected_at: timestamp when the output was generated
- count: number of cleaned records
- competitions: list of cleaned competition records

Examples are illustrative of the current project schema. Actual values can change between pipeline runs.
