from fastapi import FastAPI
from data_generator import build_demo
from s3_uploader import upload_summary
import sqlite3

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Demo Environment Builder API is running"}

@app.post("/build")
def build():
    build_demo()
    summary_data = {
        "customers": 10,
        "products": 5,
        "transactions": 20
    }
    filename = upload_summary(summary_data)
    return {
        "status": "success",
        "message": "Demo environment built successfully",
        "report": filename
    }

@app.get("/summary")
def summary():
    conn = sqlite3.connect("demo_env.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
    customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products")
    products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions")
    transactions = cursor.fetchone()[0]

    conn.close()

    return {
        "customers": customers,
        "products": products,
        "transactions": transactions
    }

@app.delete("/reset")
def reset():
    import os
    if os.path.exists("demo_env.db"):
        os.remove("demo_env.db")
        return {"status": "success", "message": "Demo environment reset"}
    return {"status": "error", "message": "No demo environment found"}
