import os
from io import StringIO

import google.generativeai as genai
import pdfplumber
import streamlit as st


# Configure Google Generative AI
# You can set the API key via environment variable or Streamlit secrets
def configure_genai():
    """Configure Google Generative AI with API key."""
    api_key = os.environ.get("GOOGLE_API_KEY")

    # Check if API key is in Streamlit secrets
    try:
        if "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        pass

    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False


def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        st.error(f"Error extracting PDF: {str(e)}")
        return None


def generate_questions(text, num_questions=5, question_types=None):
    """Generate exam questions from text using Google Generative AI."""
    if question_types is None:
        question_types = ["Multiple Choice", "True/False", "Short Answer"]

    if not text or len(text.strip()) < 50:
        return (
            None,
            "Text is too short to generate questions. Please provide more content.",
        )

    try:
        # Build the prompt for question generation
        question_types_str = ", ".join(question_types)
        prompt = f"""Based on the following study material, generate {num_questions} exam questions.
Include these types: {question_types_str}.

Study Material:
{text[:4000]}

Generate questions that test understanding of the key concepts in the material.
For Multiple Choice questions, provide 4 options (A, B, C, D) and indicate the correct answer.
For True/False questions, indicate whether the statement is True or False.
For Short Answer questions, provide a brief answer key.

Format the output as follows:
---
## Multiple Choice Questions
1. [Question text]
   A. [Option A]
   B. [Option B]
   C. [Option C]
   D. [Option D]
   Correct Answer: [A/B/C/D]

## True/False Questions
1. [Statement]
   Answer: [True/False]

## Short Answer Questions
1. [Question]
   Answer: [Brief answer]
---
"""

        # Use Gemini model to generate questions
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        return response.text, None

    except Exception as e:
        return None, f"Error generating questions: {str(e)}"


def main():
    st.set_page_config(
        page_title="Smart Exam Question Generator", page_icon="📝", layout="wide"
    )

    # Sidebar for settings
    st.sidebar.title("⚙️ Settings")

    # Configure API
    api_configured = configure_genai()

    if not api_configured:
        st.sidebar.warning("⚠️ API Key Not Configured")
        st.sidebar.info("""
        To use this app, you need to set up your Google API Key:

        **Option 1:** Set environment variable
        ```bash
        export GOOGLE_API_KEY=your_api_key_here
        ```

        **Option 2:** Add to Streamlit secrets
        Create `.streamlit/secrets.toml`:
        ```toml
        GOOGLE_API_KEY = "your_api_key_here"
        ```

        Get your API key from: https://aistudio.google.com/app/apikey
        """)

    # Main content
    st.title("📝 Smart Exam Question Generator")
    st.markdown("""
    Upload your study material (PDF or text) and generate practice exam questions using AI.
    """)

    # Number of questions slider
    num_questions = st.sidebar.slider("Number of Questions", 3, 20, 5)

    # Question types selection
    st.sidebar.subheader("Question Types")
    use_mcq = st.sidebar.checkbox("Multiple Choice", value=True)
    use_tf = st.sidebar.checkbox("True/False", value=True)
    use_short = st.sidebar.checkbox("Short Answer", value=True)

    question_types = []
    if use_mcq:
        question_types.append("Multiple Choice")
    if use_tf:
        question_types.append("True/False")
    if use_short:
        question_types.append("Short Answer")

    if not question_types:
        st.sidebar.error("Please select at least one question type")
        question_types = ["Multiple Choice"]

    # Input section
    st.header("📚 Upload Study Material")

    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
        if uploaded_file:
            st.success(f"✅ Uploaded: {uploaded_file.name}")

    with col2:
        st.write("**OR**")
        text_input = st.text_area(
            "Paste your study text here",
            height=200,
            placeholder="Enter your study material text here...",
        )

    # Extract text from PDF if uploaded
    extracted_text = ""
    if uploaded_file and text_input:
        st.info("Both PDF and text provided. Using PDF content.")
        extracted_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file:
        with st.spinner("Extracting text from PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)
    elif text_input:
        extracted_text = text_input

    # Show text preview
    if extracted_text:
        with st.expander("📄 View Extracted Text"):
            st.text(
                extracted_text[:1000] + "..."
                if len(extracted_text) > 1000
                else extracted_text
            )

    # Generate questions button
    st.header("🎯 Generate Questions")

    if st.button("Generate Questions", type="primary", use_container_width=True):
        if not api_configured:
            st.error("Please configure your Google API Key first!")
            return

        if not extracted_text or len(extracted_text.strip()) < 50:
            st.error(
                "Please provide more content (at least 50 characters) to generate questions."
            )
            return

        with st.spinner("🤖 Generating questions... This may take a moment."):
            questions, error = generate_questions(
                extracted_text, num_questions, question_types
            )

            if error:
                st.error(error)
            else:
                st.success("✅ Questions Generated Successfully!")

                # Display questions
                st.markdown("---")
                st.header("📋 Generated Questions")
                st.markdown(questions)

                # Download button
                st.download_button(
                    label="📥 Download Questions",
                    data=questions,
                    file_name="generated_questions.txt",
                    mime="text/plain",
                )

    # Add some helpful information
    st.markdown("---")
    st.markdown("""
    ### How to use:
    1. **Upload PDF** - Upload a PDF document with your study material
    2. **Or paste text** - Copy and paste text directly into the text area
    3. **Configure settings** - Choose number of questions and types in the sidebar
    4. **Generate** - Click the button to generate AI-powered questions
    5. **Download** - Download your questions for later use

    ### Features:
    - 📄 PDF text extraction
    - 🤖 AI-powered question generation
    - 📝 Multiple question types (MCQ, True/False, Short Answer)
    - ⬇️ Download questions as text file
    """)


if __name__ == "__main__":
    main()
