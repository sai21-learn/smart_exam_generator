# 📝 Smart Exam Question Generator

An AI-powered application that generates exam questions from study materials (PDF files or text). Built with Python, Streamlit, and Google Generative AI.

## 🚀 Features

- **PDF Text Extraction** - Upload PDF documents and extract text for question generation
- **AI-Powered Generation** - Uses Google's Gemini model to create relevant exam questions
- **Multiple Question Types** - Supports Multiple Choice, True/False, and Short Answer questions
- **Customizable Settings** - Choose number of questions and question types
- **Download Options** - Export generated questions as text files

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: Google Generative AI (Gemini)
- **PDF Processing**: pdfplumber
- **Language**: Python 3.x

## 📋 Requirements

```
streamlit>=1.30.0
google-generativeai>=0.8.0
pdfplumber>=0.11.0
python-dotenv>=1.0.0
```

## ⚡ Installation

1. **Clone the repository**
   ```bash
   cd smart_exam_generator
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API Key**

   Get your Google API key from: [Google AI Studio](https://aistudio.google.com/app/apikey)

   **Option A - Environment Variable**
   ```bash
   export GOOGLE_API_KEY=your_api_key_here
   ```

   **Option B - Streamlit Secrets**
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   # Edit secrets.toml and add your API key
   ```

## 🎯 Usage

1. **Run the application**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** to `http://localhost:8501`

3. **Generate Questions**
   - Upload a PDF file with study material, OR
   - Paste text directly into the text area
   - Configure number of questions and types in the sidebar
   - Click "Generate Questions" button
   - Download the generated questions

## 📖 How It Works

1. **Text Extraction**: The app extracts text from uploaded PDFs using pdfplumber
2. **AI Processing**: Sends the extracted text to Google's Gemini model with a carefully crafted prompt
3. **Question Generation**: AI generates relevant exam questions based on the study material
4. **Display & Download**: Shows questions in the UI and allows downloading as a text file

## 📝 Project Structure

```
smart_exam_generator/
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── readme.md              # This file
└── .streamlit/
    └── secrets.toml       # Configuration (create from template)
```

## ⚠️ Note

- The Google API key is required for question generation
- PDF text extraction quality depends on the PDF's formatting
- The app limits text to 4000 characters for API calls to manage costs

## 🤝 Contributing

Feel free to fork this project and add your own improvements!

## 📄 License

MIT License