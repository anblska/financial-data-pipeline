# Financial Data Pipeline

A small ETL project. It processes stock market data through an ETL pipeline, transforming raw records into structured data stored in SQLite, with Apache Airflow orchestrating the workflow.

**Heads up:** the Airflow DAG currently runs on synthetic test data. There's a separate script that pulls real data from the Alpha Vantage API, but I haven't plugged it into the DAG yet.

## How it works

Data goes through three stages:

1. **Bronze:** raw JSON records (date, ticker, open, high, low, close, volume), either generated test data or pulled from Alpha Vantage.
2. **Silver:** pandas cleans the JSON and writes it out as CSV.
3. **Database:** the CSVs get loaded into SQLite. It uses an upsert on `date` + `ticker`, so running the same data twice updates rows instead of duplicating them.

The Airflow DAG runs `test_bronze` → `transform_market_data` → `load_market_data`. The scripts are in `dags/`.

## Running it

You'll need Docker with Docker Compose, and optionally an Alpha Vantage API key.

Clone the repo:

```bash
git clone https://github.com/anblska/financial-data-pipeline.git
cd financial-data-pipeline
```

Create a `.env` file in the project root:

```dotenv
POSTGRES_PASSWORD=your_postgres_password
FERNET_KEY=your_generated_fernet_key
AIRFLOW__API_AUTH__JWT_SECRET=your_generated_jwt_secret
_AIRFLOW_WWW_USER_PASSWORD=your_airflow_admin_password
ALPHA_VANTAGE_API_KEY=your_api_key
```

The API key is only needed for the real-data script. To generate the secrets:

```bash
# JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Fernet key (needs the cryptography package)
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Don't commit your `.env` file. It's already in `.gitignore`.

Then start Airflow:

```bash
docker compose up airflow-init
docker compose up -d
```

Open http://localhost:8080, log in, enable the DAG, and trigger a run. It generates test data, transforms it, and loads it into SQLite.

This is a local learning setup, not production-ready. You may need to tweak file paths if you run it on another machine.

## Where the data goes

- `data/bronze/market/` has the raw JSON
- `data/silver/market/` has the cleaned CSVs
- SQLite holds the final records

Generated data and databases aren't tracked in Git.

## What's left

- [ ] Plug the Alpha Vantage script into the DAG
- [ ] Add data quality tests
- [ ] Add cloud storage (probably S3)
- [ ] Bring in macroeconomic data from FRED

## License

MIT. See [LICENSE](LICENSE).
