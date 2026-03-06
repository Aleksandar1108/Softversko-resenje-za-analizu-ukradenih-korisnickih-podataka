# Data Collection Module

Modul za automatsko prikupljanje breach podataka iz različitih izvora.

## Komponente

### 1. DataCollectorService
Glavni servis koji koordinira prikupljanje podataka iz različitih izvora:
- **HaveIBeenPwned API** - Prikupljanje breach metapodataka
- **Web Scraping** - Prikupljanje podataka sa javnih breach baza
- **Normalizacija** - Normalizacija email i password podataka
- **Deduplikacija** - Izbegavanje duplikata

### 2. BreachScraper
Web scraper koji parsira breach podatke sa različitih izvora:
- Parsiranje HTML struktura (tabele, kartice, JSON-LD)
- Ekstrakcija email i password parova
- Normalizacija podataka

### 3. DataCollectionScheduler
Scheduler za automatsko prikupljanje podataka:
- **Dnevna sinhronizacija sa HIBP** (2:00 AM)
- **Nedeljno web scraping** (Nedelja 3:00 AM)
- **Periodično prikupljanje kredencijala** (svakih 6 sati)

## Korišćenje

### Automatsko Prikupljanje (Scheduler)

Pokreni scheduler:

```bash
python scripts/start_scheduler.py
```

Scheduler će automatski:
- Sinhronizovati breach podatke sa HIBP API-ja svakog dana
- Skrejpovati web izvore jednom nedeljno
- Prikupljati kredencijale svakih 6 sati

### Ručno Prikupljanje (API)

#### Sinhronizacija sa HIBP

```bash
POST /api/v1/data-collection/sync/hibp
Authorization: Bearer <token>
```

#### Web Scraping

```bash
POST /api/v1/data-collection/scrape
Authorization: Bearer <token>
Content-Type: application/json

{
  "sources": ["https://example-breach-db.com/breaches"],
  "parse_credentials": true
}
```

#### Prikupljanje iz svih izvora

```bash
POST /api/v1/data-collection/collect/all
Authorization: Bearer <token>
Content-Type: application/json

{
  "sources": ["https://example-breach-db.com/breaches"]
}
```

## Konfiguracija

### Web Sources

Dodaj web izvore u `scripts/start_scheduler.py`:

```python
web_sources = [
    "https://example-breach-db.com/breaches",
    "https://another-source.com/data",
]
```

### Scheduler Settings

Podesi vremenske intervale u `data_collection_scheduler.py`:

```python
# Dnevna sinhronizacija
CronTrigger(hour=2, minute=0)

# Nedeljno scraping
CronTrigger(day_of_week="sun", hour=3, minute=0)

# Periodično prikupljanje
IntervalTrigger(hours=6)
```

## Funkcionalnosti

### Email Normalizacija
- Konverzija u lowercase
- Uklanjanje whitespace-a
- Validacija formata
- Uklanjanje prefiksa (mailto:)

### Password Parsing
- Detekcija različitih formata (email:password, email|password)
- Validacija dužine (4-200 karaktera)
- Uklanjanje nepotrebnih prefiksa

### Deduplikacija
- Praćenje već viđenih kredencijala
- Provera u bazi pre čuvanja
- Jedinstveni ključ: `email:password_hash:breach_id`

### Error Handling
- Graceful handling grešaka
- Logging svih operacija
- Nastavak rada pri greškama na jednom izvoru

## Sigurnost

⚠️ **VAŽNO**: 
- Poštuj robots.txt fajlove
- Koristi rate limiting
- Ne skrejpuj zaštićene sajtove bez dozvole
- Poštuj Terms of Service

## Logging

Sve operacije se loguju sa sledećim nivoima:
- **INFO**: Uspešne operacije i statistike
- **WARNING**: Upozorenja (npr. duplikati)
- **ERROR**: Greške tokom prikupljanja

## Statistike

Svaka operacija vraća statistike:
```json
{
  "breaches_collected": 10,
  "credentials_collected": 150,
  "duplicates_skipped": 5,
  "errors": 0
}
```
