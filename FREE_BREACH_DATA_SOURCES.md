# Besplatni Izvori Breach Podataka

## ✅ HIBP API Key je BESPLATAN!

**VAŽNO:** Have I Been Pwned API key je **POTPUNO BESPLATAN**! Ne plaća se ništa!

### Kako dobiti besplatni API key:
1. Idite na: https://haveibeenpwned.com/API/Key
2. Kliknite "Get API Key"
3. Registrujte se (besplatno, samo email)
4. Kopirajte API key
5. Dodajte u `backend/.env`: `HIBP_API_KEY=your-key-here`

**Rate Limits (besplatno):**
- Sa API key-om: Više zahteva
- Bez API key-a: 1 zahtev na 1.5 sekundi

## Alternativni Besplatni Izvori

### 1. HIBP Password API (POTPUNO BESPLATNO - bez API key-a)
- ✅ Već implementirano u aplikaciji
- ✅ Ne zahteva API key
- ✅ Proverava preko 11 milijardi kompromitovanih lozinki
- ✅ Koristi k-anonymity model (siguran)

### 2. Web Scraping (BESPLATNO)
- ✅ Već implementirano u aplikaciji
- ✅ Može da skrejpuje sa javnih breach baza
- ⚠️ Treba poštovati robots.txt i terms of service

### 3. Javne Breach Baze (BESPLATNO)
Mogu se dodati izvori kao što su:
- DeHashed (ima besplatni tier)
- LeakCheck (ima besplatni tier)
- BreachDirectory (javni API)

## Implementacija Alternativa

Aplikacija već ima:
1. ✅ **BreachScraper** - za web scraping
2. ✅ **Password API** - potpuno besplatno
3. ✅ **Fallback mehanizam** - ako HIBP API ne radi, pokušava web scraping

## Preporuka

**Najbolje rešenje:** Koristite besplatni HIBP API key (ne košta ništa!)

**Alternativa:** Ako ne želite API key, aplikacija će:
1. Koristiti Password API (besplatno, bez API key-a)
2. Pokušati web scraping (ako su izvori dostupni)
3. Prikazati poruku da je potreban API key za email proveru
