from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True,autoincrement=True,index=True)
    name = Column(String(50),unique=True,nullable=False)
    description = Column(String(255),nullable=True)

    products = relationship(
        "Products", back_populates="category", cascade="all, delete-orphan"
    )