<<<<<<< HEAD
﻿# ContestRadar

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
=======
﻿# 🎯 ContestRadar – Live Competition & Deadline Tracker

ContestRadar is a competition-tracking project that collects, cleans, and organizes programming contests and cybersecurity events in one place. It helps students and developers discover competitions and keep track of upcoming events.

## 🌟 Project Overview

Finding competitions across different platforms can be time-consuming. ContestRadar aims to make this easier by bringing competition information together in one place.

The project uses official APIs to collect competition data, validates and cleans the records, and stores structured information for further use.

## ✨ Features

- 💻 Collects programming contest data from Codeforces.
- 🔐 Collects cybersecurity event data from CTFtime.
- 🧹 Validates and cleans collected records.
- 🗃️ Stores structured competition data.
- 🔍 Supports competition discovery through the project dashboard.
- 🧪 Includes automated tests for data parsing and database functionality.

## 📸 Project Screenshots

### 🏠 Homepage

![ContestRadar Homepage](docs/screenshots/homepage.PNG)

### 🏆 Competitions

![ContestRadar Competitions](docs/screenshots/competitions.PNG)

### 💡 Example

![ContestRadar Example](docs/screenshots/example.PNG)

## 🛠️ Technologies Used

- **Frontend:** React and Vite
- **Backend and Data Processing:** Python
- **Database:** SQLite
- **Data Sources:** Codeforces API and CTFtime API
- **Testing:** Python unittest
- **Version Control:** Git and GitHub

## 🔗 Data Sources

| Platform | Official API |
|---|---|
| Codeforces | https://codeforces.com/api/contest.list |
| CTFtime | https://ctftime.org/api/v1/events/ |

## 📂 Project Structure

```text
ContestRadar-Cybernaut/
├── collector/
│   └── api_collector.py
├── fixtures/
│   └── raw_data.json
├── docs/
│   ├── screenshots/
│   │   ├── homepage.PNG
│   │   ├── competitions.PNG
│   │   └── example.PNG
│   ├── accuracy_check.csv
│   ├── data_dictionary.md
│   └── project_report.md
├── tests/
├── app.py
├── database.py
├── parser.py
├── run_pipeline.py
├── schema.sql
├── requirements.txt
├── clean_data.json
├── test_parser.py
└── test_database.py
```

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sureka-dev/ContestRadar-Cybernaut.git
```

### 2. Open the project folder

```bash
cd ContestRadar-Cybernaut
```

### 3. Install dependencies
>>>>>>> dd8ee05 (Update README and add project screenshots)

```bash
pip install -r requirements.txt
```

<<<<<<< HEAD
Run the pipeline:
=======
### 4. Run the data pipeline
>>>>>>> dd8ee05 (Update README and add project screenshots)

```bash
python run_pipeline.py
```

<<<<<<< HEAD
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
=======
The pipeline processes competition records, validates them, and saves the cleaned data.

### 5. Run automated tests

```bash
python -m unittest test_parser.py test_database.py -v
```

## 🧪 Testing

The project includes tests for:

- Data parsing and validation.
- Invalid record handling.
- Duplicate record handling.
- Database insertion and retrieval.
- Database filtering and updates.

The test suite previously passed 24 tests.

## 🔄 Data Processing Workflow

1. Collect competition data from supported APIs.
2. Parse and validate the records.
3. Reject records that fail validation.
4. Store and organize valid records.
5. Save the cleaned dataset.

## 🎯 Project Objectives

- Simplify competition discovery.
- Organize programming and cybersecurity events.
- Improve the reliability of collected data.
- Gain practical experience with APIs, data processing, databases, and testing.
- Build a useful project through teamwork and collaboration.

## 🚀 Future Enhancements

- Integrate additional official competition APIs.
- Improve search and filtering features.
- Add competition deadline reminders.
- Expand competition categories.
- Improve the user interface and mobile responsiveness.
- Add more automated tests and data accuracy checks.

## 👥 Team Project

**Project:** ContestRadar – Live Competition & Deadline Tracker

A collaborative project focused on API-based data collection, data cleaning, database management, testing, and competition discovery.

## 📄 License

This project is intended for educational and development purposes. A specific open-source license can be added when required.
>>>>>>> dd8ee05 (Update README and add project screenshots)
