# Alternativni Besplatni Izvori Breach Podataka

## ✅ HIBP API Key je BESPLATAN!

**VAŽNO:** Have I Been Pwned API key je **POTPUNO BESPLATAN**! Ne plaća se ništa!

### Kako dobiti besplatni API key:
1. Idite na: https://haveibeenpwned.com/API/Key
2. Kliknite "Get API Key"
3. Registrujte se (besplatno, samo email)
4. Kopirajte API key
5. Dodajte u `backend/.env`: `HIBP_API_KEY=your-key-here`

## Alternativni Besplatni Izvori

### 1. ✅ HIBP Password API (POTPUNO BESPLATNO)
- **Status:** Već implementirano u aplikaciji
- **API Key:** Ne zahteva
- **Funkcionalnost:** Proverava da li je lozinka kompromitovana
- **Baza:** Preko 11 milijardi kompromitovanih lozinki
- **Sigurnost:** K-anonymity model (samo prva 5 karaktera hash-a se šalje)

### 2. ✅ Web Scraping (BESPLATNO)
- **Status:** Već implementirano u aplikaciji
- **Funkcionalnost:** Može da skrejpuje sa javnih breach baza
- **Komponenta:** `BreachScraper` klasa
- **Napomena:** Treba poštovati robots.txt i terms of service

### 3. Javne Breach Baze (Mogu se dodati)

#### DeHashed
- **URL:** https://dehashed.com
- **Besplatni tier:** Da (ograničen)
- **API:** Da

#### LeakCheck
- **URL:** https://leakcheck.io
- **Besplatni tier:** Da (ograničen)
- **API:** Da

#### BreachDirectory
- **URL:** https://breachdirectory.tk
- **Besplatni tier:** Da
- **API:** Da

## Trenutna Implementacija

Aplikacija već ima:

1. ✅ **HIBP Password API** - Potpuno besplatno, bez API key-a
2. ✅ **BreachScraper** - Web scraping mehanizam
3. ✅ **Fallback mehanizam** - Ako HIBP API ne radi, pokušava alternativne metode

## Preporuka

**Najbolje rešenje:** Koristite besplatni HIBP API key (ne košta ništa!)

**Alternativa:** Ako ne želite API key:
- ✅ Koristite Password Check (besplatno, bez API key-a)
- ✅ Implementirajte web scraping sa javnih izvora
- ⚠️ Email provera neće raditi bez API key-a (HIBP API v3 zahteva API key)

## Zaključak

**Ne morate da plaćate ništa!** 
- HIBP API key je besplatan
- Password API je besplatan
- Web scraping je besplatan

Samo treba da se registrujete na HIBP sajtu da dobijete besplatni API key.
