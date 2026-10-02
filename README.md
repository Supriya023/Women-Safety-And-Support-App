# Women Safety and Support App

This project contains:
- `Backend/` - Node.js + Express + MongoDB API
- `frontend/` - Flutter client (Web/Desktop/Mobile)

## Run on Windows (PowerShell)

### Quick Start (print commands)
From project root, print the exact commands users should run:
```powershell
powershell -ExecutionPolicy Bypass -File .\run-windows.ps1 -Port 5000
```
### 1) Start MongoDB locally
Use one of these:
- Installed as Windows service: `net start MongoDB`
- Manual start: `mongod --dbpath C:\data\db`

### 2) Run Backend
```powershell
cd Backend
npm install
$env:PORT=5000
if (!(Test-Path .env)) { Copy-Item .env.example .env }
npm run dev
```
Backend listens on `http://127.0.0.1:5000`.

Set AI chatbot key (optional, enables Groq-powered replies):
```powershell
$env:GROQ_API_KEY="your_groq_key"      # for current PowerShell session
$env:GROQ_MODEL="llama-3.1-8b-instant"   # optional
npm run dev
```

Persist key across new terminals (optional):
```powershell
setx GROQ_API_KEY "your_groq_key"
setx GROQ_MODEL "llama-3.1-8b-instant"
```

### 3) (Optional) Seed admin user
```powershell
cd Backend
npm run seed:admin
```
Default login: `admin / admin` (from `Backend/.env` defaults in script).

### 4) Run Flutter Frontend
```powershell
cd frontend
flutter pub get
flutter run -d chrome --dart-define=API_BASE_URL=http://127.0.0.1:5000
```
If backend runs on another port, update `API_BASE_URL` to the same port.

## Notes
- Signup now requires selecting role (`user` or `volunteer`) on Create Account screen.
- If a logged-in account has no role (for example first-time Google account), app shows a role selection screen before dashboard access.
- Chatbot uses Groq when `GROQ_API_KEY` is present; otherwise it falls back to built-in safety replies.
