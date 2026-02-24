import streamlit as st

st.title("Smart Exam Question Generator")

st.header("Upload Study Material")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

st.write("OR")

text_input = st.text_area("Paste your study text here")

if st.button("Generate Questions"):
    st.write("Button clicked. System ready.")