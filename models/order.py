from database import Base
from sqlalchemy import Column, Integer,String,DateTime,Float
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"

    id= Column(Integer,primary_key=True,autoincrement=True,index=True)
    order_code = Column(String(20),unique=True,nullable=False)
    customer_name = Column(String(100), nullable=False)
    total_amount = Column(Float, default=0.0)
    status = Column(String(20), default="PENDING")
    create_at = Column(DateTime, nullable=False)

    items = relationship(
    "OrderItem", back_populates="order", cascade="all, delete-orphan"
)