# Resume Analyzer

Streamlit-based resume analyzer that compares a PDF resume against a target role using either Google Gemini (`google-genai`) or local Ollama.

## Features

- Upload resume PDF and extract text.
- Analyze role fit with Gemini or Ollama.
- Get structured ATS-style feedback:
  - Match score
  - Strengths
  - Missing or weak areas
  - Improvement suggestions
  - Final verdict

## Tech Stack

- Python 3.10+
- Streamlit
- PyPDF2
- Google GenAI SDK (`google-genai`)
- LangChain + LangChain Ollama (`langchain`, `langchain-ollama`)

## Project Files

- `resume_analyzer1.py` - main Streamlit app
- `requirements.txt` - Python dependencies
- `requriement.txt` - compatibility copy of dependency list
- `smoke_test.py` - simple environment/config verification

## Quick Start

```powershell
cd D:\Resume-Analyzer-main
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requriement.txt
# or
pip install -r requirements.txt
```

If using Google Gemini, create API key variable (current terminal session):

```powershell
$env:GOOGLE_API_KEY="your_google_api_key"
```

Run app:

```powershell
streamlit run resume_analyzer1.py
```

In the UI, choose provider:

- `Google Gemini (API Key)` for cloud model access
- `Ollama Local (No API Key)` for local inference

## Configuration

For Google mode, the app reads `GOOGLE_API_KEY` from either:

1. Streamlit secrets (`.streamlit/secrets.toml`), or
2. Environment variable (`GOOGLE_API_KEY`)

Example `secrets.toml`:

```toml
GOOGLE_API_KEY = "your_google_api_key"
```

## Smoke Test

Run a quick check before starting Streamlit:

```powershell
python smoke_test.py
```

This checks dependency imports and whether `GOOGLE_API_KEY` is available.

If using Ollama mode, also ensure Ollama is installed locally and running, then pull a model (example):

```powershell
ollama pull mistral
```

## Notes

- Do not commit real API keys.
- Add `.env`, `.streamlit/secrets.toml`, and local virtual environment folders to `.gitignore`.
