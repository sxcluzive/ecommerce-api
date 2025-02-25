from pydantic import BaseModel
from typing import List

class CreateProduct(BaseModel):
    name: str
    description: str
    price: float
    stock: int

class CreateOrderItem(BaseModel):
    product_name: str
    quantity: int

class CreateOrder(BaseModel):
    products: List[CreateOrderItem]

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int

    class Config:
        orm_mode = True 
