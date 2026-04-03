# Demo Environment Builder

[![CI](https://github.com/dunsworthdavid/demo-env-builder/actions/workflows/ci.yml/badge.svg)](https://github.com/dunsworthdavid/demo-env-builder/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)
![AWS S3](https://img.shields.io/badge/AWS-S3-orange)
![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey)

> **Spin up a complete, realistic demo environment in seconds — customers, products, transactions, and a live API — so you never waste sales cycle time on fake data.**

---

## The Problem

Solutions Engineers spend hours before every demo manually assembling fake data — spreadsheets, hardcoded CSVs, or worse, live production databases. It's slow, inconsistent, and breaks at the worst times.

## The Solution

**Demo Environment Builder** is a CLI + REST API tool that generates a fully populated, realistic SaaS dataset on demand. One command seeds an SQLite database with customers, products, and transactions, uploads a JSON report to S3 for audit/sharing, and exposes a live API you can point any frontend or integration at.

Built for Solutions Engineers who need a clean, repeatable demo environment that just works.

---

## Features

| Capability | Details |
|---|---|
| ⚡ Instant data generation | 50 customers, 20 products, 200 transactions seeded in < 1 second |
| 🏗️ Realistic SaaS data | Tiered pricing plans (Starter / Pro / Enterprise), product categories, dated transactions |
| 🌐 REST API | FastAPI server with `/build`, `/summary`, and `/reset` endpoints |
| ☁️ S3 integration | JSON report auto-uploaded to AWS S3 on every build |
| 🔁 CI/CD | GitHub Actions runs tests and triggers a live build + upload on every push to `main` |
| 🧹 One-command reset | Wipe and rebuild the environment without touching config |

---

## Quick Start

### Prerequisites
- Python 3.11+
- AWS credentials configured (`aws configure` or environment variables)

### Installation

```bash
git clone https://github.com/dunsworthdavid/demo-env-builder.git
cd demo-env-builder
pip install -r requirements.txt
```

### CLI Usage

```bash
# Generate a full demo environment
python cli.py build

# View a summary of the current environment
python cli.py summary

# Wipe the environment and start clean
python cli.py reset
```

**Example output:**
```
✅ Build complete.
  Customers:    50
  Products:     20
  Transactions: 200
  S3 report:    s3://demo-env-builder-dunsworth/demo_report.json
```

### API Usage

```bash
# Start the server
uvicorn api:app --reload
```

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/build` | Generates the demo environment and uploads to S3 |
| `GET` | `/summary` | Returns current record counts as JSON |
| `POST` | `/reset` | Wipes all data from the database |

**Example `/build` response:**
```json
{
  "status": "ok",
  "summary": {
    "customers": 50,
    "products": 20,
    "transactions": 200
  }
}
```

---

## Architecture

```
demo-env-builder/
├── data_generator.py      # Faker-powered data generation (customers, products, transactions)
├── cli.py                 # Click CLI — build / summary / reset commands
├── api.py                 # FastAPI server wrapping the CLI logic
├── s3_uploader.py         # boto3 uploader → s3://demo-env-builder-dunsworth/
├── demo.db                # SQLite database (gitignored)
├── demo_report.json       # Generated report artifact (gitignored)
├── tests/
│   ├── test_cli.py        # Unit tests for data generation and DB layer
│   └── test_api.py        # Integration tests for all FastAPI endpoints
└── .github/
    └── workflows/
        └── ci.yml         # GitHub Actions: test → build → S3 upload
```

**Data flow:**

```
cli.py build
    └── data_generator.py  →  SQLite (demo.db)
                           →  demo_report.json
                           →  s3_uploader.py  →  AWS S3
```

---

## CI/CD Pipeline

On every push to `main`, GitHub Actions:

1. **Installs dependencies** and runs the full test suite (`pytest` with coverage)
2. **Triggers a live demo build** using the CLI
3. **Uploads the generated report** to S3

AWS credentials are stored as GitHub repository secrets (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`). No credentials are committed to the repository.

---

## Running Tests

```bash
pip install pytest pytest-cov httpx
pytest tests/ -v --cov=. --cov-report=term-missing
```

The test suite covers:
- Data generator output shapes and validity
- CLI commands against a live SQLite database
- All three FastAPI endpoints, including edge cases (reset before build, double build, empty summary)

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `DB_PATH` | `demo.db` | SQLite database file path |
| `S3_BUCKET` | `demo-env-builder-dunsworth` | Target S3 bucket name |
| `AWS_DEFAULT_REGION` | `us-east-1` | AWS region |

---

## Roadmap

- [ ] `--customers`, `--products`, `--transactions` flags for custom volume
- [ ] Docker image for zero-install demo environments
- [ ] Webhook trigger: rebuild on Slack slash command
- [ ] Multi-tenant mode: isolated schemas per prospect/account

---

## Why This Exists

This project was built as a portfolio piece for Solutions Engineering roles, but reflects a real workflow problem. The best SE teams I've seen treat demo prep like engineering — repeatable, version-controlled, and fast. This is what that looks like in code.

---

## License

MIT © David Dunsworth# demo-env-builder
This is an application that will spin up and populate an envriorment with data to showcase capabilities to customers.
