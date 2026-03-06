# Pokretanje Servera

## Backend Server

1. Otvori PowerShell u `backend` direktorijumu
2. Aktiviraj virtualno okruženje:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
3. Postavi PYTHONPATH:
   ```powershell
   $env:PYTHONPATH = $PWD
   ```
4. Pokreni server:
   ```powershell
   python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000 --reload
   ```

Ili jednostavno:
```powershell
.\start_backend.ps1
```

Backend će biti dostupan na: http://localhost:8000
API dokumentacija: http://localhost:8000/docs

## Frontend Server

1. Otvori PowerShell u `frontend` direktorijumu
2. Pokreni dev server:
   ```powershell
   npm run dev
   ```

Ili jednostavno:
```powershell
.\start_frontend.ps1
```

Frontend će biti dostupan na: http://localhost:3000

## Pokretanje oba servera odjednom

Koristi `start_all.bat` fajl u root direktorijumu projekta.
