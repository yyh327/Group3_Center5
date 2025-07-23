import streamlit as st
import streamlit.components.v1 as components
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle
import datetime
import pandas as pd

st.set_page_config(page_title="Calendar")

st.sidebar.header("Calendar")
st.title("Calendar")
st.markdown("""
    Select a date on the calendar to view the availability of each classroom.
    Note: This calendar is for checking availability only — reservations cannot be made here.
""")

# Google Calendar OAuth
CLIENT_SECRETS_FILE = "/mount/src/group3_center5/Group3_Center5/pages/credentials.json"
TOKEN_FILE = "token.pkl"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Detect local or deployed environment and set redirect_uri accordingly
IS_LOCAL = os.environ.get("STREAMLIT_SERVER_PORT") == "8501"
REDIRECT_URI = "http://localhost:8501/" if IS_LOCAL else "https://group3center5-gnpekcrtfkawfet2ewfsi8.streamlit.app/Calendar"

def save_token(creds):
    with open(TOKEN_FILE, 'wb') as token:
        pickle.dump(creds, token)

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            return pickle.load(token)
    return None

def get_calendar_service():
    creds = load_token()
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(prompt='consent')

    query_params = st.experimental_get_query_params()
    code = query_params.get("code", [None])[0]

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif code:
            flow.fetch_token(code=code)
            creds = flow.credentials
            save_token(creds)
            st.experimental_rerun()
        else:
            st.markdown(f"👉 Please [authorize here]({auth_url}) to access your Google Calendar.")
            st.stop()

    if creds:
        return build('calendar', 'v3', credentials=creds)
    return None

# Main logic
service = get_calendar_service()

# Logout button
if st.button("Logout"):
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    st.experimental_rerun()

# If authenticated
if service:
    st.success("✅ Access granted to your Google Calendar!")

    selected_date = st.date_input("📅 Select a date to view events", datetime.date.today())
    start_of_day = datetime.datetime.combine(selected_date, datetime.time.min).isoformat() + 'Z'
    end_of_day = datetime.datetime.combine(selected_date, datetime.time.max).isoformat() + 'Z'

    # Load calendars
    try:
        calendars = service.calendarList().list().execute().get('items', [])
    except Exception as e:
        st.error("❌ Failed to load calendar list:")
        st.exception(e)
        st.stop()

    col1, col2 = st.columns(2)

    # Show calendar names
    with col1:
        st.subheader("📘 Your Calendars")
        for cal in calendars:
            st.write(cal['summary'])

    # Show events from all calendars
    with col2:
        st.subheader(f"📆 Events on {selected_date.strftime('%Y-%m-%d')}")
        for cal in calendars:
            st.markdown(f"**📍 {cal['summary']}**")
            try:
                events_result = service.events().list(
                    calendarId=cal['id'],
                    timeMin=start_of_day,
                    timeMax=end_of_day,
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()
                events = events_result.get('items', [])
            except Exception as e:
                st.warning(f"Could not fetch events for {cal['summary']}.")
                st.exception(e)
                continue

            if not events:
                st.info("No events in this calendar.")
            else:
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    end = event['end'].get('dateTime', event['end'].get('date'))
                    title = event.get('summary', 'No title')
                    st.write(f"**{title}**")
                    st.write(f"🕒 Start: {start}")
                    st.write(f"🕓 End: {end}")
                    st.markdown("---")

    # Dropdown to select calendar to embed
    st.markdown("### 🔗 Embed One of Your Calendars")
    calendar_names = {cal['summary']: cal['id'] for cal in calendars}
    selected_cal_name = st.selectbox("Choose calendar to embed:", list(calendar_names.keys()))
    user_cal_id = calendar_names[selected_cal_name]

    embed_url = (
        "https://calendar.google.com/calendar/embed?"
        f"src={user_cal_id}&"
        "mode=week&showTitle=0&showPrint=0&showCalendars=0&showTz=0&"
        "ctz=America/New_York"
    )
    components.iframe(embed_url, width=900, height=700)
