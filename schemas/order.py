from datetime import datetime
from pydantic import BaseModel,Field

class OrderItemCreate(BaseModel):
    product_id:int
    quantity:int = Field(gt=0)

class OrderCreate(BaseModel):
    customer_name: str = Field(max_length=100)
    item: list[OrderItemCreate] = Field(min_items=1)

class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    class config:
        from_attributes = True

class OrderResponse(BaseModel):
    id:int
    order_code:str
    customer_name:str
    total_amound:float
    status:str
    create_at:datetime
    item:list[OrderItemResponse]

    class config:
        from_attributes = True