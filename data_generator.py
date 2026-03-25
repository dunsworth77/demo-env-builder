from faker import Faker
import sqlite3

fake = Faker()

# Create and connect to a local database
conn = sqlite3.connect("demo_env.db")
cursor = conn.cursor()

# Create a customers table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        company TEXT,
        phone TEXT
    )
""")

# Generate 10 fake customers
for _ in range(10):
    cursor.execute("INSERT INTO customers (name, email, company, phone) VALUES (?, ?, ?, ?)", (
        fake.name(),
        fake.email(),
        fake.company(),
        fake.phone_number()
    ))

conn.commit()
conn.close()

print("Demo environment created with 10 sample customers!")