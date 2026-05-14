# 🎓 StudyFlow AI

**The Intelligent Multi-Agent Study Companion**

StudyFlow AI is a high-performance academic tool designed to transform raw documents into professional, research-backed study guides. Built with a three-stage AI pipeline, it automates document analysis, deep-dive research, and high-quality PDF generation.

---

## 🚀 Key Features

* **📄 Smart Ingestion:** Upload any PDF or text-based assignment. Our agent extracts core concepts, deadlines, and requirements instantly.
* **🔍 Deep-Dive Research:** Powered by **Google Search Grounding**, the Research Agent finds academic sources, verified data, and real-world examples to supplement your material.
* **✍️ Professional Authoring:** Automatically drafts a structured Study Guide in Markdown, complete with a TL;DR, Action Plan, and Resource Library.
* **📥 PDF Export:** One-click conversion from AI-generated Markdown to a beautifully styled A4 PDF using **WeasyPrint**.
* **⚡ 2026 Engine:** Optimized with **Gemini 3.1 Flash-Lite** for sub-second latency and intelligent rate-limit handling.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Python-based Web UI)
* **AI Engine:** [Google Gemini 3.1 Flash-Lite](https://ai.google.dev/) (2026 Stable Release)
* **Document Analysis:** Google GenAI SDK (PDF & Text support)
* **PDF Engine:** [WeasyPrint](https://weasyprint.org/) & [Markdown](https://python-markdown.github.io/)
* **Language:** Python 3.10+

---

## ⚙️ Project Architecture

StudyFlow uses a **Multi-Agent Orchestration** workflow to ensure data quality:

1. **Ingestor Agent:** Parses the user's uploaded file to define the "Context."
2. **Researcher Agent:** Uses the Context to perform live web searches for supplementary academic data.
3. **Writer Agent:** Synthesizes all gathered data into a final, professional study document.

---

## 💻 Installation & Setup

1. **Clone the Repository:**
```bash
git clone https://github.com/Meloppa/StudyFlow-AI.git
cd StudyFlow-AI

```


2. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


3. **Set Up Environment Variables:**
Create a `.env` file or export your API key:
```bash
export GEMINI_API_KEY="your_api_key_here"

```


4. **Run the App:**
```bash
streamlit run app.py

```



---

## 🛡️ Error Handling & Quota Management

StudyFlow AI is designed for the **Gemini Free Tier**. It includes:

* **Intelligent Backoff:** Automatic 60-second cooldowns when 429 (Rate Limit) errors occur.
* **Model Fallbacks:** Automatically switches between Gemini 3.1 Flash-Lite and Gemini 2.0 Flash to maximize uptime.
* **Context Truncation:** Ensures large documents don't exceed the 1-million-token input limit.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

### 👨‍💻 Developed By

**Meloppa** - *Hackathon 2026 Participant*

---

### 💡 Pro-Tip for your Demo:

To make this look even better on GitHub, you can add a screenshot of your app's UI right under the title:
`![App Screenshot](path/to/your/screenshot.png)`
