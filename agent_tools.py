from langchain.tools import tool
from pydantic import BaseModel, Field
from google_auth import get_google_services
from google_services import get_google_doc_content, get_google_sheet_content, create_calendar_event
from ai_event_extractor import extract_events_from_text
from tzlocal import get_localzone_name

class ExtractEventsInput(BaseModel):
    text_content: str = Field(description="The large block of text read from a document or sheet.")
    user_query: str = Field(description="The user's original request or question, used to focus the search for specific events.")

@tool(args_schema=ExtractEventsInput)
def extract_events_from_document_text(text_content: str, user_query: str) -> str:
    """
    Analyzes a large block of text from a document to find events that match a user's query.
    Use this tool first to get structured event data (summary, start/end times, description) from unstructured text.
    The output of this tool is a JSON string that can be used by other tools.
    """
    print(f"🤖 Agent is using extract_events_from_document_text tool...")
    
    events = extract_events_from_text(text_content, user_query) 
    if not events:
        return "No matching events were found in the text."
    
    import json
    return json.dumps(events)

@tool
def add_event_to_calendar(summary: str, start_datetime: str, end_datetime: str, description: str, calendar_id: str = "primary") -> str:
    """
    Adds a single, specific event to a Google Calendar.
    Use this tool for each individual event you need to schedule.
    Requires precise event details: summary, start_datetime, end_datetime (in ISO 8601 format), and an optional calendar_id.
    """
    print(f"🤖 Agent is using add_event_to_calendar tool for calendar: '{calendar_id}'")
    services = get_google_services()
    user_timezone = get_localzone_name()
    if not services:
        return "Error: Could not connect to Google services."

    event_data = {
        "summary": summary,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "description": description
    }
    
    try:
        create_calendar_event(services["calendar"], calendar_id, event_data, user_timezone)
        return f"Successfully created event '{summary}' in calendar '{calendar_id}'."
    except Exception as e:
        return f"Error creating event '{summary}': {e}"

@tool
def read_google_doc(document_id: str) -> str:
    """
    Reads the text content from a Google Doc given its ID. 
    Use this to get the raw text from a document before analyzing it.
    """
    print(f"🤖 Agent is using read_google_doc tool for doc ID: {document_id}")
    services = get_google_services()
    if not services:
        return "Error: Could not connect to Google services."
    return get_google_doc_content(services["docs"], document_id)

@tool
def read_google_sheet(spreadsheet_id: str) -> str:
    """
    Reads the text content from a Google Sheet given its ID.
    Use this to get the raw text from a spreadsheet before analyzing it.
    """
    print(f"🤖 Agent is using read_google_sheet tool for sheet ID: {spreadsheet_id}")
    services = get_google_services()
    if not services:
        return "Error: Could not connect to Google services."
    return get_google_sheet_content(services["sheets"], spreadsheet_id)

@tool
def create_new_google_calendar(calendar_name: str) -> str:
    """
    Creates a new Google Calendar with the specified name. 
    Use this when the user asks to create a new, separate calendar.
    Returns a confirmation message with the new calendar's ID.
    """
    print(f"🤖 Agent is using create_new_google_calendar tool to create '{calendar_name}'")
    services = get_google_services()
    if not services:
        return "Error: Could not connect to Google services."
    
    user_timezone = get_localzone_name()
    calendar_body = {
        'summary': calendar_name,
        'timeZone': user_timezone
    }
    
    try:
        created_calendar = services["calendar"].calendars().insert(body=calendar_body).execute()
        calendar_id = created_calendar['id']
        return f"Successfully created new calendar '{calendar_name}' with ID: {calendar_id}"
    except Exception as e:
        return f"Error creating new calendar: {e}"

all_tools = [
    read_google_doc,
    read_google_sheet,
    extract_events_from_document_text,
    add_event_to_calendar,
    create_new_google_calendar,
]