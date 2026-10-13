from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ In-memory DB
products_db = []

# ✅ REQUEST MODEL (IMPORTANT)
class Product(BaseModel):
    name: str
    price: str
    desc: str
    category: str
    amazon: str = ""
    flipkart: str = ""

# ✅ ADD PRODUCT (POST FIXED)
@app.post("/admin/add-product")
def add_product(product: Product):
    products_db.append(product.dict())
    return {"message": "Product Added ✅"}

# ✅ GET PRODUCTS
@app.get("/admin/products")
def get_products():
    return {"products": products_db}