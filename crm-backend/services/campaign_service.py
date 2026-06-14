import mysql.connector
from dotenv import load_dotenv
import os
import threading

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)


def ensure_connection():
    global db

    if not db.is_connected():
        db.reconnect()


def create_campaign(
    segment_name,
    message,
    channel,
    customer_count
):

    ensure_connection()

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO campaigns(
            segment_name,
            message,
            channel,
            customer_count
        )
        VALUES(%s,%s,%s,%s)
        """,
        (
            segment_name,
            message,
            channel,
            customer_count
        )
    )

    db.commit()

    return cursor.lastrowid


def create_communications(
    campaign_id,
    customers
):

    ensure_connection()

    cursor = db.cursor()

    for customer in customers:

        cursor.execute(
            """
            INSERT INTO communications(
                campaign_id,
                customer_id,
                status
            )
            VALUES(%s,%s,%s)
            """,
            (
                campaign_id,
                customer["id"],
                "pending"
            )
        )

    db.commit()


def send_to_channel_service(
    campaign_id,
    customers,
    message,
    channel
):

    from __main__ import send_callback

    threading.Thread(
        target=send_callback,
        args=(
            campaign_id,
            len(customers)
        )
    ).start()

    return {
        "status": "accepted"
    }


def save_event(
    campaign_id,
    event_type
):

    ensure_connection()

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO communication_events(
            communication_id,
            event_type
        )
        VALUES(%s,%s)
        """,
        (
            campaign_id,
            event_type
        )
    )

    db.commit()

    print(f"Saved event: {event_type}")


def get_campaign_analytics(campaign_id):

    ensure_connection()

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            event_type,
            COUNT(*) AS count
        FROM communication_events
        WHERE communication_id = %s
        GROUP BY event_type
        """,
        (campaign_id,)
    )

    events = cursor.fetchall()

    analytics = {
        "campaign_id": campaign_id,
        "delivered": 0,
        "opened": 0,
        "clicked": 0
    }

    for event in events:
        analytics[event["event_type"]] = event["count"]

    return analytics


def get_all_campaigns():

    ensure_connection()

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM campaigns
        ORDER BY id DESC
        """
    )

    return cursor.fetchall()