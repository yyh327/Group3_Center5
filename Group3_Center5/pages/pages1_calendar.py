import streamlit as st
import streamlit_calendar as st_calendar

st.set_page_config(page_title="Calendar")

st.markdown("Calendar")
st.sidebar.header("Calendar")

st.title("Calendar")
st.markdown(
    """ 
    Select a date on the calendar to view the availability of each classroom.
    Note: This calendar is for checking availability only — reservations cannot be made here.
     
    """
)

st_calendar.calendar()
