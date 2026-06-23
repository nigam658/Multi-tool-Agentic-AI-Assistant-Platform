# Agentic AI Assistant Platform

> A Multi-Agent Orchestration System where Gemini dynamically routes user requests across specialized AI agents such as Email, Reminder, Chat, and Career Automation tools.

---



- **Email Agent** — Draft, modify, and send professional emails using AI
- **Reminder Agent** — Track e-commerce product prices and get notified when they drop
- **Chat Agent** — Natural conversation fallback for everything else

---

## 🏗️ Architecture

```
User Message (via /chat)
        │
        ▼
 JWT Authentication
        │
        ▼
  🤖 Orchestrator (Gemini)
  Detects intent → routes to tool
        │
  ┌─────┼──────┐
  ▼     ▼      ▼
📧    💰      💬
Email  Reminder  Chat
Agent  Agent    Agent
        │
        ▼
  APScheduler (every 30 min)
  Checks prices → sends email alert
```

## ✨ Features

- AI-powered tool routing using Gemini
- JWT-based authentication
- Multi-step conversational workflows
- Email drafting and sending
- Product price tracking and notifications
- Session-aware workflow switching
- Background task scheduling with APScheduler


### Key Design Patterns
- **Orchestrator-Agent Pattern** — Gemini acts as the central router
- **Stateful Session Management** — Multi-step workflows tracked per user
- **Human-in-the-Loop** — User reviews drafts/actions before execution
- **Interrupt & Resume** — Mid-workflow switching with session cleanup
- **Singleton LLM Client** — One shared Gemini client across all agents
- **Autonomous Background Agent** — APScheduler runs independently

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| AI / LLM | Google Gemini (`google-genai`) |
| Auth | JWT (`python-jose`) + bcrypt (`passlib`) |
| Database | MySQL (`mysql-connector-python`) |
| Scheduler | APScheduler |
| Email | SMTP via Gmail |
| Web Scraping | `requests` + `re` (Myntra) |
| Config | `python-dotenv` |

---

## 📁 Project Structure

```
AGENT/
├── auth/
│   ├── auth_router.py        # Signup / Login endpoints
│   ├── auth_service.py       # Password hashing & validation
│   ├── auth_repository.py    # DB queries for users
│   ├── auth_schemas.py       # Pydantic models
│   └── jwt_handler.py        # JWT create & verify
│
├── conservation_tool/
│   └── chat_service.py       # Fallback chat agent
│
├── email_tool/
│   ├── email_agent.py        # Email workflow orchestration
│   ├── email_service.py      # Draft, modify, send logic (Gemini + SMTP)
│   └── email_schema.py       # DraftEmail Pydantic model
│
├── reminder_tool/
│   ├── reminder_agent.py     # Reminder workflow orchestration
│   ├── reminder_service.py   # CRUD operations
│   ├── reminder_repository.py # DB queries for reminders
│   ├── reminder_ai_services.py # Gemini: extract data, detect action
│   └── price_checker.py      # APScheduler + Myntra scraper + alert email
│
├── routers/
│   ├── agent.py              # Main orchestrator (tool router)
│   └── agent_services.py     # detect_tool() + detect_workflow_action()
│
├── ai_client.py              # Singleton Gemini client
├── database.py               # MySQL connection
├── session_manager.py        # In-memory session store
├── chat.py                   # /chat API endpoint
├── main.py                   # FastAPI app entry point
└── .env                      # Environment variables
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/agentic-multi-tool-ai-assistant.git
cd agentic-multi-tool-ai-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn google-genai python-jose passlib bcrypt \
            mysql-connector-python apscheduler requests python-dotenv
```



### Email Agent
```
User:  Send an email to hr@company.com applying for Python Backend role
Bot:   Here's your draft — [subject, body shown]. Reply send, modify, or cancel.
User:  Make the tone more confident
Bot:   Updated draft — [new version]. Reply send, modify, or cancel.
User:  Send it
Bot:   Email sent successfully ✓
```

### Reminder Agent
```
User:  Notify me when this Myntra product goes below ₹800
       https://www.myntra.com/...
Bot:   Reminder created! I'll check every 30 minutes.

[Later — price drops]
Bot:   [Email sent to user] Price dropped to ₹749!
```

### Mid-Workflow Switch
```
User:  [In the middle of email draft flow]
       Actually, show me my reminders
Bot:   Switching to reminders... [lists reminders]
       [Email session cleared automatically]
```

---

## 🔐 Authentication Flow

1. User signs up → password hashed with bcrypt → stored in MySQL
2. User logs in → JWT token returned (expires in 24 hours)
3. Every `/chat` request includes the JWT token
4. Token is verified → `user_id` extracted → passed to the orchestrator

---


## 👨‍💻 Author

Nigam Gouda

Built by Nigam Gouda to explore Agentic AI, multi-agent orchestration, workflow automation, and backend system design using FastAPI and Google Gemini.
