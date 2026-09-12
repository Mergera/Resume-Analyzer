import os
from typing import Optional

import PyPDF2
import streamlit as st
from google import genai
from dotenv import load_dotenv


load_dotenv()


def get_api_key() -> Optional[str]:
    """Read API key from Streamlit secrets first, then environment variables."""
    if "GOOGLE_API_KEY" in st.secrets:
        return st.secrets["GOOGLE_API_KEY"]
    return os.getenv("GOOGLE_API_KEY")


def extract_resume_text(uploaded_file) -> str:
    """Extract plain text from uploaded PDF and handle empty pages safely."""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    page_text = []
    for page in pdf_reader.pages:
        page_text.append(page.extract_text() or "")
    return "\n".join(page_text).strip()


def build_prompt(resume_text: str, role: str) -> str:
    return f"""You are an expert ATS resume reviewer.

Analyze the following resume for the role: {role}

Return your response in this format:
1) Match Score (0-100)
2) Key Strengths (bullet points)
3) Missing or Weak Areas (bullet points)
4) Recommended Improvements (bullet points)
5) Final Verdict (2-3 lines)

Resume:
{resume_text}
"""


def analyze_resume(client: genai.Client, model_name: str, resume_text: str, role: str) -> str:
    prompt = build_prompt(resume_text=resume_text, role=role)
    response = client.models.generate_content(model=model_name, contents=prompt)
    return response.text or "Model returned an empty response."


def analyze_resume_ollama(model_name: str, resume_text: str, role: str) -> str:
    """Run analysis with local Ollama through LangChain when API keys are not desired."""
    try:
        from langchain_ollama import OllamaLLM
    except Exception as exc:
        raise RuntimeError(
            "langchain-ollama is not installed. Install requirements or switch provider."
        ) from exc

    llm = OllamaLLM(model=model_name, temperature=0.2)
    prompt = build_prompt(resume_text=resume_text, role=role)
    result = llm.invoke(prompt)
    return result if isinstance(result, str) else str(result)


st.set_page_config(page_title="Resume Analyzer", page_icon="📄")
st.title("📄 Resume Analyzer")
st.write("Upload a resume PDF and get AI insights with Gemini API or local Ollama.")

provider = st.selectbox(
    "AI provider",
    options=["Google Gemini (API Key)", "Ollama Local (No API Key)"],
)

role = st.text_input("Target role", value="Software Engineer")
default_model = "gemini-1.5-flash" if provider.startswith("Google") else "mistral"
model_name = st.text_input("Model name", value=default_model)
uploaded_resume = st.file_uploader("Upload Resume (PDF)", type="pdf")

st.markdown(
    """
<style>
.main { padding: 2rem; }
.stButton>button { width: 100%; }
</style>
""",
    unsafe_allow_html=True,
)

api_key = get_api_key()
if provider.startswith("Google") and not api_key:
    st.warning("Set GOOGLE_API_KEY in Streamlit secrets or environment variables.")

if uploaded_resume:
    st.success("Resume uploaded successfully.")
    resume_text = extract_resume_text(uploaded_resume)

    if not resume_text:
        st.error("Could not extract text from the PDF. Try another resume file.")
    else:
        st.text_area("Resume Text Preview", resume_text, height=260)

        if st.button("Analyze Resume"):
            with st.spinner("Analyzing resume..."):
                try:
                    if provider.startswith("Google"):
                        if not api_key:
                            st.error("Missing GOOGLE_API_KEY. Add it and try again.")
                        else:
                            client = genai.Client(api_key=api_key)
                            result = analyze_resume(client, model_name, resume_text, role)
                            st.subheader("Analysis Result")
                            st.write(result)
                    else:
                        result = analyze_resume_ollama(model_name, resume_text, role)
                        st.subheader("Analysis Result")
                        st.write(result)
                except Exception as exc:
                    st.error(f"Analysis failed: {exc}")
