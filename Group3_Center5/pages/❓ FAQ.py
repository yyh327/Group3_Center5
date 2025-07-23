import streamlit as st

st.set_page_config(page_title="FAQ")

st.sidebar.header("FAQ")
st.title("📝 Frequently Asked Questions (FAQ)")

st.markdown("""
Find answers to common questions about classroom use and this system.  
If you can’t find what you’re looking for, please contact us via the inquiry form below.
""")

# --- Sample FAQ data ---
faq_data = [
    {
        "question": "How can I check if a classroom is available?",
        "answer": "Use the 'Recommended Available Classroom' page and select the day and period to see the open classrooms."
    },
    {
        "question": "Can I search by teacher or class name?",
        "answer": "Yes. Use the 'Class Search' page to enter keywords such as the teacher's name or course title."
    },
    {
        "question": "What should I do if I find incorrect class information?",
        "answer": "Please use the contact form below to report the issue. We’ll investigate and correct it."
    },
]

# --- Search Box ---
search_query = st.text_input("🔎 Search FAQs (e.g. classroom, teacher, contact)")

# --- Display Matching FAQs ---
st.markdown("### 💡 Common Questions")

matched = [
    item for item in faq_data
    if search_query.lower() in item["question"].lower() or search_query.lower() in item["answer"].lower()
]

if search_query and not matched:
    st.warning("No matching FAQ found. Please try different keywords.")

for item in matched if search_query else faq_data:
    with st.expander(f"Q: {item['question']}"):
        st.markdown(f"A: {item['answer']}")

# --- Contact / Inquiry Form ---
st.markdown("---")
st.markdown("### 📬 Contact Us / お問い合わせ")

with st.form("contact_form"):
    name = st.text_input("Your Name / お名前")
    email = st.text_input("Email Address / メールアドレス")
    message = st.text_area("Your Message / お問い合わせ内容")

    submitted = st.form_submit_button("Send / 送信")

    if submitted:
        # Normally, you'd send this info to an email or database
        st.success("Thank you for your message. We'll get back to you shortly.")
