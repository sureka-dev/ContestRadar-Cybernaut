# 🎯 ContestRadar – Live Competition & Deadline Tracker

ContestRadar is a competition-tracking project that collects, cleans, and organizes upcoming programming contests and cybersecurity events in one place. It helps students and developers discover competitions and keep track of important deadlines.

## 🌟 Project Overview

Finding competitions across multiple platforms can be time-consuming. ContestRadar aims to simplify this process by bringing competition information together in a single dashboard.

The project uses official APIs to collect competition data, validates and cleans the collected records, and stores structured data for further use.

## ✨ Key Features

- 📌 Collects competition data from supported platforms.
- 💻 Supports programming contests from Codeforces.
- 🔐 Supports cybersecurity events from CTFtime.
- 🧹 Validates and cleans collected records.
- 🗃️ Stores structured competition data.
- 🔍 Provides a foundation for discovering and tracking competitions.
- 🧪 Includes automated tests for parser and database functionality.

## 📸 Project Screenshots

### 🏠 Homepage
![ContestRadar Homepage](docs/screenshots/homepage.png)

### 🏆 Competitions
![ContestRadar Competitions](docs/screenshots/competitions.png)

### 💡 Example
![ContestRadar Example](docs/screenshots/example.png)

## 🛠️ Technologies Used

- **Frontend:** React, Vite (if included in your project frontend)
- **Backend:** Python
- **Data Processing:** Python
- **Database:** SQLite
- **Data Sources:** Codeforces API, CTFtime API
- **Testing:** Python `unittest`
- **Version Control:** Git and GitHub

## 🔗 Official Data Sources

| Platform | API |
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
│   │   ├── homepage.png
│   │   ├── competitions.png
│   │   └── example.png
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

### 2. Navigate to the project directory

```bash
cd ContestRadar-Cybernaut
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the data pipeline

```bash
python run_pipeline.py
```

The pipeline collects or processes competition records, validates the data, and saves the cleaned output to `Clean_data.json`.

### 5. Run the tests

```bash
python -m unittest test_parser.py test_database.py -v
```

## 🧪 Testing

The project includes automated tests for:

- Data validation and parsing.
- Handling invalid records.
- Duplicate record handling.
- Database insertion and retrieval.
- Database filtering and updates.

The parser and database test suite has previously passed **24 tests**. Run the test command above to verify the current version.

## 📊 Data Processing Workflow

1. Collect competition data from supported APIs.
2. Parse and validate the collected records.
3. Reject records that do not meet the project's validation rules.
4. Store and organize valid competition records.
5. Save the cleaned dataset for further use.

## 🎯 Project Goals

- Make competition discovery easier.
- Organize programming and cybersecurity events.
- Improve the reliability of collected data.
- Practice API integration, data cleaning, database management, testing, and collaborative development.

## 🚀 Future Improvements

- Add more official competition APIs.
- Improve search and filtering.
- Add deadline reminders.
- Provide more competition categories.
- Improve the user interface and mobile responsiveness.
- Expand automated tests and data accuracy checks.

## 👥 Team Project

**Project Name:** ContestRadar – Live
