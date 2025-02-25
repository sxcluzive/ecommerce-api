# FastAPI E-commerce API

## Overview
This project is a **FastAPI-based E-commerce API** that manages products, orders, and order processing using **PostgreSQL**, **SQLAlchemy**, **Celery**, and **Redis**. The application provides endpoints for creating orders, checking order status, and processing them asynchronously.

## Project Structure
```
Ecommerce_API/
│-- app/
│   │-- __init__.py
│   │-- main.py         # FastAPI app entry point
│   │-- database.py     # Database setup and connection
│   │-- models.py       # SQLAlchemy ORM models
│   │-- schemas.py      # Pydantic schemas
│   │-- routes/
│   │   │-- products.py  # Product-related endpoints
│   │   │-- orders.py    # Order-related endpoints
│   │-- tasks.py        # Celery tasks for async processing
│-- requirements.txt
│-- Dockerfile
│-- docker-compose.yml
│-- README.md
```

## Installation & Setup
### 1 Clone the Repository
```bash
git clone https://github.com/your-repo/ecommerce-api.git
cd ecommerce-api
```
### 2 Set Up Virtual Environment (Optional)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application
### 1 Start PostgreSQL & Redis (Using Docker)
```bash
docker-compose up -d
```
### 2️ Run Database Migrations
```bash
alembic upgrade head
```
### 3️ Start FastAPI Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
### 4️ Start Celery Worker
```bash
celery -A app.tasks worker --loglevel=info
```

## API Endpoints
### Product Endpoints
| Method | Endpoint       | Description          |
|--------|--------------|----------------------|
| GET    | `/products/`  | Get all products    |
| POST   | `/products/`  | Add a new product   |

### Order Endpoints
| Method | Endpoint            | Description                    |
|--------|---------------------|--------------------------------|
| POST   | `/orders/`          | Create a new order            |
| GET    | `/orders/{id}/status` | Get order status              |
| POST   | `/orders/{id}/process` | Process an order asynchronously |

##  Database Models
- **Product** (`id`, `name`, `price`, `stock`)
- **Order** (`id`, `total_price`, `status`)
- **OrderItem** (`id`, `order_id`, `product_id`, `quantity`)

##  Troubleshooting
### Order Not Processing?
- Ensure Celery is running: `celery -A app.tasks worker --loglevel=info`
- Check Redis connection: `redis-cli ping`
- Verify database connection: `docker exec -it postgres_db psql -U user -d ecommerce_db`

###  Reset Orders
To delete all orders and reset data:
```sql
DELETE FROM order_items;
DELETE FROM orders;
ALTER SEQUENCE orders_id_seq RESTART WITH 1;
```

## Future Enhancements
- ✅ Add authentication & authorization
- ✅ Implement payment gateway integration
- ✅ Improve error handling & logging


