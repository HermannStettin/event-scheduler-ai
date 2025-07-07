import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/calendar",
]

def get_google_services():
    """
    Handles user authentication and builds service objects for Google APIs.
    Returns a dictionary of service objects for Calendar, Docs, and Sheets.
    """
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        calendar_service = build("calendar", "v3", credentials=creds)
        docs_service = build("docs", "v1", credentials=creds)
        sheets_service = build("sheets", "v4", credentials=creds)
        
        print("Successfully connected to Google services.")
        return {
            "calendar": calendar_service,
            "docs": docs_service,
            "sheets": sheets_service
        }
    except Exception as e:
        print(f"An error occurred while building Google services: {e}")
        return None