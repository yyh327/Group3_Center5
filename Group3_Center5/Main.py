import streamlit as st

# メインページのタイトル作成
st.title("Hello ISI Students 👋")

# 簡単な説明書き
st.markdown(
    """ 
    This is the intro page to our website for Center 5 Ito Campus for ISI students to check the availability of classrooms or class information!

    **👈 Select a tab from the dropdown on the left** to start exploring Center 5.

    **There's :rainbow[so much] you can explore!**
     
    """
)

# 風船を飛ばせるようにする
if st.button("Send balloons!"):
    st.balloons()