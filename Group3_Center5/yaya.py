import streamlit as st

st.title("Hello Streamlit-er 👋")
st.markdown(
    """ 
    This is the intro page to our website for Center 5 Ito Campus for students to have fun. 

    **There's :rainbow[so much] you can build!**
     
    """
)

if st.button("Send balloons!"):
    st.balloons()