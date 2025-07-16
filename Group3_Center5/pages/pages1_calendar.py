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

components.iframe(
    "https://calendar.google.com/calendar/embed?src=ab02e25d2cbd99a78961c80f7fc34fc403f6372650bab1fcce7861e73704d2ea%40group.calendar.google.com&ctz=America%2FNew_York",
    width=1200, height=800, scrolling=True
)

# Google Calendar OAuth
CLIENT_SECRETS_FILE = "/mount/src/group3_center5/Group3_Center5/pages/credentials.json"
TOKEN_FILE = "token.pkl"
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

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
        redirect_uri="https://group3center5-gnpekcrtfkawfet2ewfsi8.streamlit.app/pages1_calendar"
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
            st.markdown(f"Please [authorize here]({auth_url})")
            st.stop()
    if creds:
        return build('calendar', 'v3', credentials=creds)
    return None

service = get_calendar_service()

if st.button("Logout"):
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    st.experimental_rerun()

if service:
    st.success("Access granted to your Google Calendar!")

    # Date selector
    selected_date = st.date_input("Select a date to view events", datetime.date.today())

    start_of_day = datetime.datetime.combine(selected_date, datetime.time.min).isoformat() + 'Z'
    end_of_day = datetime.datetime.combine(selected_date, datetime.time.max).isoformat() + 'Z'

    # UI columns
    calendars = service.calendarList().list().execute().get('items', [])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Your Calendars")
        for cal in calendars:
            st.write(cal['summary'])

    with col2:
        st.subheader(f"Events on {selected_date.strftime('%Y-%m-%d')}")
        events_result = service.events().list(
            calendarId='primary',
            timeMin=start_of_day,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        if not events:
            st.info("No events on this day.")
        else:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                st.write(f"**{event['summary']}**")
                st.write(f"Start: {start}")
                st.write(f"End: {end}")
                st.markdown("---")
