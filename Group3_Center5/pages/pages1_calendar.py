import streamlit as st
import streamlit_calendar as st_calendar
import streamlit.components.v1 as components

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

components.iframe(
    "https://calendar.google.com/calendar/embed?src=ab02e25d2cbd99a78961c80f7fc34fc403f6372650bab1fcce7861e73704d2ea%40group.calendar.google.com&ctz=America%2FNew_York",
    width=1200, height=800, scrolling=True
)
