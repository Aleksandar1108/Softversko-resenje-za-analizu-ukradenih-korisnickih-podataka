# Environment Variables Setup Guide

Ovaj vodič objašnjava kako da podesite environment variables za projekat.

## Backend Environment Variables

### Lokacija
Kreiraj `.env` fajl u `backend/` direktorijumu na osnovu `backend/.env.example`.

### Obavezne Varijable

```env
# Database
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/breach_analyzer

# JWT
JWT_SECRET_KEY=your-strong-secret-key-here
```

### Opcione Varijable

```env
# HIBP API (za prikupljanje breach podataka)
HIBP_API_KEY=your-hibp-api-key

# SMTP (za email notifikacije)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com

# Redis (opciono, za caching)
REDIS_URL=redis://localhost:6379/0
```

### Generisanje JWT Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Frontend Environment Variables

### Lokacija
Kreiraj `.env` fajl u `frontend/` direktorijumu na osnovu `frontend/.env.example`.

### Obavezne Varijable

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Opcione Varijable

```env
VITE_ENV=development
```

## Quick Setup

### Backend

```bash
cd backend
cp .env.example .env
# Zatim uredi .env fajl sa svojim vrednostima
```

### Frontend

```bash
cd frontend
cp .env.example .env
# Zatim uredi .env fajl sa svojim vrednostima
```

## Napomene

1. **Nikada ne commit-uj `.env` fajlove** - oni su u `.gitignore`
2. **Koristi `.env.example` kao template** - oni su u git-u
3. **Za produkciju** - koristi environment variables na serveru umesto `.env` fajlova
4. **HIBP API Key** - Dobij besplatan API key na https://haveibeenpwned.com/API/Key
