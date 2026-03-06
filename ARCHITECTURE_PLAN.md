# Plan Arhitekture Sistema za Analizu Kompromitovanih Kredencijala

## 1. Pregled Sistema

### 1.1 Opis
Sistem za prikupljanje, analizu i upravljanje kompromitovanim kredencijalima iz javno dostupnih breach baza podataka. Sistem koristi AI/ML modele za analizu obrazaca, detekciju slabih lozinki i generisanje preporuka za poboljšanje bezbednosti.

### 1.2 Glavne Funkcionalnosti
- Prikupljanje breach podataka (HaveIBeenPwned API + web scraping)
- Analiza kompromitovanih kredencijala
- Detekcija slabih lozinki
- Procena rizika kredencijala
- Generisanje preporuka za bezbednost
- Provera kompromitovanosti email adresa
- Analiza trendova breach incidenata
- Notifikacioni sistem

---

## 2. Arhitektura Sistema

### 2.1 Clean Architecture Principi

Sistem će biti organizovan u slojeve prema Clean Architecture principima:

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                   │
│              (React Frontend + REST API)                 │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│                   Application Layer                      │
│         (Use Cases / Business Logic)                     │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│                    Domain Layer                          │
│         (Entities, Value Objects, Interfaces)            │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│                 Infrastructure Layer                     │
│  (Database, External APIs, ML Models, Notifications)     │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Modulna Struktura

Sistem će biti podeljen u nezavisne module:
- **Data Collection Module** - prikupljanje podataka
- **Analysis Module** - AI/ML analiza
- **Risk Assessment Module** - procena rizika
- **User Management Module** - upravljanje korisnicima
- **Notification Module** - notifikacije
- **Reporting Module** - izveštaji i trendovi

---

## 3. Backend Arhitektura (Python)

### 3.1 Struktura Direktorijuma

```
backend/
├── src/
│   ├── domain/                    # Domain Layer
│   │   ├── entities/
│   │   │   ├── breach.py
│   │   │   ├── credential.py
│   │   │   ├── user.py
│   │   │   └── notification.py
│   │   ├── value_objects/
│   │   │   ├── email.py
│   │   │   ├── password_strength.py
│   │   │   └── risk_score.py
│   │   └── repositories/          # Repository Interfaces
│   │       ├── breach_repository.py
│   │       ├── credential_repository.py
│   │       └── user_repository.py
│   │
│   ├── application/               # Application Layer
│   │   ├── use_cases/
│   │   │   ├── data_collection/
│   │   │   │   ├── collect_hibp_data.py
│   │   │   │   ├── scrape_breach_data.py
│   │   │   │   └── sync_breach_database.py
│   │   │   ├── analysis/
│   │   │   │   ├── analyze_credentials.py
│   │   │   │   ├── detect_weak_passwords.py
│   │   │   │   └── generate_recommendations.py
│   │   │   ├── risk_assessment/
│   │   │   │   ├── assess_credential_risk.py
│   │   │   │   └── calculate_risk_score.py
│   │   │   ├── user_management/
│   │   │   │   ├── check_email_breach.py
│   │   │   │   ├── register_user.py
│   │   │   │   └── get_user_breaches.py
│   │   │   ├── notifications/
│   │   │   │   ├── send_breach_alert.py
│   │   │   │   └── send_recommendations.py
│   │   │   └── reporting/
│   │   │       ├── analyze_breach_trends.py
│   │   │       └── generate_statistics.py
│   │   └── services/
│   │       ├── ml_service.py
│   │       ├── password_analyzer_service.py
│   │       └── risk_calculator_service.py
│   │
│   ├── infrastructure/            # Infrastructure Layer
│   │   ├── database/
│   │   │   ├── models/            # ORM Models
│   │   │   │   ├── breach_model.py
│   │   │   │   ├── credential_model.py
│   │   │   │   └── user_model.py
│   │   │   ├── repositories/     # Repository Implementations
│   │   │   │   ├── breach_repository_impl.py
│   │   │   │   ├── credential_repository_impl.py
│   │   │   │   └── user_repository_impl.py
│   │   │   └── database.py       # DB Connection & Setup
│   │   │
│   │   ├── external_apis/
│   │   │   ├── hibp_client.py     # HaveIBeenPwned API
│   │   │   └── breach_scraper.py  # Web Scraping
│   │   │
│   │   ├── ml/
│   │   │   ├── models/
│   │   │   │   ├── password_classifier.py
│   │   │   │   ├── risk_predictor.py
│   │   │   │   └── pattern_analyzer.py
│   │   │   ├── training/
│   │   │   │   └── train_models.py
│   │   │   └── features/
│   │   │       └── feature_extractor.py
│   │   │
│   │   └── notifications/
│   │       ├── email_service.py
│   │       └── notification_queue.py
│   │
│   ├── api/                       # Presentation Layer
│   │   ├── routes/
│   │   │   ├── breach_routes.py
│   │   │   ├── credential_routes.py
│   │   │   ├── user_routes.py
│   │   │   ├── analysis_routes.py
│   │   │   └── reporting_routes.py
│   │   ├── middleware/
│   │   │   ├── auth_middleware.py
│   │   │   ├── error_handler.py
│   │   │   └── rate_limiter.py
│   │   ├── schemas/               # Request/Response Schemas
│   │   │   ├── breach_schemas.py
│   │   │   ├── credential_schemas.py
│   │   │   └── user_schemas.py
│   │   └── main.py                # FastAPI/Flask App
│   │
│   └── config/
│       ├── settings.py
│       └── dependencies.py        # Dependency Injection
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── scripts/
│   ├── data_collection_scheduler.py
│   └── ml_training_pipeline.py
│
├── requirements.txt
└── README.md
```

### 3.2 SOLID Principi Implementacija

#### Single Responsibility Principle (SRP)
- Svaki modul ima jednu odgovornost
- Use cases su odvojeni (npr. `collect_hibp_data.py` samo prikuplja podatke)
- Servisi su fokusirani (npr. `password_analyzer_service.py` samo analizira lozinke)

#### Open/Closed Principle (OCP)
- Repository interfejsi u domain layer-u
- Konkretne implementacije u infrastructure layer-u
- Lako dodavanje novih data source-ova bez menjanja postojećeg koda

#### Liskov Substitution Principle (LSP)
- Sve repository implementacije implementiraju iste interfejse
- Različiti ML modeli implementiraju zajednički interfejs

#### Interface Segregation Principle (ISP)
- Specifični interfejsi za različite operacije
- Nema "fat" interfejsa sa mnogo metoda

#### Dependency Inversion Principle (DIP)
- High-level moduli zavise od abstrakcija (interfejsi)
- Dependency Injection kroz `dependencies.py`
- Use cases zavise od repository interfejsa, ne implementacija

### 3.3 Tehnologije i Biblioteke

- **Web Framework**: FastAPI (brz, modern, automatska dokumentacija)
- **ORM**: SQLAlchemy (za PostgreSQL) ili odmongo (za MongoDB)
- **HTTP Client**: httpx ili requests
- **Web Scraping**: BeautifulSoup4, Scrapy
- **ML/AI**: pandas, scikit-learn, numpy
- **Task Queue**: Celery (za asinhronne zadatke)
- **Scheduler**: APScheduler
- **Validation**: Pydantic
- **Testing**: pytest, pytest-asyncio

---

## 4. Frontend Arhitektura (React)

### 4.1 Struktura Direktorijuma

```
frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── common/                # Reusable components
│   │   │   ├── Button/
│   │   │   ├── Input/
│   │   │   ├── Card/
│   │   │   ├── Modal/
│   │   │   └── LoadingSpinner/
│   │   ├── layout/
│   │   │   ├── Header/
│   │   │   ├── Sidebar/
│   │   │   └── Footer/
│   │   ├── breach/
│   │   │   ├── BreachCard/
│   │   │   ├── BreachList/
│   │   │   └── BreachDetails/
│   │   ├── credential/
│   │   │   ├── CredentialCheck/
│   │   │   ├── PasswordStrength/
│   │   │   └── RiskIndicator/
│   │   ├── analysis/
│   │   │   ├── TrendChart/
│   │   │   ├── StatisticsPanel/
│   │   │   └── RecommendationsList/
│   │   └── notifications/
│   │       └── NotificationCenter/
│   │
│   ├── pages/
│   │   ├── Home/
│   │   ├── CheckEmail/
│   │   ├── BreachDatabase/
│   │   ├── Analysis/
│   │   ├── Trends/
│   │   └── Settings/
│   │
│   ├── services/
│   │   ├── api/
│   │   │   ├── breachApi.js
│   │   │   ├── credentialApi.js
│   │   │   ├── userApi.js
│   │   │   └── analysisApi.js
│   │   └── auth/
│   │       └── authService.js
│   │
│   ├── hooks/
│   │   ├── useBreachData.js
│   │   ├── useCredentialCheck.js
│   │   ├── useAnalysis.js
│   │   └── useNotifications.js
│   │
│   ├── store/                     # State Management (Redux/Zustand)
│   │   ├── slices/
│   │   │   ├── breachSlice.js
│   │   │   ├── userSlice.js
│   │   │   └── notificationSlice.js
│   │   └── store.js
│   │
│   ├── utils/
│   │   ├── formatters.js
│   │   ├── validators.js
│   │   └── constants.js
│   │
│   ├── styles/
│   │   ├── global.css
│   │   └── themes/
│   │
│   ├── App.jsx
│   ├── index.jsx
│   └── routes.jsx
│
├── package.json
└── README.md
```

### 4.2 Komponente i Funkcionalnosti

#### Glavne Stranice:
1. **Home** - Dashboard sa pregledom statistika
2. **CheckEmail** - Forma za proveru email adrese
3. **BreachDatabase** - Lista svih breach-ova sa filtriranjem
4. **Analysis** - Detaljna analiza kredencijala i preporuke
5. **Trends** - Grafikoni trendova breach incidenata
6. **Settings** - Korisničke postavke i notifikacije

#### State Management:
- Redux Toolkit ili Zustand za globalno stanje
- React Query za server state i caching

### 4.3 Tehnologije

- **Framework**: React 18+
- **Routing**: React Router v6
- **State Management**: Redux Toolkit ili Zustand
- **Data Fetching**: React Query (TanStack Query)
- **UI Library**: Material-UI ili Tailwind CSS
- **Charts**: Recharts ili Chart.js
- **Forms**: React Hook Form
- **HTTP Client**: Axios
- **Build Tool**: Vite

---

## 5. Baza Podataka

### 5.1 Preporuka: PostgreSQL

**Razlozi:**
- Relaciona struktura podataka (breach-ovi, kredencijali, korisnici)
- ACID transakcije za kritične operacije
- Napredne SQL funkcionalnosti za analitiku
- JSON podrška za fleksibilne strukture (ML features)
- Odlična performansa za kompleksne upite
- Zrelost i stabilnost

### 5.2 Alternativa: MongoDB

**Kada bi se koristio:**
- Ako su podaci veoma nestrukturirani
- Ako je potrebna brza skalabilnost
- Ako se često menjaju šeme

**Preporuka**: PostgreSQL je bolji izbor za ovaj projekat zbog relacione prirode podataka.

### 5.3 Šema Baze Podataka

#### Tabela: `breaches`
```sql
CREATE TABLE breaches (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255),
    breach_date DATE,
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP,
    pwn_count INTEGER,
    description TEXT,
    data_classes TEXT[],  -- Array of compromised data types
    is_verified BOOLEAN,
    is_fabricated BOOLEAN,
    is_sensitive BOOLEAN,
    is_retired BOOLEAN,
    is_spam_list BOOLEAN,
    logo_path VARCHAR(500),
    source VARCHAR(100),  -- 'hibp', 'scraped', etc.
    metadata JSONB
);
```

#### Tabela: `credentials`
```sql
CREATE TABLE credentials (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255),  -- SHA-1 hash (from HIBP)
    breach_id INTEGER REFERENCES breaches(id),
    discovered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    password_strength_score INTEGER,  -- 0-100
    risk_score DECIMAL(5,2),  -- 0.00-10.00
    is_weak BOOLEAN,
    pattern_type VARCHAR(50),  -- 'common', 'dictionary', 'sequential', etc.
    ml_features JSONB,  -- Extracted features for ML
    recommendations TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE INDEX idx_credentials_email ON credentials(email);
CREATE INDEX idx_credentials_breach_id ON credentials(breach_id);
CREATE INDEX idx_credentials_risk_score ON credentials(risk_score);
```

#### Tabela: `users`
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    notification_preferences JSONB,  -- Email, SMS, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    last_login TIMESTAMP
);
```

#### Tabela: `user_breaches`
```sql
CREATE TABLE user_breaches (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    breach_id INTEGER REFERENCES breaches(id),
    credential_id INTEGER REFERENCES credentials(id),
    notified_at TIMESTAMP,
    notification_sent BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, breach_id)
);

CREATE INDEX idx_user_breaches_user_id ON user_breaches(user_id);
CREATE INDEX idx_user_breaches_breach_id ON user_breaches(breach_id);
```

#### Tabela: `notifications`
```sql
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    type VARCHAR(50) NOT NULL,  -- 'breach_alert', 'recommendation', 'trend_update'
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    priority VARCHAR(20) DEFAULT 'normal',  -- 'low', 'normal', 'high', 'critical'
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);
```

#### Tabela: `breach_statistics`
```sql
CREATE TABLE breach_statistics (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    total_breaches INTEGER DEFAULT 0,
    new_breaches INTEGER DEFAULT 0,
    total_credentials INTEGER DEFAULT 0,
    new_credentials INTEGER DEFAULT 0,
    avg_risk_score DECIMAL(5,2),
    weak_password_percentage DECIMAL(5,2),
    top_data_classes TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date)
);
```

#### Tabela: `ml_model_versions`
```sql
CREATE TABLE ml_model_versions (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    accuracy_score DECIMAL(5,4),
    training_date TIMESTAMP,
    is_active BOOLEAN DEFAULT FALSE,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 6. AI/ML Komponente

### 6.1 Modeli

#### 6.1.1 Password Strength Classifier
- **Tip**: Classification (Weak/Medium/Strong)
- **Features**:
  - Dužina lozinke
  - Broj karaktera (velika, mala, brojevi, specijalni)
  - Učestalost u dictionary-ju
  - Obrasci (sequential, repeated, keyboard patterns)
  - Entropija
- **Algoritam**: Random Forest ili Gradient Boosting
- **Output**: Score 0-100 + klasifikacija

#### 6.1.2 Risk Score Predictor
- **Tip**: Regression
- **Features**:
  - Password strength score
  - Starost breach-a
  - Tip kompromitovanih podataka
  - Broj breach-ova za isti email
  - Verifikacija breach-a
- **Algoritam**: Gradient Boosting Regressor
- **Output**: Risk score 0.0-10.0

#### 6.1.3 Pattern Analyzer
- **Tip**: Pattern Recognition
- **Funkcionalnost**:
  - Detekcija common passwords
  - Detekcija dictionary words
  - Detekcija sekvencijalnih obrazaca
  - Detekcija keyboard patterns
- **Metod**: Rule-based + ML classification

### 6.2 Feature Engineering

```python
# Primer feature ekstrakcije
features = {
    'length': len(password),
    'has_uppercase': bool(re.search(r'[A-Z]', password)),
    'has_lowercase': bool(re.search(r'[a-z]', password)),
    'has_digits': bool(re.search(r'\d', password)),
    'has_special': bool(re.search(r'[!@#$%^&*]', password)),
    'entropy': calculate_entropy(password),
    'common_password': is_in_common_list(password),
    'dictionary_word': is_dictionary_word(password),
    'sequential_chars': has_sequential_pattern(password),
    'repeated_chars': has_repeated_pattern(password),
    'keyboard_pattern': has_keyboard_pattern(password)
}
```

### 6.3 Training Pipeline

1. **Data Collection**: Prikupljanje breach podataka
2. **Data Preprocessing**: Čišćenje i normalizacija
3. **Feature Extraction**: Ekstrakcija features
4. **Model Training**: Treniranje modela
5. **Validation**: Cross-validation i testiranje
6. **Model Deployment**: Čuvanje modela i verzionisanje
7. **Monitoring**: Praćenje performansi u produkciji

---

## 7. REST API Dizajn

### 7.1 Endpoint Struktura

#### Breach Endpoints
```
GET    /api/v1/breaches              # Lista svih breach-ova
GET    /api/v1/breaches/{id}         # Detalji breach-a
GET    /api/v1/breaches/search       # Pretraga breach-ova
POST   /api/v1/breaches/sync         # Sinhronizacija sa HIBP (admin)
```

#### Credential Endpoints
```
GET    /api/v1/credentials           # Lista kredencijala (sa filtriranjem)
GET    /api/v1/credentials/{id}      # Detalji kredencijala
POST   /api/v1/credentials/analyze   # Analiza kredencijala
GET    /api/v1/credentials/stats     # Statistike kredencijala
```

#### User Endpoints
```
POST   /api/v1/users/register        # Registracija korisnika
POST   /api/v1/users/login           # Login
GET    /api/v1/users/me              # Trenutni korisnik
POST   /api/v1/users/check-email     # Provera email adrese
GET    /api/v1/users/breaches        # Breach-ovi korisnika
PUT    /api/v1/users/settings        # Ažuriranje postavki
```

#### Analysis Endpoints
```
POST   /api/v1/analysis/password     # Analiza lozinke
GET    /api/v1/analysis/recommendations  # Preporuke za korisnika
GET    /api/v1/analysis/risk-score   # Procena rizika
```

#### Reporting Endpoints
```
GET    /api/v1/reports/trends        # Trendovi breach incidenata
GET    /api/v1/reports/statistics    # Statistike
GET    /api/v1/reports/dashboard     # Dashboard podaci
```

#### Notification Endpoints
```
GET    /api/v1/notifications         # Lista notifikacija korisnika
PUT    /api/v1/notifications/{id}/read  # Označi kao pročitano
DELETE /api/v1/notifications/{id}   # Obriši notifikaciju
```

### 7.2 Response Format

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

Error Response:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": { ... }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 7.3 Autentifikacija

- **JWT Tokens** za autentifikaciju
- **Refresh Tokens** za obnovu sesije
- **Rate Limiting** za zaštitu API-ja
- **API Keys** za admin operacije

---

## 8. Data Collection Mehanizmi

### 8.1 HaveIBeenPwned API Integracija

#### Endpoints:
- `GET /v3/breach/{name}` - Detalji breach-a
- `GET /v3/breachedaccount/{email}` - Breach-ovi za email
- `GET /v3/breaches` - Lista svih breach-ova
- `GET /v3/pasteaccount/{email}` - Paste-ovi za email

#### Implementacija:
- Rate limiting (HIBP ima ograničenja)
- Caching za smanjenje API poziva
- Retry mehanizam sa exponential backoff
- Batch processing za više email adresa

### 8.2 Web Scraping

#### Izvori:
- Javne breach baze (sa dozvolom)
- Pastebin monitoring (opciono)
- Dark web monitoring (opciono, zaštita)

#### Implementacija:
- Scrapy framework za scraping
- Respect robots.txt
- Rate limiting i delays
- Error handling i retry logika
- Data validation pre čuvanja

### 8.3 Scheduler

- **APScheduler** za periodične zadatke:
  - Dnevna sinhronizacija sa HIBP
  - Nedeljno skeniranje novih breach-ova
  - Mesečno treniranje ML modela
  - Dnevno generisanje statistika

---

## 9. Notifikacioni Sistem

### 9.1 Tipovi Notifikacija

1. **Breach Alert**: Novi breach detektovan za korisnika
2. **Risk Alert**: Visok risk score detektovan
3. **Recommendation**: Preporuke za poboljšanje bezbednosti
4. **Trend Update**: Periodični izveštaji o trendovima

### 9.2 Kanali

- **Email**: SMTP integracija
- **In-App**: Notifikacije u aplikaciji
- **SMS**: Opciono (Twilio)
- **Push Notifications**: Opciono (za mobilnu app)

### 9.3 Queue System

- **Celery** za asinhronne notifikacije
- **Redis** kao message broker
- Retry mehanizam za failed notifikacije
- Prioriteti (low, normal, high, critical)

---

## 10. Bezbednost

### 10.1 Zaštita Podataka

- **Password Hashing**: bcrypt ili Argon2
- **Email Hashing**: SHA-1 za HIBP kompatibilnost
- **Encryption**: Enkripcija osetljivih podataka u bazi
- **HTTPS**: Obavezno za sve komunikacije

### 10.2 API Bezbednost

- **Rate Limiting**: Zaštita od abuse-a
- **CORS**: Konfigurisan za frontend domen
- **Input Validation**: Pydantic schemas
- **SQL Injection Protection**: ORM sa parameterized queries
- **XSS Protection**: Sanitizacija input-a

### 10.3 Compliance

- **GDPR**: Pravo na brisanje podataka
- **Data Retention**: Politika čuvanja podataka
- **Privacy Policy**: Transparentnost o prikupljanju podataka

---

## 11. Deployment Arhitektura

### 11.1 Komponente

```
┌─────────────┐
│   React     │  (Frontend - Nginx)
│   Frontend  │
└─────────────┘
      ↕
┌─────────────┐
│   Nginx     │  (Reverse Proxy)
│   (SSL)     │
└─────────────┘
      ↕
┌─────────────┐
│   FastAPI   │  (Backend API)
│   Backend   │
└─────────────┘
      ↕
┌─────────────┐
│ PostgreSQL  │  (Database)
└─────────────┘
      ↕
┌─────────────┐
│   Redis     │  (Cache + Message Broker)
└─────────────┘
      ↕
┌─────────────┐
│   Celery    │  (Background Tasks)
│   Workers   │
└─────────────┘
```

### 11.2 Docker Containerizacija

- **docker-compose.yml** za lokalni development
- **Dockerfile** za svaki servis
- **.dockerignore** za optimizaciju build-a

### 11.3 Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Redis
REDIS_URL=redis://localhost:6379

# HIBP API
HIBP_API_KEY=your_api_key

# JWT
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email
SMTP_PASSWORD=your_password

# ML Models
ML_MODELS_PATH=/app/models
```

---

## 12. Testing Strategija

### 12.1 Backend Testing

- **Unit Tests**: pytest za use cases i servise
- **Integration Tests**: Testiranje API endpoints
- **ML Tests**: Testiranje modela sa test dataset-om
- **Coverage**: Minimum 80% code coverage

### 12.2 Frontend Testing

- **Unit Tests**: Jest + React Testing Library
- **Component Tests**: Testiranje React komponenti
- **E2E Tests**: Cypress ili Playwright

### 12.3 Test Data

- Mock HIBP API responses
- Test database sa sample podacima
- Fixtures za konzistentno testiranje

---

## 13. Monitoring i Logging

### 13.1 Logging

- **Structured Logging**: JSON format
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Aggregation**: ELK Stack ili Loki

### 13.2 Monitoring

- **Application Metrics**: Prometheus
- **Health Checks**: `/health` endpoint
- **Performance Monitoring**: APM tools
- **Error Tracking**: Sentry

### 13.3 Alerts

- Database connection issues
- API rate limit exceeded
- ML model accuracy drops
- High error rates

---

## 14. Razvojni Workflow

### 14.1 Git Workflow

- **Main Branch**: Production-ready kod
- **Develop Branch**: Integration branch
- **Feature Branches**: Nove funkcionalnosti
- **Hotfix Branches**: Hitne ispravke

### 14.2 CI/CD Pipeline

1. **Code Push** → Trigger pipeline
2. **Linting** → Code quality checks
3. **Tests** → Run test suite
4. **Build** → Docker image build
5. **Deploy** → Deploy to staging/production

---

## 15. Dokumentacija

### 15.1 API Dokumentacija

- **Swagger/OpenAPI**: Automatska dokumentacija (FastAPI)
- **Postman Collection**: Za testiranje
- **Examples**: Primeri request/response

### 15.2 Code Dokumentacija

- **Docstrings**: Python docstrings za sve funkcije/klase
- **Type Hints**: Type annotations za bolju dokumentaciju
- **README**: Setup i development instrukcije

### 15.3 User Dokumentacija

- **User Guide**: Kako koristiti aplikaciju
- **FAQ**: Često postavljana pitanja
- **Privacy Policy**: Politika privatnosti

---

## 16. Faze Implementacije

### Faza 1: Osnovna Infrastruktura (2-3 nedelje)
- Backend struktura (Clean Architecture)
- Database setup i migracije
- Osnovni API endpoints
- Frontend setup i routing

### Faza 2: Data Collection (2 nedelje)
- HIBP API integracija
- Web scraping mehanizmi
- Database storage
- Scheduler setup

### Faza 3: ML/AI Komponente (3-4 nedelje)
- Feature engineering
- Model training
- Password analysis
- Risk assessment

### Faza 4: User Features (2 nedelje)
- User registration/login
- Email check functionality
- User dashboard
- Breach listing

### Faza 5: Analysis & Reporting (2 nedelje)
- Trend analysis
- Statistics generation
- Recommendations engine
- Reporting dashboard

### Faza 6: Notifications (1 nedelja)
- Notification system
- Email service
- In-app notifications

### Faza 7: Testing & Polish (2 nedelje)
- Comprehensive testing
- Bug fixes
- Performance optimization
- Documentation

---

## 17. Zaključak

Ovaj plan arhitekture obezbeđuje:

✅ **Clean Architecture** - Jasna separacija slojeva
✅ **SOLID Principi** - Održiv i proširiv kod
✅ **Modularni Dizajn** - Nezavisni moduli
✅ **REST API** - Standardizovana komunikacija
✅ **Skalabilnost** - Spremno za rast
✅ **Bezbednost** - Zaštita podataka i API-ja
✅ **Testabilnost** - Lako testiranje komponenti
✅ **Održivost** - Jasna struktura i dokumentacija

Plan je spreman za implementaciju. Sledeći korak bi bio kreiranje osnovne strukture projekta i početak implementacije po fazama.
