import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_campaign(goal):

    prompt = f"""
You are a marketing CRM assistant.

Convert the user's marketing goal into JSON.

Return ONLY valid JSON.

Available categories:
Shoes
Coffee
Beauty
Fashion
Electronics
Accessories
Skincare
Sports

Format:

{{
    "segment_name":"",
    "category":"",
    "inactive_days":0,
    "message":"",
    "channel":"WhatsApp"
}}

Goal:
{goal}
"""

    try:

        response = model.generate_content(prompt)

        text = response.text

        # Remove markdown if Gemini returns ```json
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        return json.loads(text)

    except Exception as e:

        print("GEMINI ERROR:", e)

        return {
            "segment_name": "Inactive Shoes Buyers",
            "category": "Shoes",
            "inactive_days": 90,
            "message": "We miss you! Come back and discover our latest shoe collection.",
            "channel": "WhatsApp"
        }