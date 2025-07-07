import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import date

load_dotenv()

try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    print("✅ Gemini model initialized successfully.")
except Exception as e:
    print(f"❌ Error configuring Gemini API: {e}")
    model = None


def extract_events_from_text(text: str, user_query: str) -> list:
    """
    Uses Google's Gemini model to extract event details from a block of text.
    """
    if not model:
        print("❌ Gemini model is not available. Cannot extract events.")
        return []

    today_str = date.today().isoformat()
    prompt = f"""
    For context, the current date is {today_str}.
    Analyze the following text to find events that match the user's request: "{user_query}".

    For each matching event, provide:
    - summary: A concise title.
    - start_datetime: The start time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS).
    - end_datetime: The end time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS).
    - description: A brief description.

    Rules:
    1. If an end time is not specified, assume a one-hour duration.
    2. If a year is not specified, use the current year based on the context date.
    3. Respond ONLY with a valid JSON array of event objects. If no events are found, return an empty array [].

    Text to analyze:
    ---
    {text}
    ---
    """

    try:
        response = model.generate_content(prompt)
        response_content = response.text
        print("✅ Gemini analysis complete.")

        if "```json" in response_content:
            cleaned_response = response_content.split("```json")[1].split("```")[0].strip()
        elif "```" in response_content:
            cleaned_response = response_content.split("```")[1].strip()
        else:
            cleaned_response = response_content.strip()
        
        parsed_events = json.loads(cleaned_response)
        return parsed_events

    except json.JSONDecodeError:
        print(f"❌ Error: Gemini returned invalid JSON. Response:\n{response_content}")
        return []
    except Exception as e:
        print(f"❌ An error occurred with the Gemini API: {e}")
        return []