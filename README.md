# High Concurrency Inventory System

Backend case study built with FastAPI and PostgreSQL.

## Scenario

This project simulates a flash sale event where many users attempt to purchase the same limited-stock product simultaneously.

The primary objective is to guarantee data consistency and prevent overselling under high concurrency.

---

## Tech Stack

* Python 3.12+
* FastAPI
* PostgreSQL
* SQLAlchemy Async
* Alembic
* Docker & Docker Compose
* Pytest
* HTTPX

---

## Architecture

```text
Client Request
      │
      ▼
FastAPI Router
      │
      ▼
Service Layer
      │
      ▼
SQLAlchemy Async
      │
      ▼
PostgreSQL
```

---

## Features

* High concurrency purchase endpoint
* Atomic stock decrement operation
* Order creation
* Health check endpoint
* Structured logging
* Dockerized deployment
* Database migrations with Alembic
* Automated tests with Pytest
* Async concurrency validation
* GitHub Actions CI pipeline

---

## API Endpoints

### GET /items

Returns all items and their current stock levels.

### POST /purchase/{item_id}

Attempts to purchase one unit of an item.

Success:

* Decreases stock by 1
* Creates an order record
* Returns remaining stock

Failure:

* Returns HTTP 409 Conflict when stock is unavailable

### GET /orders/count

Returns total number of created orders.

### GET /health

Health check endpoint.

---

## Concurrency Strategy

The purchase operation uses an Atomic Conditional Update in PostgreSQL:

```sql
UPDATE items
SET stock = stock - 1
WHERE id = :item_id
AND stock > 0
RETURNING id, stock;
```

This approach prevents race conditions by ensuring that stock validation and stock decrement occur within a single database operation.

### Why This Works

Instead of:

1. Reading stock
2. Checking stock
3. Updating stock

The application performs validation and update in a single SQL statement.

This guarantees:

* No race conditions
* No negative stock values
* No overselling
* Consistent order creation

---

## Why Async SQLAlchemy?

The application is primarily I/O bound because requests spend most of their time waiting for database responses.

Using AsyncSession allows FastAPI to process more concurrent requests efficiently without blocking worker threads.

### Benefits

* Better scalability
* Improved concurrency handling
* More efficient resource utilization

---

## Running the Project

### Prerequisites

* Docker Desktop (Windows/macOS) or Docker Engine (Linux)
* Docker Compose

Verify installation:

```bash
docker --version
docker compose version
```

### Clone Repository

```bash
git clone https://github.com/IlkerUnver00/high-concurrency-inventory-system.git
cd high-concurrency-inventory-system
```

### Start Application

Build and start all services:

```bash
docker compose up --build
```

The application automatically:

* Starts PostgreSQL
* Waits until the database is healthy
* Applies Alembic migrations
* Seeds the initial product
* Starts the FastAPI application

### API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

Health Check:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

## Running Tests

Open a second terminal while the application is running.

Run all tests:

```bash
docker compose exec api pytest -v
```

Expected result:

```text
========================
4 passed
========================
```

Included tests:

* Root endpoint validation
* Health endpoint validation
* API functionality validation
* High concurrency purchase validation

---

## Concurrency Validation

The project includes:

* Automated concurrency testing (`tests/test_concurrency.py`)
* Manual load testing (`load_concurrency.py`)

### Run Manual Load Test

```bash
docker compose exec api python load_concurrency.py
```

### Test Scenario

```text
Initial Stock      : 50
Concurrent Requests: 100
```

### Expected Result

```text
Successful purchases: 50
Failed purchases: 50
```

### Guaranteed Outcomes

```text
Remaining Stock    : 0
Successful Orders  : 50
Rejected Requests  : 50
Overselling        : No
Negative Stock     : No
```

This validates that the system preserves full database consistency under concurrent load.

---

## Database Migrations

Create migration:

```bash
alembic revision --autogenerate -m "message"
```

Apply migration:

```bash
alembic upgrade head
```

---

## Continuous Integration

GitHub Actions automatically:

* Starts PostgreSQL
* Runs Alembic migrations
* Starts the FastAPI application
* Executes the test suite

Every push and pull request to the `main` branch triggers the CI pipeline.

---

## Repository Structure

```text
app/
├── routers/
├── services/
├── models.py
├── schemas.py
├── database.py
└── main.py

tests/
├── test_basic.py
├── test_health.py
└── test_concurrency.py

alembic/
├── versions/

.github/
├── workflows/
│   └── ci.yml

Dockerfile
docker-compose.yml
alembic.ini
requirements.txt
load_concurrency.py
pytest.ini
README.md
```

---

## Key Achievement

The system guarantees stock consistency under high concurrency through PostgreSQL atomic conditional updates and transactional order creation.

The implementation has been validated through:

* Automated test suite (4 passing tests)
* Concurrent purchase stress testing
* GitHub Actions CI pipeline
* Clean Docker-based deployment

The application successfully prevents overselling while maintaining strict database consistency under concurrent load.
