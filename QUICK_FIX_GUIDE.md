# Brzi Vodič za Ispravke

## ✅ Ispravke Primene

### 1. check-email Endpoint
- ✅ Radi bez baze podataka (samo sa HIBP API)
- ✅ Ako baza ne radi, endpoint i dalje radi
- ✅ Ako HIBP API ne radi, vraća prazan rezultat (bez greške)

### 2. HIBP Client
- ✅ Bolje error handling
- ✅ Ne zatvara konekciju pre nego što se koristi
- ✅ Detaljno logovanje grešaka

### 3. SQLite Podrška
- ✅ Dodat aiosqlite za SQLite podršku
- ✅ Default database URL je sada SQLite (ne zahteva PostgreSQL setup)

## ⚠️ Važno - HIBP API Key

HIBP API v3 **zahteva API key** za `breachedaccount` endpoint.

**Opcije:**

1. **Dodaj API Key** (preporučeno):
   - Idi na: https://haveibeenpwned.com/API/Key
   - Registruj se i dobij API key
   - Dodaj u `backend/.env`:
     ```
     HIBP_API_KEY=your-api-key-here
     ```

2. **Bez API Key-a**:
   - Endpoint će raditi ali će vratiti prazan rezultat
   - Email će biti prikazan kao "nije kompromitovan" (čak i ako jeste)

## 🔧 Restart Backend Servera

**VAŽNO**: Backend mora biti restartovan!

1. Zatvori trenutni PowerShell prozor gde je backend pokrenut
2. Pokreni ponovo:
   ```powershell
   cd backend
   $env:PYTHONPATH = $PWD
   .\venv\Scripts\python.exe -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000 --reload
   ```

## 🧪 Testiranje

1. **Otvori http://localhost:3000**
2. **Unesi email i klikni "Proveri"**
3. **Proveri rezultate:**
   - Ako imaš HIBP API key: videćeš stvarne rezultate
   - Ako nemaš API key: videćeš "nije kompromitovan" (čak i ako jeste)

## 📝 Provera Grešaka

Ako i dalje ima problema:
1. Proveri backend PowerShell prozor za detaljne logove
2. Proveri browser Console (F12) za frontend greške
3. Proveri Network tab za HTTP zahteve
