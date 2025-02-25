from celery import Celery
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Order
import time

celery = Celery("tasks", broker="redis://localhost:6379/0")

@celery.task
def process_order(order_id: int):
    """Background task to update order status."""
    db: Session = SessionLocal()
    
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return "Order not found"

        if order.status != "pending":
            order.status = "procesing"
            db.commit()

        # Simulate shipping process
        time.sleep(5)
        order.status = "shipped"
        db.commit()

        # Simulate delivery after some time
        time.sleep(5)
        order.status = "completed"
        db.commit()

        return f"Order {order_id} completed"
    
    finally:
        db.close()

@celery.task
def test_task():
    return "Hello from Celery!"