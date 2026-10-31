from database import Base
from sqlalchemy import Column, Integer,String,ForeignKey,Float
from sqlalchemy.orm import relationship

class Products(Base):
    __tablename__ = "products"

    id= Column(Integer,primary_key=True,autoincrement=True,index=True)
    product_code = Column(String(10),unique=True,nullable=False)
    name = Column(String(100),nullable=False)
    price = Column(Float,nullable=False)
    stock_quantity = Column(Integer,default=0)
    category_id = Column(Integer,ForeignKey("categories.id"),nullable=False)

    category = relationship("Category", back_populates="products")

    order_items = relationship("OrderItem", back_populates="product")