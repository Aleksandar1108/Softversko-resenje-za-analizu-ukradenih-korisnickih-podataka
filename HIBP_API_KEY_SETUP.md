# HIBP API Key Setup

## Problem

Have I Been Pwned API v3 **zahteva API key** za `breachedaccount` endpoint. Bez API key-a, endpoint vraća 401 grešku i ne možemo da dobijemo podatke o breach-ovima.

## Rešenje

### 1. Dobijte besplatni API key

1. Idite na: https://haveibeenpwned.com/API/Key
2. Kliknite na "Get API Key"
3. Registrujte se ili se prijavite
4. Kopirajte vaš API key

### 2. Dodajte API key u backend/.env

Otvorite `backend/.env` fajl i dodajte:

```env
HIBP_API_KEY=your-actual-api-key-here
```

**Napomena:** Zamenite `your-actual-api-key-here` sa vašim stvarnim API key-em.

### 3. Restartujte backend server

Nakon dodavanja API key-a, restartujte backend server da učita novu konfiguraciju.

## Alternativa (bez API key-a)

Ako ne želite da koristite API key, možete koristiti javni endpoint, ali ima **striktne rate limite**:
- Maksimalno 1 zahtev na 1.5 sekundi
- Ako prekoračite limit, morate čekati 5 minuta

## Provera

Nakon što dodate API key, proverite backend logove. Trebalo bi da vidite:

```
HIBP Client initialized with API key: abc12345...
```

Umesto:

```
HIBP Client initialized WITHOUT API key (rate limited)
```

## Testiranje

Nakon što dodate API key, testirajte email check funkcionalnost. Trebalo bi da vraća iste rezultate kao Have I Been Pwned sajt.
