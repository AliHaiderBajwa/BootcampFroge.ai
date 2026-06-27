# Coding Bootcamp Builder

An AI-powered coding bootcamp curriculum builder using CrewAI and Gemini.

## Setup

1. Clone the repo and create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` (or use the existing `.env`) and add your Gemini API key:
   ```
   GEMINI_API_KEY=your-actual-key-here
   ```

## Run Locally

```bash
streamlit run src/app.py
```


> **Note:** This app is designed for Streamlit Cloud. It is not compatible with Vercel's serverless runtime.
