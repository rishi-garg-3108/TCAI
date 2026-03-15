# Transaction Categorizer AI (TCAI)

An AI-powered transaction categorization API built with Django REST Framework. It uses LLMs (OpenAI or Ollama) to automatically categorize financial transactions based on your company's chart of accounts and historical transaction data.

---

## Table of Contents

- [How It Works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Setting Up uv](#setting-up-uv)
- [Project Setup](#project-setup)
- [Environment Configuration](#environment-configuration)
  - [Using OpenAI](#option-1-openai)
  - [Using Ollama (Local)](#option-2-ollama-local)
- [Running the Project](#running-the-project)
- [API Usage](#api-usage)
- [Switching Providers](#switching-providers)

---
## Project Structure
TCAI/
├── manage.py              # django entry point
├── pyproject.toml         # dependencies managed by uv
├── uv.lock                # locked dependency versions
├── .env.example           # template for environment variables
├── .gitignore
├── README.md
│
├── config/                # django project configuration
│   ├── settings.py        # environment variables, installed apps, logging
│   ├── urls.py            # root url routing
│   ├── asgi.py
│   └── wsgi.py
│
└── categorization/        # main app
    ├── api/               # request/response layer
    │   ├── __init__.py
    │   ├── views.py       # api endpoint
    │   ├── serializers.py # json request validation
    │   └── urls.py        # app url routing
    │
    ├── services/          # core business logic
    │   ├── __init__.py
    │   ├── categorization_service.py  # orchestrates the pipeline
    │   ├── context_builder.py         # structures transaction data
    │   ├── prompt_builder.py          # builds the llm prompt
    │   └── response_parser.py         # parses and validates llm output
    │
    ├── llm/               # llm provider integrations
    │   ├── __init__.py
    │   ├── base_provider.py       # abstract base class
    │   ├── openai_provider.py     # openai integration
    │   ├── ollama_provider.py     # ollama integration
    │   └── provider_factory.py   # picks provider based on .env
    │
│── sample_data/       # for testing
    ├── sample_transactions.json
    └── expected_outputs.json

## How It Works

```
Request → Serializer → Context Builder → Prompt Builder → LLM Provider → Response Parser → Response
```

1. **Serializer** validates the incoming request
2. **Context Builder** structures the transaction data
3. **Prompt Builder** constructs the LLM prompt
4. **LLM Provider** calls OpenAI or Ollama
5. **Response Parser** validates and returns structured JSON

---

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (package manager)
- OpenAI API key **OR** [Ollama](https://ollama.com/) installed locally

---

## Setting Up uv

`uv` is a fast Python package manager. Install it with:

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**macOS(Homebrew):**
```bash
 brew install uv
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify installation:
```bash
uv --version
```

---

## Project Setup

**1. Clone the repository:**
```bash
git clone https://github.com/rishi-garg-3108/TCAI.git
cd TCAI
```

**2. Create a virtual environment:**
```bash
uv venv
```

**3. Activate the virtual environment:**

macOS / Linux:
```bash
source .venv/bin/activate
```

Windows:
```bash
.venv\Scripts\activate
```

**4. Install dependencies:**
```bash
uv sync
```

**5. Run migrations:**
```bash
python manage.py migrate
```

---

## Environment Configuration

A `.env.example` template is included in the project root. Copy it and fill in your values:

```bash
cp .env.example .env
```

The `.env.example` file looks like this — it is safe to commit to git since it contains no real secrets:

```bash
# .env.example

DJANGO_SECRET_KEY=your-django-secret-key-here

LLM_PROVIDER=openai               # Change to "ollama" for local model

OPENAI_API_KEY=your-openai-api-key-here
MODEL_NAME=gpt-4o-mini

OLLAMA_MODEL=phi3:3.8b

```

**Generating a Django secret key:**

The `DJANGO_SECRET_KEY` is required by Django for cryptographic signing. Generate one by running:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as the value of `DJANGO_SECRET_KEY` in your `.env` file.

After copying, edit `.env` with your real values based on your chosen provider below.



---

### Option 1: OpenAI

```bash
# .env

LLM_PROVIDER=openai

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
MODEL_NAME=gpt-4o-mini
```

> Get your API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

---

### Option 2: Ollama (Local)

**Step 1 — Install Ollama:**

Download from [ollama.com](https://ollama.com/) or install via terminal:

macOS:
```bash
brew install ollama
```

Linux:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Step 2 — Pull a model:**
```bash
ollama pull phi3:3.8b
```

> Other supported models: `llama3`, `mistral`, `gemma`. Make sure the model you pull matches `OLLAMA_MODEL` in your `.env`.

**Step 3 — Start the Ollama server:**
```bash
ollama serve
```

> Ollama runs on `http://localhost:11434` by default.

**Step 4 — Configure `.env`:**

```bash
# .env

LLM_PROVIDER=ollama

OLLAMA_MODEL=phi3:3.8b
OLLAMA_BASE_URL=http://localhost:11434
```

---

## Running the Project

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000`.

---

## API Usage

### Endpoint

```
POST /api/categorize-transaction/
```

### Request Body

```json
{
  "description": "Slack monthly subscription",
  "vendor": "Slack",
  "company_context": {
    "company_id": "company_1",
    "industry": "SaaS",
    "chart_of_accounts": [
      "Software Subscription",
      "Office Supplies",
      "Travel",
      "Marketing"
    ],
    "historical_transactions": [
      {
        "description": "Notion subscription",
        "category": "Software Subscription"
      },
      {
        "description": "Google Workspace",
        "category": "Software Subscription"
      }
    ]
  }
}
```

### Example curl

```bash
curl -X POST http://127.0.0.1:8000/api/categorize-transaction/ \
-H "Content-Type: application/json" \
-d '{
  "description": "Slack monthly subscription",
  "vendor": "Slack",
  "company_context": {
    "company_id": "company_1",
    "industry": "SaaS",
    "chart_of_accounts": [
      "Software Subscription",
      "Office Supplies",
      "Travel",
      "Marketing"
    ],
    "historical_transactions": [
      {
        "description": "Notion subscription",
        "category": "Software Subscription"
      },
      {
        "description": "Google Workspace",
        "category": "Software Subscription"
      }
    ]
  }
}'
```

### Response

```json
{
  "category": "Software Subscription",
  "confidence": 1.0,
  "reason": "Slack is a software service with a monthly subscription, consistent with historical examples like Notion and Google Workspace."
}
```

| Field        | Type   | Description                              |
|--------------|--------|------------------------------------------|
| `category`   | string | Matched category from chart of accounts  |
| `confidence` | float  | Confidence score between 0 and 1         |
| `reason`     | string | Short explanation for the categorization |

---

## Switching Providers

To switch between OpenAI and Ollama, change a **single line** in your `.env`:

```bash
# Use OpenAI
LLM_PROVIDER=openai

# Use Ollama
LLM_PROVIDER=ollama
```

Then restart the server:
```bash
python manage.py runserver
```

No code changes needed.