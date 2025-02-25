from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Order, Product, OrderItem
from app.schemas import CreateOrder
from app.database import get_db
from app.tasks import process_order


router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
def create_order(order: CreateOrder, db: Session = Depends(get_db)):
    total_price = 0.0
    items = []
    for item in order.products:
        product = db.query(Product).filter(Product.name == item.product_name).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_name} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {item.product_name}")
        product.stock -= item.quantity
        db.add(product)
        total_price += product.price * item.quantity
        items.append(OrderItem(product_id=product.id, quantity=item.quantity))

    new_order = Order(total_price=total_price, status="processing", items=items)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Asynchronously process the order
    process_order.delay(new_order.id)

    return {"order_id": new_order.id, "status": "processing"}

@router.post("/{order_id}/process")
def process_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "processing":
        raise HTTPException(status_code=400, detail="Order not in processing state")

    # Trigger Celery task
    process_order.delay(order_id)

    return {"message": f"Order {order_id} processing started"}

@router.get("/{order_id}/status")
def get_order_status(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order_id": order_id, "status": order.status}
