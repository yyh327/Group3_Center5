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

# --- Helpers ---------------------------------------------------------------
CLIENT_SECRETS_FILE = "/mount/src/group3_center5/Group3_Center5/pages/credentials.json"
TOKEN_FILE = "token.pkl"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Detect environment
IS_LOCAL = os.environ.get("STREAMLIT_SERVER_PORT") == "8501"
REDIRECT_URI = "http://localhost:8501/" if IS_LOCAL else "https://group3center5-gnpekcrtfkawfet2ewfsi8.streamlit.app/Calendar"

def safe_rerun():
    """Use the appropriate rerun API depending on Streamlit version."""
    try:
        st.rerun()  # preferred in newer versions. :contentReference[oaicite:3]{index=3}
    except AttributeError:
        try:
            st.experimental_rerun()
        except Exception:
            st.error("Cannot programmatically rerun; please manually refresh the page.")

def save_token(creds):
    with open(TOKEN_FILE, 'wb') as token:
        pickle.dump(creds, token)

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            return pickle.load(token)
    return None

def remove_query_params():
    # Remove the OAuth code from URL for cleanliness without full reload
    st.markdown("""
        <script>
        if (window.location.search.length > 0) {
            window.history.replaceState({}, document.title, window.location.pathname);
        }
        </script>
    """, unsafe_allow_html=True)

def get_calendar_service():
    creds = load_token()

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(prompt='consent')

    # NEW preferred API: query params available via property (deprecated experimental_get_query_params). :contentReference[oaicite:4]{index=4}
    query_params = st.query_params
    code = query_params.get("code", [None])[0]

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                save_token(creds)
            except Exception as e:
                st.warning("Failed to refresh credentials; reauthorization required.")
                creds = None
        elif code:
            try:
                flow.fetch_token(code=code)
                creds = flow.credentials
                save_token(creds)
