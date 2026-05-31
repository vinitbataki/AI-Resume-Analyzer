HEAD
# 🎯 SmartScan ATS

> An AI-powered resume analyser that scores your resume, matches keywords, and gives actionable feedback — built with Python, Streamlit, and the Anthropic Claude API.

---

## 📸 Demo

![SmartScan ATS running on localhost](https://via.placeholder.com/900x500?text=SmartScan+ATS+Screenshot)

> Run locally at: [http://localhost:8501](http://localhost:8501)

---

## ✨ Features

- 📄 **PDF Resume Upload** — extracts text from any PDF resume automatically
- 🤖 **AI-Powered Analysis** — powered by Claude (Anthropic) for deep resume feedback
- 📊 **ATS Score** — see how well your resume performs against applicant tracking systems
- 🔍 **Keyword Matching** — matched vs. missing keywords from a job description
- 💡 **Actionable Suggestions** — specific improvements to strengthen your resume
- 🎯 **Job Description Targeting** — paste a job posting to get tailored feedback
- ⚡ **Instant Results** — analysis delivered in seconds

---

## 🗂️ Project Structure

```
AI-Resume-Analyzer/
│
├── .env                    # Local environment secrets (API keys) — never commit
├── .env.example            # Template showing required environment variables
├── .gitignore              # Files Git should ignore
├── requirements.txt        # Python dependencies
├── app.py                  # Main Streamlit app — UI, layout, and web server
│
└── src/                    # Core processing logic
    ├── __init__.py         # Initialises src as a Python package
    ├── pdf_processor.py    # Extracts text from uploaded PDF resumes
    └── ai_engine.py        # Anthropic API connection and prompt configuration
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- An [Anthropic API key](https://console.anthropic.com/)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables

Copy the example file and add your API key:

```bash
cp .env.example .env
```

Then open `.env` and fill in your key:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 5. Run the app

```bash
streamlit run app.py
```

The app will open automatically at [http://localhost:8501](http://localhost:8501).

---

## 📦 Dependencies

```
streamlit
anthropic
pdfplumber
python-dotenv
```

Install all at once:

```bash
pip install streamlit anthropic pdfplumber python-dotenv
```

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic Claude API key | ✅ Yes |

Get your API key at [console.anthropic.com](https://console.anthropic.com/).

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

---

## 🧠 How It Works

```
User uploads PDF
      ↓
pdf_processor.py extracts plain text
      ↓
prompt.py builds structured prompt (resume + optional job description)
      ↓
ai_engine.py sends request to Claude API
      ↓
Claude returns structured JSON analysis
      ↓
app.py renders scores, keywords, strengths, suggestions in Streamlit UI
```

---

## 📊 Analysis Output

SmartScan ATS returns the following for every resume:

| Section | Description |
|---|---|
| **Overall Score** | 0–100 rating of resume quality |
| **ATS Score** | How well the resume passes ATS filters |
| **Clarity Score** | Readability and structure rating |
| **Summary** | 2–3 sentence professional assessment |
| **Strengths** | What the resume does well |
| **Weaknesses** | Areas that need improvement |
| **Matched Keywords** | Keywords found in both resume and job description |
| **Missing Keywords** | Important keywords absent from the resume |
| **Suggestions** | Specific, actionable improvements |
| **ATS Tips** | Formatting advice to pass automated screening |

---

## ☁️ Deployment

### Deploy to Streamlit Cloud (free)

1. Push your project to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → connect your GitHub repo
4. Set the main file path to `app.py`
5. Under **Advanced settings → Secrets**, add:
   ```
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
   ```
6. Click **Deploy**

Your app will be live at `https://your-app-name.streamlit.app`.

---

## 🛡️ Security Notes

- Your API key is stored in `.env` locally and in Streamlit Cloud's secrets manager — never in your code
- The `.env` file is excluded from Git via `.gitignore`
- No resume data is stored or logged — analysis happens in memory and is discarded after the session

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Built by **[ Vinit Bataki ]**

- GitHub: [@vinitbataki](https://github.com/vinitbataki?tab=repositories)
- LinkedIn: [Vinit Bataki]((https://www.linkedin.com/in/vinit-bataki-8b9944314?utm_source=share_via&utm_content=profile&utm_medium=member_android))

---

## 🙏 Acknowledgements

- [Anthropic](https://anthropic.com) for the Claude API
- [Streamlit](https://streamlit.io) for the rapid UI framework
- [pdfplumber](https://github.com/jsvine/pdfplumber) for PDF text extraction

---

*SmartScan ATS — because your resume deserves a second opinion.*

# AI-Resume-Analyzer
 69de2e299c7c2079ee8964bf2fcee095c30b1ff0
