import streamlit as st
import streamlit_calendar as st_calendar

st.set_page_config(page_title="Calendar")

st.markdown("Calendar")
st.sidebar.header("Calendar")

st_calendar.calendar()
