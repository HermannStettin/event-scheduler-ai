import streamlit as st
from tzlocal import get_localzone_name
from google_auth import get_google_services
from google_services import get_google_doc_content, get_google_sheet_content, create_calendar_event
from ai_event_extractor import extract_events_from_text

# Set page title and icon
st.set_page_config(page_title="AI Event Scheduler", page_icon="🚀")

# Title and description
st.title("🚀 AI Event Scheduler")
st.markdown("""
Extract events from Google Docs/Sheets and add them to Google Calendar.
""")

# Initialize session state
if 'events' not in st.session_state:
    st.session_state.events = []
if 'processed' not in st.session_state:
    st.session_state.processed = False

# Get user timezone
try:
    user_timezone = get_localzone_name()
except Exception:
    user_timezone = "UTC"

# Sidebar for inputs
with st.sidebar:
    st.header("Configuration")
    input_type = st.radio("Select input type:", ("Google Doc", "Google Sheet"))

    doc_id = ""
    sheet_id = ""

    if input_type == "Google Doc":
        doc_id = st.text_input("Google Doc ID:", help="The document ID from the Google Docs URL")
    else:
        sheet_id = st.text_input("Google Sheet ID:", help="The spreadsheet ID from the Google Sheets URL")

    calendar_id = st.text_input("Calendar ID:", "primary",
                                help="Target calendar ID. 'primary' for your main calendar")

    process_btn = st.button("Process Document")

# Main processing logic
if process_btn:
    st.session_state.processed = False
    st.session_state.events = []

    if (input_type == "Google Doc" and not doc_id) or \
            (input_type == "Google Sheet" and not sheet_id):
        st.warning("Please provide a valid ID")
        st.stop()

    with st.spinner("Authenticating with Google..."):
        services = get_google_services()
        if not services:
            st.error("Failed to authenticate with Google. Please check your credentials.")
            st.stop()

    with st.spinner(f"Fetching content from {input_type}..."):
        text_content = None
        if input_type == "Google Doc":
            text_content = get_google_doc_content(services["docs"], doc_id)
        else:
            text_content = get_google_sheet_content(services["sheets"], sheet_id)

        if not text_content or not text_content.strip():
            st.error("No content found in the specified document/sheet.")
            st.stop()

    # Show raw content in expander
    with st.expander("View Raw Content"):
        st.code(text_content.strip())

    with st.spinner("AI is analyzing content for events..."):
        extracted_events = extract_events_from_text(text_content)
        st.session_state.events = extracted_events or []
        st.session_state.processed = True

# Show results if processing is complete
if st.session_state.processed:
    if not st.session_state.events:
        st.success("✅ No events found by the AI")
    else:
        st.subheader(f"✨ Found {len(st.session_state.events)} potential event(s)")

        # Display events and collect confirmation
        for i, event in enumerate(st.session_state.events):
            with st.container():
                st.markdown(f"### Event {i + 1}: {event.get('summary')}")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**Start:** `{event.get('start_datetime')}`")
                    st.markdown(f"**End:** `{event.get('end_datetime')}`")
                    if event.get('description'):
                        st.markdown(f"**Description:** {event.get('description')}")
                with col2:
                    event_key = f"create_{i}"
                    if st.button("Create Event", key=event_key):
                        with st.spinner(f"Creating '{event.get('summary')}'..."):
                            try:
                                create_calendar_event(
                                    services["calendar"],
                                    calendar_id,
                                    event,
                                    user_timezone
                                )
                                st.success(f"Event '{event.get('summary')}' created successfully!")
                            except Exception as e:
                                st.error(f"Failed to create event: {str(e)}")

                st.divider()

# Footer information
st.caption(f"Local timezone: {user_timezone}")