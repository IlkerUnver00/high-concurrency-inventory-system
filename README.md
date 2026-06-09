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

Client Request

↓

FastAPI Router

↓

Service Layer

↓

SQLAlchemy Async

↓

PostgreSQL

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

---

## Why Async SQLAlchemy?

The application is primarily I/O bound because requests spend most of their time waiting for database responses.

Using AsyncSession allows FastAPI to process more concurrent requests efficiently without blocking worker threads.

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

```bash
pytest
```

Current result:

```text
3 passed
```

---

## Concurrency Test

Run:

```bash
python load_concurrency.py
```

Example result:

```text
Successful purchases: 50
Failed purchases: 50
```

Validation:

* Initial stock: 50
* Created orders: 50
* Final stock: 0
* Overselling: No
* Negative stock: No

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

## Key Achievement

The system guarantees stock consistency under high concurrency by using PostgreSQL atomic conditional updates and transactional order creation.
