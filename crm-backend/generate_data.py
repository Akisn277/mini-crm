from datetime import date, timedelta
from dotenv import load_dotenv
import mysql.connector
import random
import os

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor()

# Categories customers can buy from
categories = [
    "Shoes",
    "Coffee",
    "Beauty",
    "Fashion"
]

# Get all customer IDs
cursor.execute("SELECT id FROM customers")
customers = cursor.fetchall()

# Generate 5000 orders
for _ in range(5000):

    customer_id = random.choice(customers)[0]

    amount = random.randint(200, 5000)

    category = random.choice(categories)

    days_ago = random.randint(1, 365)

    order_date = date.today() - timedelta(days=days_ago)

    cursor.execute(
        """
        INSERT INTO orders(
            customer_id,
            amount,
            category,
            order_date
        )
        VALUES(%s,%s,%s,%s)
        """,
        (
            customer_id,
            amount,
            category,
            order_date
        )
    )

db.commit()

print("5000 Orders Added!")

cursor.close()
db.close()