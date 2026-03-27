from faker import Faker
import sqlite3
import random

fake = Faker()

# Connect to database
conn = sqlite3.connect("demo_env.db")
cursor = conn.cursor()

# Customers table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        company TEXT,
        phone TEXT
    )
""")

# Products table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        price REAL
    )
""")

# Transactions table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        total REAL,
        date TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
""")

# Seed customers
for _ in range(10):
    cursor.execute("INSERT INTO customers (name, email, company, phone) VALUES (?, ?, ?, ?)", (
        fake.name(),
        fake.email(),
        fake.company(),
        fake.phone_number()
    ))

# Seed products
products = [
    ("CRM Pro", "Software", 299.99),
    ("Analytics Suite", "Software", 499.99),
    ("Support Desk", "Software", 199.99),
    ("Data Connector", "Integration", 149.99),
    ("Security Pack", "Add-on", 99.99)
]
for product in products:
    cursor.execute("INSERT INTO products (name, category, price) VALUES (?, ?, ?)", product)

# Seed transactions
for _ in range(20):
    customer_id = random.randint(1, 10)
    product_id = random.randint(1, 5)
    quantity = random.randint(1, 5)
    price = products[product_id - 1][2]
    total = round(quantity * price, 2)
    cursor.execute("INSERT INTO transactions (customer_id, product_id, quantity, total, date) VALUES (?, ?, ?, ?, ?)", (
        customer_id,
        product_id,
        quantity,
        total,
        fake.date_this_year().isoformat()
    ))

conn.commit()
conn.close()

print("Demo environment created!")
print("- 10 customers")
print("- 5 products")
print("- 20 transactions")