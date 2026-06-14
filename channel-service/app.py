from flask import Flask, request
import requests
import threading
import time

app = Flask(__name__)


import random

def send_callback(campaign_id, customer_count):

    for i in range(customer_count):

        requests.post(
            "http://127.0.0.1:5000/receipt",
            json={
                "campaign_id": campaign_id,
                "event": "delivered"
            }
        )

    opened_count = random.randint(
        int(customer_count * 0.5),
        int(customer_count * 0.8)
    )

    for i in range(opened_count):

        requests.post(
            "http://127.0.0.1:5000/receipt",
            json={
                "campaign_id": campaign_id,
                "event": "opened"
            }
        )

    clicked_count = random.randint(
        int(opened_count * 0.1),
        int(opened_count * 0.3)
    )

    for i in range(clicked_count):

        requests.post(
            "http://127.0.0.1:5000/receipt",
            json={
                "campaign_id": campaign_id,
                "event": "clicked"
            }
        )

@app.route("/send", methods=["POST"])
def send():

    print("REQUEST RECEIVED")

    data = request.get_json()

    print(data)

    threading.Thread(
        target=send_callback,
        args=(
    data["campaign_id"],
    data["customer_count"]
)
    ).start()

    return {
        "status": "accepted"
    }


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5001
    )