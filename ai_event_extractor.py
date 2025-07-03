import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import date

load_dotenv()

try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    print("✅ Gemini model initialized successfully.")
except Exception as e:
    print(f"❌ Error configuring Gemini API: {e}")
    model = None


def extract_events_from_text(text: str) -> list:
    """
    Uses Google's Gemini model to extract event details from a block of text.
    """
    if not model:
        print("❌ Gemini model is not available. Cannot extract events.")
        return []

    # Get today's date in a standard format (YYYY-MM-DD)
    today_str = date.today().isoformat()

    prompt = f"""
    Analyze the following text and extract any events mentioned. 
    For context, the current date is {today_str}. Use this date to resolve relative dates like 'tomorrow' or 'this Friday'.

    For each event, provide the following details:
    - summary: A concise title for the event.
    - start_datetime: The start date and time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS).
    - end_datetime: The end date and time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS).
    - description: A brief description of the event.

    Important Rules:
    1. If an end time is not specified, assume the event is one hour long.
    2. If a year is not specified, use the current year based on the context date provided above.
    3. Respond ONLY with a valid JSON array of event objects. Do not include any other text or markdown formatting like ```json. If no events are found, return an empty array [].

    Text to analyze:
    ---
    {text}
    ---
    """

    try:
        print("\n🤖 Sending text to Gemini for event extraction...")
        response = model.generate_content(prompt)
        response_content = response.text
        print("✅ Gemini analysis complete.")
        
        events = json.loads(response_content)
        return events

    except json.JSONDecodeError:
        print(f"❌ Error: Gemini returned invalid JSON. Response:\n{response_content}")
        return []
    except Exception as e:
        print(f"❌ An error occurred with the Gemini API: {e}")
        return []