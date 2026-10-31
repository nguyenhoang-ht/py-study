from database import engine, Base, get_db
from fastapi import FastAPI, status, Depends
from models import Category,Products,Order
from schemas.product import ProductCreate,ProductUpdate
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind = engine)

@app.get("/")
def root():
    return{"message": "you better fucking work"}

@app.get("/products/")
def get_product(
    category_id:int | None = None,
    search:str | None = None,
    db:Session = Depends(get_db)
):
    query = db.query(Products)

    if category_id is not None:
        query= query.filter(Products.category_id == category_id)

    if search is not None:
        search_keyword = f"%{search}%"
        query = query.filter(
            (Products.name.ilike(search_keyword))
            | (Products.product_code.ilike(search_keyword))
        )
    products = query.all()

    return{
        "status":200,
        "error":None,
        "message":"yay",
        "data":products
    }

@app.post("/products/",status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    category = (
        db.query(Category)
        .filter(Category.id == product_data.category_id).first()
    )
    if not category:
        return{
            "statusCode": 404,
            "error": "Not Found",
            "message": f"can't find : {product_data.category_id}",
            "data": None,
        }

    existing_product=(
        db.query(Products)
        .filter(Products.product_code == product_data.product_code).first()
    )
    if existing_product:
        return{
            "statusCode": 400,
            "error": "Bad Request",
            "message": f"already exist : {product_data.product_code}",
            "data": None,
        }

    new_product = Products(
        product_code=product_data.product_code,
        name=product_data.name,
        price=product_data.price,
        stock_quantity=product_data.stock_quantity,
        category_id=product_data.category_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return{
        "statusCode": 200,
        "error": None,
        "message": "success",
        "data": new_product,
    }

@app.put("/products/{id}")
def update_product(
    id:int,product_data: ProductUpdate, db: Session = Depends(get_db)
):
    product = db.query(Products).filter(Products.id == id).first()

    if not product:
        return {
        "statusCode": 404,
        "error": "Not Found",
        "message": f"Không tìm thấy sản phẩm có ID = {id}",
        "data": None,
    }
    if product_data.price is not None:
        product.price = product_data.price
    if product_data.stock_quantity is not None:
        product.stock_quantity = product_data.stock_quantity

    db.commit()
    db.refresh(product)
    return {
        "statusCode": 404,
        "error": None,
        "message": "yay",
        "data": product,
    }

@app.get("/orders/")
def get_orders(db: Session = Depends(get_db)):
  orders = db.query(Order).all()

  return {
      "statusCode": 200,
      "error": None,
      "message": "Lấy danh sách đơn hàng thành công",
      "data": orders,
  }

@app.delete("/categories/{id}")
def delete_category(id:int,db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == id).first()

    if not category:
        return {
        "statusCode": 404,
        "error": "Not Found",
        "message": f"Không tìm thấy danh mục có ID = {id}",
        "data": None,
    }

    products_in_category = (
        db.query(Products).filter(Products.category_id == id).all()
    )
    if len(products_in_category) > 0:
        if len(products_in_category) > 0:
            return {
                "statusCode": 400,
                "error": "Bad Request",
                "message": (
                    "Không thể xóa danh mục vì vẫn còn sản phẩm liên kết bên trong!"
                ),
                "data": None,
            }
    db.delete(category)
    db.commit()

    return {
      "statusCode": 200,
      "error": None,
      "message": "Xóa danh mục thành công",
      "data": None,
  }
