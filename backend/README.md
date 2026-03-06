# Breach Analyzer Backend

Backend API za analizu kompromitovanih kredencijala.

## Struktura Projekta

Projekat je organizovan prema Clean Architecture principima:

```
backend/
├── src/
│   ├── domain/              # Domain layer (entities, value objects, interfaces)
│   ├── application/         # Application layer (use cases, services)
│   ├── infrastructure/      # Infrastructure layer (database, external APIs, ML)
│   ├── api/                 # API layer (routes, schemas, middleware)
│   └── config/              # Configuration
├── requirements.txt
├── .env.example
└── main.py
```

## Instalacija

1. Kreiraj virtualno okruženje:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ili
venv\Scripts\activate  # Windows
```

2. Instaliraj zavisnosti:
```bash
pip install -r requirements.txt
```

3. Kopiraj `.env.example` u `.env` i popuni vrednosti:
```bash
cp .env.example .env
```

4. Postavi PostgreSQL bazu podataka i ažuriraj `DATABASE_URL` u `.env`

5. Pokreni aplikaciju:
```bash
python main.py
```

API će biti dostupan na `http://localhost:8000`

## API Dokumentacija

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Moduli

### 1. API Layer
- REST API endpoints
- Request/Response schemas
- Middleware (auth, rate limiting, error handling)

### 2. Data Collection
- HaveIBeenPwned API integracija
- Web scraping mehanizmi

### 3. ML/AI Modul
- Password strength classifier
- Risk predictor
- Pattern analyzer

### 4. Risk Assessment
- Procena rizika kredencijala
- Generisanje preporuka

### 5. Notifications
- Email notifikacije
- Notification queue

### 6. Database
- PostgreSQL sa SQLAlchemy ORM
- Repository pattern implementacija

## Testiranje

```bash
pytest
```

## License

MIT
