# Status Servera

## ✅ APLIKACIJA RADI!

### Backend Server
- **Status**: ✅ RADI
- **URL**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Dokumentacija**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Frontend Server
- **Status**: ✅ RADI
- **URL**: http://localhost:3000

## Kako Testirati

### 1. Frontend
Otvorite u browseru: **http://localhost:3000**

### 2. Backend API
Otvorite u browseru: **http://localhost:8000/docs**

U Swagger UI možete:
- Videti sve dostupne endpoint-e
- Testirati API pozive direktno iz browsera
- Proveriti request/response formate

### 3. Health Check
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/health"
```

## Dostupni Endpoint-i

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/v1/breaches` - Lista breach-ova
- `POST /api/v1/users/register` - Registracija korisnika
- `POST /api/v1/users/login` - Login
- `GET /api/v1/users/me` - Trenutni korisnik
- `POST /api/v1/data-collection/sync/hibp` - Sinhronizacija HIBP podataka
- `POST /api/v1/ml-analysis/analyze-password` - Analiza lozinke
- I mnogi drugi...

## Zaustavljanje Servera

Zatvorite PowerShell prozore gde su serveri pokrenuti, ili pritisnite `CTRL+C` u tim prozorima.
