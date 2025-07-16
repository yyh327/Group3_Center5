import streamlit as st

st.title("Hello Fellow Students 👋")
st.markdown(
    """ 
    This is the intro page to our website for Center 5 Ito Campus for students to check the availability of each classrooms.

    **👈 Select a tab from the dropdown on the left** to start exploring Center 5.

    **There's :rainbow[so much] you can explore!**
     
    """
)

if st.button("Send balloons!"):
    st.balloons()