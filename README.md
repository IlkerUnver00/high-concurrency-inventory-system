# High Concurrency Inventory System

Backend case study built with FastAPI and PostgreSQL.

## Scenario

This project simulates a flash sale event where thousands of users attempt to purchase the same limited-stock product simultaneously.

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

Benefits:

* Better scalability
* Improved concurrency handling
* More efficient resource utilization

---

## Running the Project

### Start PostgreSQL

```bash
docker compose up -d db
```

### Run API

```bash
uvicorn app.main:app --reload
```

### API Documentation

```text
http://localhost:8000/docs
```

---

## Running Tests

Run all tests:

```bash
pytest
```

Current result:

```text
4 passed
```

Included tests:

* Root endpoint
* Health endpoint
* Basic API functionality
* High concurrency purchase scenario

---

## Concurrency Test

The project includes both:

* Manual load testing (`load_concurrency.py`)
* Automated async concurrency testing (`tests/test_concurrency.py`)

Run automated concurrency test:

```bash
pytest tests/test_concurrency.py -v
```

### Test Scenario

```text
Initial Stock      : 100
Concurrent Requests: 500
```

### Expected Result

```text
Successful Purchases : 100
Rejected Purchases   : 400
Final Stock          : 0
Created Orders       : 100
Overselling          : No
Negative Stock       : No
```

### Example Execution

```text
tests/test_concurrency.py::test_high_concurrency_purchase PASSED
```

This verifies that the system maintains full data consistency under concurrent load.

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

Dockerfile
docker-compose.yml
alembic.ini
requirements.txt
README.md
```

---

## Key Achievement

The system guarantees stock consistency under high concurrency by using PostgreSQL atomic conditional updates and transactional order creation.

The implementation was validated through automated concurrency testing with 500 simultaneous purchase requests, successfully preventing overselling while maintaining database consistency.
