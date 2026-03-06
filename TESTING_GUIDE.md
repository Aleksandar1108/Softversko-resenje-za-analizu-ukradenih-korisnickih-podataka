# Vodič za Testiranje Hibridnog Pristupa

## ✅ Serveri Pokrenuti

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Dokumentacija**: http://localhost:8000/docs

## 🧪 Test Scenariji

### 1. Anonimna Provera Email-a (bez registracije)

**Koraci:**
1. Otvori http://localhost:3000 u browseru
2. Na home page-u, unesi email adresu u polje "Brza Provera Email-a"
3. Klikni "Proveri"
4. Vidi rezultate provere bez potrebe za registracijom

**Očekivano:**
- ✅ Email se proverava bez autentifikacije
- ✅ Rezultati se prikazuju odmah
- ✅ Ako je email kompromitovan, vidi se lista breach-ova
- ✅ Ako nije kompromitovan, vidi se poruka da je bezbedan

### 2. Opciona Registracija

**Koraci:**
1. Nakon provere email-a, ako je kompromitovan, pojaviće se opcija "Registrujte se besplatno"
2. Klikni na dugme
3. Popuni formu za registraciju:
   - Ime (opciono)
   - Prezime (opciono)
   - Email adresa
   - Lozinka (min 8 karaktera)
   - Potvrdi lozinku
4. Klikni "REGISTRUJ SE"

**Očekivano:**
- ✅ Korisnik se registruje uspešno
- ✅ Automatski se loguje (dobija JWT token)
- ✅ Preusmerava se na dashboard ili home page
- ✅ Sada ima pristup zaštićenim funkcionalnostima

### 3. Login

**Koraci:**
1. Klikni na "Login" u navigacionom meniju
2. Unesi email i lozinku
3. Klikni "PRIJAVI SE"

**Očekivano:**
- ✅ Korisnik se uspešno loguje
- ✅ Dobija JWT token
- ✅ Preusmerava se na dashboard
- ✅ Ime korisnika se prikazuje u meniju

### 4. Zaštićene Funkcionalnosti (za prijavljene korisnike)

**Dostupne funkcionalnosti:**
- ✅ Dashboard sa statistikama
- ✅ Istorija provera
- ✅ Notifikacije o novim breach-ovima
- ✅ Personalizovane preporuke
- ✅ Profil korisnika

## 🔍 Provera u Browser Developer Tools

### Network Tab
1. Otvori Developer Tools (F12)
2. Idi na Network tab
3. Proveri zahteve:
   - `POST /api/v1/users/check-email` - treba da prođe bez autentifikacije
   - `POST /api/v1/users/register` - treba da vrati token i user
   - `POST /api/v1/users/login` - treba da vrati token i user
   - `GET /api/v1/users/me` - treba da zahteva autentifikaciju

### Console Tab
- Proveri da li ima grešaka
- Proveri da li se token čuva u localStorage

## 🐛 Troubleshooting

### Problem: CORS greška
**Rešenje:** Proveri da li je backend restartovan nakon CORS promena

### Problem: 401 Unauthorized
**Rešenje:** Proveri da li je token validan u localStorage

### Problem: 400 Bad Request
**Rešenje:** Proveri format podataka koji se šalju (email format, password length)

### Problem: Email provera ne radi
**Rešenje:** 
- Proveri da li backend radi
- Proveri Network tab za greške
- Proveri da li je HIBP API key podešen (opciono)

## 📝 Napomene

- Anonimna provera radi bez registracije
- Registracija je opciona za dodatne funkcionalnosti
- Notifikacije zahtevaju registraciju
- Dashboard i statistike su dostupni samo prijavljenim korisnicima
