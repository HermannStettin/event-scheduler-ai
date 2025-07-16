def get_google_doc_content(service, document_id: str) -> str:
    """Reads and returns the text content of a Google Doc."""
    try:
        print(f"📄 Reading content from Google Doc ID: {document_id}")
        doc = service.documents().get(documentId=document_id).execute()
        content = doc.get('body').get('content')
        
        text = ""
        for value in content:
            if 'paragraph' in value:
                elements = value.get('paragraph').get('elements')
                for elem in elements:
                    text += elem.get('textRun', {}).get('content', '')
        return text
    except Exception as e:
        print(f"❌ Error reading Google Doc: {e}")
        return None


def get_google_sheet_page_names(service, spreadsheet_id: str) -> list:
    """Returns the names of all sheets/pages in a Google Spreadsheet.

    Args:
        service: Google Sheets API service object
        spreadsheet_id: ID of the spreadsheet to inspect

    Returns:
        List of sheet names (empty list on error)
    """
    try:
        print(f"📑 Fetching sheet names from Google Sheet ID: {spreadsheet_id}")
        spreadsheet = service.spreadsheets().get(
            spreadsheetId=spreadsheet_id
        ).execute()

        sheet_names = [
            sheet['properties']['title']
            for sheet in spreadsheet.get('sheets', [])
        ]

        print(f"✅ Found {len(sheet_names)} sheets: {', '.join(sheet_names)}")
        return sheet_names

    except Exception as e:
        print(f"❌ Error fetching sheet names: {e}")
        return []


def get_google_sheet_content(service, spreadsheet_id: str, sheet_name: str = None, sheet_range: str = "A1:Z100") -> str:
    """Reads and returns the content of a Google Sheet as a single string."""
    try:
        print(f"📊 Reading content from Google Sheet ID: {spreadsheet_id}")
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=((sheet_name + "!") if sheet_name is not None else "") + sheet_range
        ).execute()
        values = result.get('values', [])
        
        text = "\n".join([" ".join(row) for row in values])
        return text
    except Exception as e:
        print(f"❌ Error reading Google Sheet: {e}")
        return None

def create_calendar_event(service, calendar_id: str, event_data: dict, timezone: str):
    """Creates an event in the specified Google Calendar using the provided timezone."""
    event_body = {
        'summary': event_data.get('summary'),
        'description': event_data.get('description'),
        'start': {
            'dateTime': event_data.get('start_datetime'),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': event_data.get('end_datetime'),
            'timeZone': timezone,
        },
    }
    
    try:
        event = service.events().insert(
            calendarId=calendar_id, body=event_body
        ).execute()
        print(f"✅ Event created in timezone {timezone}: {event.get('summary')} -> {event.get('htmlLink')}")
    except Exception as e:
        print(f"❌ Error creating calendar event: {e}")