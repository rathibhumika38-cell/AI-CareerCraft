# AI CareerCraft – Resume & Portfolio Builder

An AI-powered web application that helps students build professional resumes, cover letters, and portfolios using Generative AI.

---

## Features

| Feature | Description |
|---|---|
| 📄 **Resume Builder** | Multi-step form → AI generates professional summary, enhanced project descriptions, skill recommendations, and ATS keywords |
| ✍️ **Cover Letter Generator** | Personalized cover letters tailored to specific companies and job roles |
| 🎨 **Portfolio Builder** | AI-generated About Me, project descriptions, taglines and portfolio content |
| 🔍 **ATS Checker** | Resume vs job description analysis with compatibility score, matching/missing keywords |
| 🗺️ **Career Suggestions** | Personalized job roles, skills to learn, career paths, project ideas and interview topics |
| ⚡ **Demo Mode** | Works fully without an API key using realistic sample AI responses |

---

## Quick Start (Windows)

### 1. Open a terminal in the project folder

```
cd AI-CareerCraft
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. (Optional) Set up your OpenAI API key

Copy the example env file and add your key:

```powershell
copy .env.example .env
```

Then open `.env` in a text editor and replace `your_openai_api_key_here` with your actual key.

> **Without an API key the app runs in Demo Mode** — all features work with realistic sample data.

### 5. Run the application

```powershell
python app.py
```

### 6. Open in browser

```
http://127.0.0.1:5000
```

---

## Project Structure

```
AI-CareerCraft/
│
├── app.py                  ← Flask backend, all routes
├── requirements.txt        ← Python dependencies
├── .env.example            ← Environment variable template
├── README.md
│
├── templates/
│   ├── index.html          ← Landing page
│   ├── dashboard.html      ← Main dashboard
│   ├── resume.html         ← Resume builder + preview
│   ├── cover_letter.html   ← Cover letter generator
│   ├── portfolio.html      ← Portfolio builder
│   └── ats_checker.html    ← ATS checker + career suggestions
│
├── static/
│   ├── css/style.css       ← All styles (responsive, modern)
│   └── js/app.js           ← Frontend logic (forms, AI calls, rendering)
│
├── services/
│   └── ai_service.py       ← OpenAI integration + demo mode fallbacks
│
└── database/
    └── database.py         ← SQLite CRUD operations
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/generate-resume` | Generate AI resume content |
| GET | `/api/resume/<id>` | Retrieve a saved resume |
| POST | `/api/generate-cover-letter` | Generate cover letter |
| POST | `/api/generate-portfolio` | Generate portfolio content |
| POST | `/api/career-suggestions` | Get career path suggestions |
| POST | `/api/ats-check` | ATS compatibility analysis |
| GET | `/api/status` | App status + mode info |

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Optional | OpenAI API key. Without this, app runs in Demo Mode |
| `SECRET_KEY` | Optional | Flask session secret key |

---

## Demo Mode

If no `OPENAI_API_KEY` is set, the application automatically enters **Demo Mode**:

- All AI features still work
- Realistic sample responses are returned
- A yellow "Demo Mode" badge is shown in the UI
- Perfect for classroom demonstrations

---

## Technology Stack

- **Backend**: Python 3.8+, Flask
- **Database**: SQLite (auto-created on first run)
- **AI**: OpenAI GPT-3.5 Turbo (with demo mode fallback)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Design**: Custom CSS with responsive grid layout

---

## College Project Information

- **Project Name**: AI CareerCraft – Resume & Portfolio Builder
- **Problem Statement**: AI Resume & Portfolio Builder
- **Technology**: Python, Flask, OpenAI API, SQLite, HTML/CSS/JS
- **Type**: Full-stack AI web application
