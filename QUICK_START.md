# Brzo Pokretanje

## ✅ Sve greške su rešene!

Backend i frontend su spremni za pokretanje.

## Pokretanje Backend Servera

```powershell
cd backend
$env:PYTHONPATH = $PWD
.\venv\Scripts\python.exe -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000 --reload
```

**Ili jednostavno:**
```powershell
cd backend
.\start_backend.ps1
```

## Pokretanje Frontend Servera

```powershell
cd frontend
npm run dev
```

**Ili jednostavno:**
```powershell
cd frontend
.\start_frontend.ps1
```

## Pokretanje Oba Servera Odjednom

```cmd
start_all.bat
```

## URL-ovi

- **Backend API**: http://localhost:8000
- **API Dokumentacija**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Frontend**: http://localhost:3000

## Provera Statusa

Nakon pokretanja, proveri da li serveri rade:

```powershell
# Backend
Invoke-WebRequest -Uri "http://localhost:8000/health"

# Frontend
Invoke-WebRequest -Uri "http://localhost:3000"
```

## Rešeni Problemi

✅ Svi importi su ispravljeni (relativni → apsolutni)
✅ Svi nedostajući paketi su instalirani
✅ SQLAlchemy `metadata` konflikt je rešen
✅ App se učitava bez grešaka
