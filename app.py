import os
import json
from io import BytesIO
from PIL import Image
import streamlit as st
from dotenv import load_dotenv

# Load local .env if present
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="BugLens - Multimodal AI Issue Copilot",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished Hackathon Look
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF6B4A, #FFA34E, #388BFD);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #8b949e;
        margin-bottom: 1.2rem;
    }
    .badge-container {
        display: flex;
        gap: 8px;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 14px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    .badge-hacktober {
        background-color: #ff5e3620;
        color: #ff5e36;
        border: 1px solid #ff5e3640;
    }
    .badge-gemma {
        background-color: #1a73e820;
        color: #4285f4;
        border: 1px solid #4285f440;
    }
    .badge-open {
        background-color: #00d08420;
        color: #00c853;
        border: 1px solid #00c85340;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff5e36, #ff8c42);
        color: white;
        font-weight: 700;
        border: none;
        padding: 0.6rem 1.4rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(255, 94, 54, 0.25);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(255, 94, 54, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR CONFIG -----------------
with st.sidebar:
    st.image("https://octodex.github.com/images/doctocat.png", width=90)
    st.markdown("### ⚙️ Engine Settings")

    env_key = os.getenv("GEMINI_API_KEY", "")
    api_key = st.text_input(
        "Gemini API Key",
        value=env_key,
        type="password",
        help="Enter your Google Gemini / Gemma API key. Can also be set as GEMINI_API_KEY environment variable."
    )

    model_option = st.selectbox(
        "Multimodal Model",
        [
            "gemini-3.8-flash",
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-flash",
            "Custom Model ID"
        ],
        index=0,
        help="Select the multimodal model to use. Defaults to the fast and accurate gemini-3.8-flash."
    )

    if model_option == "Custom Model ID":
        selected_model = st.text_input("Enter custom model name", value="gemini-3.8-flash")
    else:
        selected_model = model_option

    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.05,
                           help="Lower values yield more deterministic code fixes and structured JSON.")

    st.markdown("---")
    st.markdown("### 🏆 Hackathon Eligibility")
    st.markdown("""
    - **Best Use of Gemma / Multimodal**: Multimodal analysis of UI bugs and stack-trace screenshots.
    - **Best Open Source AI Project**: 100% open-source tool for GitHub maintainers & contributors.
    """)
    st.markdown("---")
    st.markdown("Built for **Hacktoberfest 2026** 🎃")

# ----------------- MAIN UI -----------------
st.markdown('<div class="main-title">🔍 BugLens — Multimodal Issue & Bug Copilot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Instantly convert screenshots of broken UIs, terminal stack traces, and errors into root-cause diagnoses, code patches, and ready-to-file GitHub Issues.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="badge-container">
    <span class="badge badge-hacktober">🎃 Hacktoberfest 2026</span>
    <span class="badge badge-gemma">🤖 Gemma & Gemini Multimodal</span>
    <span class="badge badge-open">🌐 Open Source Developer Tool</span>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1], gap="medium")

uploaded_image = None

with col_left:
    st.markdown("#### 1. Upload Error / UI Screenshot")
    upload_tab, camera_tab, sample_tab = st.tabs(["📁 File Upload", "📷 Camera Capture", "💡 Sample Image"])

    with upload_tab:
        file = st.file_uploader("Upload error screenshot or UI bug", type=["png", "jpg", "jpeg", "webp"])
        if file:
            uploaded_image = Image.open(file)

    with camera_tab:
        cam_file = st.camera_input("Capture screenshot or physical screen")
        if cam_file:
            uploaded_image = Image.open(cam_file)

    with sample_tab:
        st.write("Don't have a screenshot right now? Test with our realistic stacktrace sample:")
        sample_path = os.path.join(os.path.dirname(__file__), "samples", "sample_stacktrace.png")
        if os.path.exists(sample_path):
            if st.button("Use Sample Python KeyError Stacktrace"):
                uploaded_image = Image.open(sample_path)
                st.session_state["sample_active"] = True

    if uploaded_image:
        st.image(uploaded_image, caption="Visual Input", use_container_width=True)

with col_right:
    st.markdown("#### 2. Provide Context (Optional)")
    project_name = st.text_input("Repository / Project Name", placeholder="e.g. acme/user-auth-service")
    framework_context = st.selectbox(
        "Framework / Tech Stack",
        ["Auto-Detect from Image", "Python / FastAPI / Django", "TypeScript / React / Next.js", "Node.js / Express", "Go", "Rust", "Other"],
        index=0
    )
    user_notes = st.text_area(
        "What was happening when the error occurred?",
        placeholder="e.g. Occurs when logging in with an expired session token, or after clicking the submit button.",
        height=100
    )
    code_snippet = st.text_area(
        "Relevant Code Snippet (Optional)",
        placeholder="Paste suspected code file or function here if available...",
        height=140
    )

st.markdown("---")

# ----------------- PROMPT & ANALYSIS LOGIC -----------------
def analyze_multimodal_bug(image: Image.Image, key: str, model_name: str, temp: float, proj: str, stack: str, notes: str, code: str):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=key)

    prompt = f"""
You are an expert Principal Software Engineer and Open Source Triage Maintainer specializing in debugging, UI regressions, and code review.
Analyze the provided screenshot (which may be a terminal stack trace, a browser console error, a broken web/mobile UI, or a compiler log).

### Context provided by user:
- Project/Repo: {proj if proj else 'Not specified'}
- Tech Stack: {stack}
- User Notes: {notes if notes else 'None'}
- Relevant Code Snippet:
```
{code if code else 'None provided'}
```

### Instructions:
Provide your response strictly structured in clear, professional GitHub-flavored Markdown with the following exact sections:

## 1. 🚨 Issue Summary & Classification
- **Issue Title**: Concise, descriptive title for a GitHub issue (e.g. `[Bug]: KeyError 'exp' in parse_user_payload during JWT validation`)
- **Severity**: [Critical / High / Medium / Low]
- **Category**: [Runtime Exception / Visual Regression / Syntax Error / Environment & Dependency / Memory or Timeout]
- **Primary Tech Stack**: Detected framework/language

## 2. 🔍 Visual Diagnostics & Error Extraction
- Transcribe the exact error messages, file names, line numbers, or visual anomalies extracted from the screenshot.
- Identify the exact component, line, or CSS/DOM element responsible.

## 3. 🎯 Root Cause Analysis
Explain clearly *why* this error occurred in 2-3 sentences. Detail the sequence of events leading to the failure.

## 4. 🛠️ Step-by-Step Resolution & Proposed Code Fix
Explain how to resolve the bug. Provide the exact, production-ready code patch or corrected snippet with comments.

## 5. 📋 Formatted GitHub Issue Template
Provide a complete, copy-pasteable GitHub Issue in markdown format inside a single markdown block starting with:
```markdown
# [Bug]: <Title>

**Describe the Bug**
...

**Steps to Reproduce**
1. ...
2. ...

**Expected Behavior**
...

**Actual Behavior**
...

**Environment**
...

**Proposed Solution**
...
```
"""

    response = client.models.generate_content(
        model=model_name,
        contents=[image, prompt],
        config=types.GenerateContentConfig(
            temperature=temp,
            max_output_tokens=3000
        )
    )
    return response.text

# ----------------- TRIGGER BUTTON -----------------
analyze_col, _ = st.columns([1, 2])
with analyze_col:
    analyze_clicked = st.button("🚀 Analyze Screenshot & Generate Issue", use_container_width=True)

if analyze_clicked:
    if not api_key:
        st.error("⚠️ Please enter your Gemini API Key in the left sidebar to proceed.")
    elif not uploaded_image:
        st.warning("⚠️ Please upload an image, capture one with your camera, or use the sample image.")
    else:
        with st.spinner("🧠 BugLens is analyzing visual evidence, extracting stack traces, and formulating the fix..."):
            try:
                result_text = analyze_multimodal_bug(
                    image=uploaded_image,
                    key=api_key,
                    model_name=selected_model,
                    temp=temperature,
                    proj=project_name,
                    stack=framework_context,
                    notes=user_notes,
                    code=code_snippet
                )
                st.session_state["analysis_result"] = result_text
                st.success("✅ Analysis completed successfully!")
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")

# ----------------- RESULTS DISPLAY -----------------
if "analysis_result" in st.session_state:
    result = st.session_state["analysis_result"]

    st.markdown("### 📋 Triage & Resolution Report")

    # Action bar for downloads
    dl_col1, dl_col2, _ = st.columns([1, 1, 2])
    with dl_col1:
        st.download_button(
            label="📥 Download Full Report (.md)",
            data=result,
            file_name="buglens_triage_report.md",
            mime="text/markdown",
            use_container_width=True
        )

    # Display full report
    st.markdown(result)
