import streamlit as st
from streamlit_calendar import calendar

st.set_page_config(page_title="Calendar")

st.markdown("Calendar")
st.sidebar.header("Calendar")

st_calendar.calendar()
