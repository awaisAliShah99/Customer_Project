# Customer Data Engineering Pipeline

## 1. Overview

This repository is an undergraduate practical assignment. Students will design and complete a small, industry-style customer-orders pipeline using pandas, SQLAlchemy, a SQL database, pytest, and Docker. The supplied CSV is intentionally dirty. The scaffold deliberately contains TODOs and `pass` placeholders rather than implementation answers.

## 2. Objectives

Students will:

1. Load raw customer-order data.
2. Clean and transform records.
3. Validate data quality and document accepted, corrected, and rejected records.
4. Save the selected records to `data/clean/cleaned_customers.csv`.
5. Connect Python to SQL and load the `customer_orders` table.
6. Answer business questions with SQL.
7. Test the pipeline with pytest.
8. Containerize the application and connect it to a separate SQL container.
9. Produce an evidence-based management report.

## 3. Architecture

```text
data/raw/data.csv
        |
        v
src/ingestion/load_data.py
        |
        v
src/transformations/clean_data.py
        |
        v
src/validation/validate_data.py
        |
        +--> data/clean/cleaned_customers.csv
        |
        v
src/database/connection.py --> SQL container: customer_orders
        |
        v
reports/sql/ and reports/screenshots/
```

## 4. Folder and file responsibilities

- `data/raw/data.csv`: required input location; do not overwrite the original source.
- `data/clean/`: destination for the cleaned CSV.
- `src/config.py`: paths, table name, and environment-driven database settings.
- `src/ingestion/load_data.py`: raw CSV loading function.
- `src/transformations/clean_data.py`: student cleaning and transformation function.
- `src/validation/validate_data.py`: student validation function.
- `src/database/connection.py`: SQLAlchemy connection function.
- `src/database/load_to_sql.py`: SQL loading function for `customer_orders`.
- `src/analytics/queries.py`: organization point for student analytical SQL.
- `src/pipeline.py`: calls the stages in the required order.
- `tests/`: student-authored pytest tests.
- `reports/sql/`: the ten SQL query files written by students.
- `reports/screenshots/`: screenshots of each query and its result.
- `docs/`: assignment brief and report template.

## 5. Pipeline flow

`run_pipeline()` must load raw data, transform it, validate it, save the validated output, connect to SQL, load the records, and provide an execution summary. The scaffold calls the stages in that order, but students must implement every TODO before running it successfully.

## 6. Environment and dependencies

Copy `.env.example` to `.env` and set `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD`. Never commit `.env` or credentials. Install dependencies with:

```powershell
python -m pip install -r requirements.txt
```

## 7. Running locally

Place the source CSV at `data/raw/data.csv`, complete the TODO sections, then run:

```powershell
python -m src.pipeline
```

Run tests with:

```powershell
pytest
```

## 8. Docker and networking

Build the required image name:

```powershell
docker build -t customer-project .
```

Create a user-defined network:

```powershell
docker network create customer-network
```

Run the SQL database and Python application as separate containers, attaching both to `customer-network`. The application must use the SQL database container or service name as `DB_HOST`; `localhost` inside the Python container refers to the Python container itself, not the database container. Pass database settings as environment variables at runtime. Do not put passwords in the Dockerfile or image. Do not automatically create or start containers from this repository.

## 9. SQL verification and analysis

After loading the table, verify row counts and inspect records using the SQL client connected to the database container. Write one query file per business question under `reports/sql/`, execute each query in the database, and save query/result screenshots under `reports/screenshots/`.

Questions:

1. Which cities generate the highest number of orders and total revenue?
2. Which product categories generate the most revenue?
3. What is the average order value for each customer segment?
4. Which payment methods are most frequently used?
5. What percentage of orders are completed, pending, cancelled, and returned?
6. Which months have the highest and lowest sales?
7. Which customers have spent the most money?
8. Are there unusual prices, quantities, or order totals that require investigation?
9. How many records were accepted, corrected, or rejected during data cleaning?
10. Based on the analysis, what recommendations would you give to management?

## 10. GitHub submission

Create a new **public** GitHub repository, upload the complete project, commit after each milestone with meaningful messages, and push the final version to `main`. Verify that the repository is public. Do not upload `.env`, passwords, API keys, or other sensitive information. Submit the public repository URL to Google Classroom.

## 11. Documents

Read `docs/Student_Assignment_Brief.docx` for the full milestones and requirements. Complete `docs/Manager_Analytical_Report_Template.docx` in your own words, including evidence for numerical claims and all screenshots.
