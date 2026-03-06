# AI/ML Modul za Analizu Kredencijala

Kompletan ML modul za analizu kompromitovanih kredencijala sa naprednim feature engineering-om i risk scoring-om.

## Komponente

### 1. AdvancedFeatureExtractor
Napredna ekstrakcija features iz lozinki:
- **Basic Features**: dužina, karakteri (upper/lower/digits/special), brojevi
- **Complexity Features**: unique chars, char variety ratio, character types
- **Pattern Features**: sequential patterns, repeated chars, keyboard patterns
- **Dictionary Features**: common passwords, dictionary words, leet speak
- **Entropy Features**: Shannon entropy, entropy per char, effective length

### 2. CredentialRiskAnalyzer
ML model za analizu rizika:
- **Risk Score Prediction** (0-100): GradientBoostingRegressor
- **Weak Password Classification**: RandomForestClassifier
- **Feature Scaling**: StandardScaler za normalizaciju
- **Rule-based Fallback**: Ako modeli nisu trenirani

### 3. CredentialMLService
Servis za ML analizu kredencijala:
- Analiza pojedinačnih kredencijala
- Batch analiza
- Detekcija slabih lozinki
- Ažuriranje kredencijala sa analizom

## Feature Engineering

### Ekstrahovani Features (25 features):

1. **Basic Features**:
   - `length`: Dužina lozinke
   - `has_uppercase`: Ima velika slova (0/1)
   - `has_lowercase`: Ima mala slova (0/1)
   - `has_digits`: Ima brojeve (0/1)
   - `has_special`: Ima specijalne karaktere (0/1)
   - `digit_count`: Broj cifara
   - `special_count`: Broj specijalnih karaktera
   - `upper_count`: Broj velikih slova
   - `lower_count`: Broj malih slova

2. **Complexity Features**:
   - `unique_chars`: Broj jedinstvenih karaktera
   - `char_variety_ratio`: Odnos jedinstvenih/total karaktera
   - `char_types`: Broj tipova karaktera (0-4)
   - `repetition_ratio`: Odnos ponavljanja

3. **Pattern Features**:
   - `has_sequential`: Ima sekvencijalne obrasce (0/1)
   - `sequential_count`: Broj sekvencijalnih obrazaca
   - `repeated_chars`: Broj ponavljanja karaktera
   - `keyboard_patterns`: Broj keyboard obrazaca
   - `max_consecutive`: Maksimalno uzastopnih istih karaktera

4. **Dictionary Features**:
   - `is_common`: Je li common password (0/1)
   - `contains_dictionary_word`: Sadrži reč iz rečnika (0/1)
   - `dictionary_word_count`: Broj reči iz rečnika
   - `has_leet`: Ima leet speak (0/1)

5. **Entropy Features**:
   - `entropy`: Shannon entropy
   - `entropy_per_char`: Entropy po karakteru
   - `effective_length`: Efektivna dužina (based on charset)

## Risk Score (0-100)

- **0-32**: LOW risk
- **33-65**: MEDIUM risk
- **66-100**: HIGH risk

## Korišćenje

### API Endpoints

#### Analiza lozinke
```bash
POST /api/v1/ml-analysis/analyze-password
Authorization: Bearer <token>
Content-Type: application/json

{
  "password": "MyPassword123",
  "email": "user@example.com",
  "breach_count": 1
}
```

Response:
```json
{
  "risk_score": 45.5,
  "risk_level": "MEDIUM",
  "is_weak": false,
  "recommendations": [
    "Add special characters",
    "Use at least 12 characters"
  ],
  "features": { ... }
}
```

#### Analiza kredencijala
```bash
POST /api/v1/ml-analysis/analyze-credential/{credential_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "password": "MyPassword123"
}
```

#### Detekcija slabih lozinki
```bash
POST /api/v1/ml-analysis/detect-weak-passwords
Authorization: Bearer <token>
Content-Type: application/json

{
  "credential_ids": ["uuid1", "uuid2"],
  "passwords": ["password1", "password2"]
}
```

### Python Usage

```python
from src.infrastructure.ml.models.credential_risk_analyzer import CredentialRiskAnalyzer

analyzer = CredentialRiskAnalyzer()

# Analiza lozinke
result = analyzer.analyze_credential(
    password="MyPassword123",
    email="user@example.com",
    breach_count=1
)

print(f"Risk Score: {result['risk_score']}")
print(f"Risk Level: {result['risk_level']}")
print(f"Recommendations: {result['recommendations']}")
```

## Training Models

### Treniranje sa sintetičkim podacima

```bash
python -m src.infrastructure.ml.training.train_models
```

### Treniranje sa CSV fajlom

CSV format:
```csv
password,risk_score,is_weak
password123,85.0,True
SecurePass123!,15.0,False
```

```python
from src.infrastructure.ml.training.train_models import train_models_from_csv

await train_models_from_csv("training_data.csv")
```

### Treniranje sa custom podacima

```python
from src.infrastructure.ml.models.credential_risk_analyzer import CredentialRiskAnalyzer

analyzer = CredentialRiskAnalyzer()

passwords = ["password1", "Secure123!", ...]
risk_scores = [85.0, 15.0, ...]
is_weak = [True, False, ...]

analyzer.train_models(passwords, risk_scores, is_weak)
```

## Preporuke

Model generiše personalizovane preporuke na osnovu analize:

- **Kritične**: "⚠️ CRITICAL: Change this password immediately!"
- **Dužina**: "Use at least 12 characters (currently 8)"
- **Karakteri**: "Add uppercase letters, numbers"
- **Common passwords**: "Avoid using common passwords"
- **Dictionary words**: "Avoid dictionary words - use random combinations"
- **Patterns**: "Avoid sequential patterns (e.g., 12345, abcde)"
- **Entropy**: "Increase password complexity to improve entropy"

## Model Performance

- **Risk Predictor**: GradientBoostingRegressor (100 estimators)
- **Weak Password Classifier**: RandomForestClassifier (100 estimators)
- **Feature Scaling**: StandardScaler za normalizaciju

## Napomene

1. **Password Availability**: Za punu analizu potreban je plain text password. Ako je dostupan samo hash, analiza je ograničena.

2. **Training Data**: U produkciji koristite stvarne breach podatke za treniranje modela.

3. **Model Persistence**: Modeli se čuvaju u `models/` direktorijumu (konfigurisano u settings).

4. **Rule-based Fallback**: Ako modeli nisu trenirani, koristi se rule-based pristup.

## Fajlovi

- `advanced_feature_extractor.py` - Napredna ekstrakcija features
- `credential_risk_analyzer.py` - ML model za risk analizu
- `credential_ml_service.py` - Servis za ML analizu
- `train_models.py` - Training script
- `ml_analysis_routes.py` - API routes
