from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import models
from database import engine, get_db
from pydantic import BaseModel

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic 모델 정의
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    image_url: str
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    description: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# 상품 관련 API
@app.post("/products/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[Product])
def read_products(
    skip: int = 0,
    limit: int = 10,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)
    
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    if search:
        query = query.filter(models.Product.name.ilike(f"%{search}%"))
    
    return query.offset(skip).limit(limit).all()

@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다")
    return product

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다")
    
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다")
    
    db.delete(product)
    db.commit()
    return {"message": "상품이 삭제되었습니다"}

# 카테고리 관련 API
@app.post("/categories/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/categories/", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    return categories

# 메인 페이지용 API
@app.get("/main/featured-products/", response_model=List[Product])
def get_featured_products(db: Session = Depends(get_db)):
    # 예시: 최근 등록된 상품 중 활성화된 상품 8개 반환
    return db.query(models.Product)\
        .filter(models.Product.is_active == True)\
        .order_by(models.Product.created_at.desc())\
        .limit(8)\
        .all()

@app.get("/main/categories-with-products/")
def get_categories_with_products(db: Session = Depends(get_db)):
    # 각 카테고리별 대표 상품 4개씩 반환
    categories = db.query(models.Category).all()
    result = []
    
    for category in categories:
        products = db.query(models.Product)\
            .filter(models.Product.category_id == category.id)\
            .filter(models.Product.is_active == True)\
            .limit(4)\
            .all()
        
        result.append({
            "category": category,
            "products": products
        })
    
    return result

@app.get("/main/search/", response_model=List[Product])
def search_products(
    query: str,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    search_query = db.query(models.Product)\
        .filter(models.Product.name.ilike(f"%{query}%"))
    
    if category_id:
        search_query = search_query.filter(models.Product.category_id == category_id)
    if min_price is not None:
        search_query = search_query.filter(models.Product.price >= min_price)
    if max_price is not None:
        search_query = search_query.filter(models.Product.price <= max_price)
    
    return search_query.all()
