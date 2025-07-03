import argparse
from tzlocal import get_localzone_name
from google_auth import get_google_services
from google_services import get_google_doc_content, get_google_sheet_content, create_calendar_event
from ai_event_extractor import extract_events_from_text

def main():
    """Main function to run the AI event scheduler."""
    parser = argparse.ArgumentParser(description="AI agent to extract events from Google Docs/Sheets and add them to Google Calendar.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--doc-id", help="The ID of the Google Doc to process.")
    group.add_argument("--sheet-id", help="The ID of the Google Sheet to process.")
    parser.add_argument("--calendar-id", default="primary", help="The ID of the calendar to add events to (default: 'primary').")
    
    args = parser.parse_args()

    print("🚀 Starting AI Event Scheduler...")

    try:
        user_timezone = get_localzone_name()
        print(f"🌍 Detected local timezone: {user_timezone}")
    except Exception:
        user_timezone = "UTC"
        print("⚠️ Could not detect local timezone. Defaulting to UTC.")
    
    services = get_google_services()
    if not services:
        return

    text_content = None
    if args.doc_id:
        text_content = get_google_doc_content(services["docs"], args.doc_id)
    elif args.sheet_id:
        text_content = get_google_sheet_content(services["sheets"], args.sheet_id)

    if not text_content or not text_content.strip():
        print("📄 No content found in the specified document/sheet. Exiting.")
        return

    extracted_events = extract_events_from_text(text_content)

    if not extracted_events:
        print("✅ No events found by the AI. All done!")
        return

    print(f"\n✨ Found {len(extracted_events)} potential event(s):")
    for i, event in enumerate(extracted_events, 1):
        print(f"--- Event {i} ---")
        print(f"  Title: {event.get('summary')}")
        print(f"  Start: {event.get('start_datetime')}")
        print(f"  End:   {event.get('end_datetime')}")
        print(f"  Desc:  {event.get('description')}")
    
    print("\n")
    for event in extracted_events:
        confirm = input(f"Create event '{event.get('summary')}' in your calendar? [y/N]: ").lower()
        if confirm == 'y':
            create_calendar_event(services["calendar"], args.calendar_id, event, user_timezone)
        else:
            print(f"Skipping event: '{event.get('summary')}'")

    print("\n🎉 Process complete.")

if __name__ == "__main__":
    main()