from langchain.tools import tool
from pydantic import BaseModel, Field
from google_auth import get_google_services
from google_services import get_google_doc_content, get_google_sheet_content, create_calendar_event, get_google_sheet_page_names
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
def list_google_sheet_names_tool(spreadsheet_id: str) -> str:
    """
    Tool: Lists all sheet (tab) names in the specified Google Sheets document.

    Args:
        spreadsheet_id (str): The ID of the Google Sheets document.

    Returns:
        str: Comma-separated sheet names or error message.
    """
    try:
        service = get_google_services()["sheets"]
        spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheet_names = [sheet['properties']['title'] for sheet in spreadsheet.get('sheets', [])]
        return "✅ Sheet names: " + ", ".join(sheet_names)
    except Exception as e:
        return f"❌ Error listing sheet names: {e}"


@tool
def read_google_sheet(spreadsheet_id: str, sheet_name: str = None,
                                  sheet_range: str = "A1:Z100") -> str:
    """
    Tool: Reads content from a specified sheet and range in a Google Sheets document.

    Args:
        service: An authorized Sheets API service instance.
        spreadsheet_id (str): The ID of the Google Sheets document.
        sheet_name (str, optional): The name of the sheet/tab to read from.
        sheet_range (str, optional): The A1 notation range to read. Defaults to "A1:Z100".

    Returns:
        str: Text representation of the sheet content or an error message.
    """
    try:
        service = get_google_services()["sheets"]
        full_range = f"{sheet_name}!{sheet_range}" if sheet_name else sheet_range
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=full_range
        ).execute()
        values = result.get('values', [])
        if not values:
            return "⚠️ No data found in the specified range."

        return "📄 Sheet Content:\n" + "\n".join([" ".join(row) for row in values])
    except Exception as e:
        return f"❌ Error reading sheet content: {e}"


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
    list_google_sheet_names_tool,
    extract_events_from_document_text,
    add_event_to_calendar,
    create_new_google_calendar,
]