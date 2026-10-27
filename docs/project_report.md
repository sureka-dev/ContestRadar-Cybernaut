# ContestRadar - Project Report

## 1. Project Overview
ContestRadar is a competition tracking project that collects programming contests and cybersecurity events from official APIs.

## 2. Data Sources
- Codeforces API: https://codeforces.com/api/contest.list
- CTFtime API: https://ctftime.org/api/v1/events/

## 3. System Workflow
Official APIs -> Collector -> Parser and Validation -> Database -> Backend -> Website

## 4. Testing Results
Latest recorded pipeline run:
- Raw records: 30
- Clean records: 26
- Rejected records: 4
- Parser and database unit tests: 24 passed

The four rejected records were reported as competitions that had already started.

## 5. Limitations
The current results confirm parser and database unit tests only. Backend integration, complete frontend integration, scheduled refresh, and manual verification of ten source records still require testing.

## 6. Future Improvements
- Complete and test backend integration.
- Add automated scheduled data refresh.
- Expand source coverage.
- Add deadline reminders and stronger error logging.
- Perform end-to-end testing.
