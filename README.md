# AIgument-backend

Tech stack: Python + FastAPI + Anthropic AI

## Setup

### 1. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
```
If you get "running scripts is disabled", do -

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

**macOS / Linux:**
```sh
cd backend
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. API key (use a `.env` file)
Add `.env` in the root directory and set:
```
ANTHROPIC_API_KEY=your-api-key-here
```

The app loads this automatically via `python-dotenv`; do not commit `.env`.

## Run

From the project root:

```sh
fastapi dev main.py
```