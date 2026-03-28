from s3_uploader import upload_summary
import argparse
import sqlite3
import os
from data_generator import build_demo

def show_summary():
    conn = sqlite3.connect("demo_env.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
    customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products")
    products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions")
    transactions = cursor.fetchone()[0]

    conn.close()

    print("\n--- Demo Environment Summary ---")
    print(f"Customers:    {customers}")
    print(f"Products:     {products}")
    print(f"Transactions: {transactions}")
    print("--------------------------------\n")

def main():
    parser = argparse.ArgumentParser(description="Demo Environment Builder")
    parser.add_argument("command", choices=["build", "summary", "reset"], help="Command to run")
    args = parser.parse_args()

    if args.command == "build":
        print("Building demo environment...")
        build_demo()
        show_summary()
        summary_data = {
            "customers": 10,
            "products": 5,
            "transactions": 20
        }
        upload_summary(summary_data)

    elif args.command == "summary":
        show_summary()

    elif args.command == "reset":
        if os.path.exists("demo_env.db"):
            os.remove("demo_env.db")
            print("Demo environment reset. Run 'build' to create a fresh one.")
        else:
            print("No demo environment found.")

if __name__ == "__main__":
    main()