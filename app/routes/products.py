from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Product
from app.schemas import CreateProduct
from app.database import get_db
import logging
from typing import List

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[CreateProduct])
def get_products(db: Session = Depends(get_db)):
    try:
        products = db.query(Product).all()
        if not products:
            raise HTTPException(status_code=404, detail="No products found")
        logger.debug(f"Fetched products: {products}")
        return products
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
@router.post("/", response_model=CreateProduct)
def create_product(product: CreateProduct, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product