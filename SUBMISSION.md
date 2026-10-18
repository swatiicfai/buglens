# 🏆 MLH / Devpost Hackathon Submission Template

Copy and paste the sections below directly into your MLH / Devpost project submission form:

---

### Project Name
**BugLens — Multimodal AI Issue & Bug Copilot**

### Elevator Pitch (Short Description)
Transform screenshots of broken UIs, terminal stack traces, and errors into instant root-cause diagnoses, code patches, and ready-to-file GitHub Issues.

---

### About the Project (Long Description)

#### 💡 Inspiration
During Hacktoberfest, open-source contributors and maintainers spend countless hours dealing with vague bug reports. Contributors often post screenshots of broken UI layouts or terminal crash dumps without understanding the underlying trace, while maintainers struggle to triage tickets that lack reproduction steps or system context. We asked ourselves: *What if an open model with multimodal vision could inspect the screenshot, extract the exact error, diagnose the root cause, write the code fix, and format a production-grade GitHub Issue in seconds?* That is why we built **BugLens**.

#### 🚀 What it Does
- **Multimodal Vision Analysis**: Developers and testers upload a screenshot of an error, terminal log, UI glitch, or capture it directly using their camera.
- **Accurate Error & OCR Diagnostics**: Identifies file paths, line numbers, variable states, and specific exception types (e.g., KeyError, NullPointer, CSS overflow) directly from image pixels.
- **Root-Cause Reasoning**: Delivers a clear 2-sentence explanation of why the failure occurred.
- **Actionable Code Patches**: Generates production-ready code fixes with syntax highlighting.
- **Automated GitHub Issue Generation**: Synthesizes a standardized, ready-to-file GitHub Issue Markdown document complete with Steps to Reproduce, Expected vs. Actual behavior, and Environment details, available for 1-click download.

#### 🛠️ How We Built It
- **Frontend / Interface**: Streamlit for an intuitive, zero-latency developer dashboard.
- **Multimodal AI Engine**: Powered by Google's latest multimodal models via the Google GenAI SDK (`google-genai`), leveraging vision intelligence for visual debugging.
- **Image Processing**: Pillow for client-side image transformation and camera input processing.
- **Language**: Python 3.12.

#### 🧗 Challenges We Ran Into
Handling diverse screenshot resolutions, terminal color codes, and noisy UI backgrounds required crafting robust multimodal system prompts that enforce structured diagnostic outputs rather than generic chatbot answers.

#### 🎖️ Accomplishments We're Proud Of
- Creating an end-to-end working developer tool in under an hour.
- Bridging visual bug artifacts directly to source code solutions.
- Creating a 100% open-source tool with MIT license directly applicable to the open-source and Hacktoberfest ecosystem.

#### 📚 What We Learned
How effective lightweight multimodal models are at OCR and structural comprehension of code artifacts, terminal traces, and UI components without requiring traditional OCR pipelines.

#### 🔮 What's Next for BugLens
- Direct GitHub App integration to auto-comment on pull request failure screenshots.
- IDE Extension (VS Code / JetBrains) to capture and triage terminal errors with one shortcut.
