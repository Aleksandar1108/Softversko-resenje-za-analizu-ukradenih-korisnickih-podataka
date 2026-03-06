# Breach Analyzer Frontend

React frontend aplikacija za analizu kompromitovanih kredencijala.

## Tehnologije

- **React 18** - UI framework
- **React Router** - Routing
- **Material UI** - UI komponente
- **Axios** - HTTP client
- **Recharts** - Grafikoni i vizualizacije
- **Vite** - Build tool

## Instalacija

```bash
npm install
```

## Pokretanje

```bash
npm run dev
```

Aplikacija će biti dostupna na `http://localhost:3000`

## Build

```bash
npm run build
```

## Struktura Projekta

```
frontend/
├── src/
│   ├── components/        # Reusable komponente
│   │   ├── Layout/        # Layout komponenta
│   │   └── ProtectedRoute/ # Route zaštita
│   ├── contexts/          # React Context
│   │   └── AuthContext.jsx
│   ├── pages/             # Stranice
│   │   ├── Home/
│   │   ├── EmailCheck/
│   │   ├── Dashboard/
│   │   ├── PasswordAnalysis/
│   │   ├── Recommendations/
│   │   ├── Profile/
│   │   ├── Notifications/
│   │   └── Auth/
│   ├── services/          # API servisi
│   │   └── api.js
│   ├── App.jsx            # Main app komponenta
│   └── main.jsx            # Entry point
```

## Stranice

1. **Home** - Početna stranica sa quick actions
2. **Email Check** - Provera kompromitovanog email-a
3. **Dashboard** - Statistike breach podataka
4. **Password Analysis** - Analiza lozinke
5. **Recommendations** - Preporuke za bezbednost
6. **Profile** - Profil korisnika
7. **Notifications** - Notifikacije

## Environment Variables

Kreiraj `.env` fajl:

```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## API Integracija

Frontend komunicira sa backend API-jem preko Axios. Sve API pozive možete pronaći u `src/services/api.js`.
