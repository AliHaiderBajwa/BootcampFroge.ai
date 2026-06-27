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

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **"New app"** and select your repo.
4. Set the main file path to `src/app.py`.
5. Click **"Deploy"**.
6. Once deployed, go to **Settings → Secrets** and add:
   - `GEMINI_API_KEY` = your Gemini API key
7. The app will restart automatically with the secret set.

> **Note:** This app is designed for Streamlit Cloud. It is not compatible with Vercel's serverless runtime.
