# services/segment_service.py
import mysql.connector
from dotenv import load_dotenv
from datetime import date, timedelta
import os

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
from datetime import date, timedelta

def find_customers(category, inactive_days):

    cursor = db.cursor(dictionary=True)

    cutoff_date = date.today() - timedelta(days=inactive_days)

    query = """
    SELECT c.*
    FROM customers c

    JOIN (
        SELECT customer_id,
               MAX(order_date) as last_order
        FROM orders
        GROUP BY customer_id
    ) latest

    ON c.id = latest.customer_id

    WHERE latest.last_order < %s

    AND c.id IN (
        SELECT customer_id
        FROM orders
        WHERE category = %s
    )
    """

    cursor.execute(
        query,
        (cutoff_date, category)
    )

    return cursor.fetchall()