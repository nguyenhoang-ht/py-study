from pydantic import BaseModel,Field

class Standard(BaseModel):
    statusCode : int
    error: str | None = None
    message: str
    data: dict | list | None = None

class ProductCreate(BaseModel):
    product_code: str = Field(min_length=4,max_length=10)
    name: str = Field(min_length=2,max_length=100)
    price: float = Field(gt=0)
    stock_quantity: int = Field(gt=0)
    category_id : int

class ProductUpdate(BaseModel):
    price: float | None = None
    stock_quantity: int | None = None

class ProductResponse(BaseModel):
    id: int
    product_code : str
    name : str
    price : float
    stock_quantity: int
    category_id: int

    class Config:
        from_attributes = True