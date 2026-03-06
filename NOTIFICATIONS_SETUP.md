# Notifikacioni Sistem - Setup i Upotreba

## Kako Notifikacije Rade

### 1. Automatske Notifikacije

Kada prijavljeni korisnik proveri email i nađe se u breach-ovima, sistem automatski kreira notifikacije:

- **Za prijavljene korisnike**: Notifikacije se kreiraju automatski kada provere email
- **Tip notifikacije**: `breach_alert`
- **Prioritet**: `high`
- **Lokacija**: Notifikacije se prikazuju u Notifications sekciji aplikacije

### 2. Kako Omogućiti Notifikacije

#### Opcija 1: Registracija i Email Provera

1. Registrujte se na aplikaciju
2. Prijavite se
3. Proverite vaš email na stranici "Provera Email-a"
4. Ako je email pronađen u breach-ovima, notifikacije će se automatski kreirati

#### Opcija 2: Email Notifikacije (Zahteva SMTP konfiguraciju)

Za email notifikacije, potrebno je konfigurisati SMTP u `backend/.env`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
```

Zatim u user profilu omogućite email notifikacije.

### 3. Pregled Notifikacija

1. Prijavite se na aplikaciju
2. Idite na "Notifikacije" u meniju
3. Videćete sve notifikacije o breach-ovima
4. Kliknite na "Pročitano" da označite notifikaciju kao pročitanu
5. Kliknite na "Obriši" da obrišete notifikaciju

### 4. Tipovi Notifikacija

- **breach_alert**: Kada je email pronađen u breach-u
- **risk_alert**: Kada je detektovan visok rizik
- **recommendation**: Personalizovane preporuke za sigurnost

### 5. Prioriteti

- **critical**: Kritične notifikacije (npr. novi breach)
- **high**: Visok prioritet (npr. email pronađen u breach-u)
- **normal**: Normalne notifikacije
- **low**: Nizak prioritet

## Napomena

Trenutno notifikacije se čuvaju u memoriji (NotificationQueue). Za produkciju, preporučuje se:
- Čuvanje notifikacija u bazi podataka
- Redis za queue sistem
- Email servis za slanje email notifikacija
