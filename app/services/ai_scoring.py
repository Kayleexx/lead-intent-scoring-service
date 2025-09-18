import os
import json
from dotenv import load_dotenv
from google.generativeai import Client

load_dotenv()  # Load .env

gemini_client = Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_ai_score(lead: dict, offer: dict) -> dict:
    """
    Sends lead + offer info to Gemini 2.5 Pro and returns intent + reasoning.
    """
    prompt = f"""
    You are a B2B sales assistant.
    Prospect info: {lead}
    Product/Offer info: {offer}

    Classify the buying intent as High, Medium, or Low.
    Explain in 1–2 sentences.
    Return JSON: {{ "intent": "<High/Medium/Low>", "reasoning": "<text>" }}
    """

    response = gemini_client.generate_text(
        model="gemini-2.5-pro",
        prompt=prompt,
        temperature=0.0
    )

    try:
        ai_result = json.loads(response.text)
        return ai_result
    except Exception:
        return {"intent": "Medium", "reasoning": "Could not parse AI response"}
