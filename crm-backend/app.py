from flask import Flask
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
import os
from flask import request
from services.ai_service import generate_campaign
from services.segment_service import find_customers
from services.campaign_service import (
    create_campaign,
    create_communications,
    send_to_channel_service,
    save_event,
    get_campaign_analytics,
    get_all_campaigns
)
from services.campaign_service import (
    save_event,
    get_campaign_analytics
)

load_dotenv()

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

@app.route("/customers")
def customers():
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM customers")

    data = cursor.fetchall()

    return data
@app.route("/ai/generate-campaign", methods=["POST"])
def ai_campaign():

    data = request.get_json()

    goal = data["goal"]

    result = generate_campaign(goal)

    customers = find_customers(
        result["category"],
        result["inactive_days"]
    )

    return {
        "campaign": result,
        "customer_count": len(customers),
        "sample_customers": customers[:5]
    }
@app.route("/campaigns/launch", methods=["POST"])
def launch_campaign():

    data = request.get_json()

    goal = data["goal"]

    campaign = generate_campaign(goal)

    customers = find_customers(
        campaign["category"],
        campaign["inactive_days"]
    )

    campaign_id = create_campaign(
        campaign["segment_name"],
        campaign["message"],
        campaign["channel"],
        len(customers)
    )

    create_communications(
        campaign_id,
        customers
    )
    send_to_channel_service(
    campaign_id,
    customers,
    campaign["message"],
    campaign["channel"]
)

    return {
        "campaign_id": campaign_id,
        "customer_count": len(customers),
        "status": "Campaign Created"
        
    }
@app.route("/receipt", methods=["POST"])
def receipt():

    data = request.get_json()

    print("CALLBACK RECEIVED")
    print(data)

    save_event(
        data["campaign_id"],
        data["event"]
    )

    return {
        "status": "received"
    }
@app.route("/campaigns/<int:campaign_id>/analytics")
def campaign_analytics(campaign_id):

    return get_campaign_analytics(campaign_id)
@app.route("/campaigns")
def campaigns():

    return get_all_campaigns()
import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )