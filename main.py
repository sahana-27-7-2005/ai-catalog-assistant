from fastapi import FastAPI, UploadFile, File
import os
import shutil
import json

from rag import csv_to_chunks, search_context
from llm import generate_answer

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

UPLOAD_FOLDER = "uploaded_catalogs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ FILE STORAGE
DATA_FILE = "products.json"

# 🔥 Load existing data
def load_products():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# 🔥 Save data
def save_products(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# 🧑‍💼 Load into memory
admin_products = load_products()

# ✅ MODEL
class Product(BaseModel):
    name: str
    price: str
    desc: str
    category: str
    amazon: str = ""
    flipkart: str = ""


# 🏠 Home
@app.get("/")
def home():
    return {"message": "AI Catalog Assistant API running 🚀"}


# 📁 Upload CSV
@app.post("/upload")
async def upload_catalog(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"{file.filename} uploaded successfully"}


# ❓ CSV MODE
@app.get("/ask")
def ask(question: str, filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return {"error": "File not found"}

    chunks = csv_to_chunks(file_path)
    context = search_context(chunks, question, top_k=20)
    answer = generate_answer(context, question)

    return {
        "question": question,
        "answer": answer,
        "mode": "csv"
    }


# 🔥 LIVE MODE
@app.get("/ask-live")
def ask_live(question: str):
    q = question.lower()

    if "shoe" in q:
        products = [
            "Nike Running Shoes ₹4000 - Lightweight running shoes",
            "Adidas Sneakers ₹3500 - Stylish casual shoes",
            "Puma Sports Shoes ₹3000 - Comfortable sports wear"
        ]
    elif "laptop" in q:
        products = [
            "Dell Inspiron ₹65000 - i5 laptop",
            "HP Pavilion ₹70000 - 16GB RAM",
            "Lenovo IdeaPad ₹55000 - Budget laptop"
        ]
    elif "mobile" in q or "phone" in q:
        products = [
            "iPhone 13 ₹60000 - Apple smartphone",
            "Samsung Galaxy S21 ₹50000 - Android flagship",
            "OnePlus Nord ₹30000 - Mid-range phone"
        ]
    else:
        products = [
            f"Top rated {question} ₹999 - Best item",
            f"Budget {question} ₹799 - Affordable",
            f"Premium {question} ₹1299 - High quality"
        ]

    return {
        "question": question,
        "answer": "\n".join(products),
        "mode": "live"
    }


# =========================
# 🧑‍💼 ADMIN (PERMANENT NOW)
# =========================

# ➕ ADD PRODUCT
@app.post("/admin/add-product")
def add_product(product: Product):
    data = product.dict()

    admin_products.append(data)
    save_products(admin_products)  # ✅ SAVE TO FILE

    return {
        "message": "Product added permanently ✅",
        "product": data
    }


# 📦 GET PRODUCTS
@app.get("/admin/products")
def get_products():
    return {"products": admin_products}


# 🔍 SEARCH ADMIN
@app.get("/ask-admin")
def ask_admin(question: str):
    q = question.lower()

    matched = [
        p for p in admin_products
        if p["category"].lower() in q or p["name"].lower() in q
    ]

    if matched:
        formatted = [
            f"{p['name']} ₹{p['price']} - {p['desc']}"
            for p in matched
        ]

        return {
            "question": question,
            "answer": "\n".join(formatted),
            "mode": "admin"
        }

    return {
        "question": question,
        "answer": "No admin products found",
        "mode": "admin"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)