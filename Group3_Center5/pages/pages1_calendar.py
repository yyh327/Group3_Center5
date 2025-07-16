import streamlit as st
import streamlit.components.v1 as components
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle

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
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES,
                redirect_uri="https://group3center5-gnpekcrtfkawfet2ewfsi8.streamlit.app/pages1_calendar"
            )
            auth_url, _ = flow.authorization_url(prompt='consent')
            st.write("Please [authorize here](%s)" % auth_url)
            code = st.text_input("Enter the authorization code:")
            if code:
                flow.fetch_token(code=code)
                creds = flow.credentials
                save_token(creds)
    if creds:
        return build('calendar', 'v3', credentials=creds)
    return None

# Run authentication and get calendar list
service = get_calendar_service()
if service:
    st.success("Access granted to your Google Calendar!")
    calendars = service.calendarList().list().execute()
    for cal in calendars.get('items', []):
        st.write(f"**{cal['summary']}** — {cal['id']}")
