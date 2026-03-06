# CORS Problem - Rešen

## Problem
Registracija nije radila zbog CORS greške. OPTIONS preflight zahtev je vraćao 400 Bad Request.

## Rešenja

### 1. Rate Limiter Middleware
- ✅ Rate limiter sada preskače OPTIONS zahteve (CORS preflight)
- OPTIONS zahtevi se ne broje u rate limiting

### 2. CORS Konfiguracija
- ✅ Dodati eksplicitni CORS origins (localhost i 127.0.0.1)
- ✅ Omogućene sve HTTP metode uključujući OPTIONS
- ✅ Dodat `max_age=3600` za keširanje preflight zahteva

### 3. Import Greška
- ✅ Ispravljen nedostajući `List` import u `user_schemas.py`

## Promene u Fajlovima

1. `backend/src/api/middleware/rate_limiter.py`
   - Dodata provera za OPTIONS metode

2. `backend/src/api/main.py`
   - Poboljšana CORS konfiguracija

3. `backend/src/config/settings.py`
   - Dodati dodatni CORS origins

4. `backend/src/api/schemas/user_schemas.py`
   - Dodat `List` import

## Restart Backend Servera

**VAŽNO**: Backend server mora biti restartovan da bi promene stupile na snagu!

1. Zatvori trenutni PowerShell prozor gde je backend pokrenut (CTRL+C)
2. Pokreni ponovo:
   ```powershell
   cd backend
   $env:PYTHONPATH = $PWD
   .\venv\Scripts\python.exe -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000 --reload
   ```

Ili jednostavno:
```powershell
cd backend
.\start_backend.ps1
```

## Testiranje

Nakon restart-a, pokušaj ponovo registraciju. Trebalo bi da radi bez CORS greške.
