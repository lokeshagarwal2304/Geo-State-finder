
# 🌍 Country Finder AI

An intelligent, AI-powered microservice for identifying countries from phone codes, names, or natural language queries. Built with Python (FastAPI) and modern web technologies.

## 🚀 Features

- **Multi-Modal Identification**:
  - Exact Phone Code Match (e.g., `+91`, `1`)
  - country Name Fuzzy Matching (e.g., `Inida` -> `India`)
  - Natural Language Intent (e.g., `code for Germany`)
- **Microservices Architecture**: decoupled frontend and backend.
- **Production-Ready**: FastAPI backend, Docker-ready structure, clean code.
- **Interactive UI**: Modern, responsive dashboard.

## 🛠️ Tech Stack

- **Backend**: Python 3.9+, FastAPI, Phonenumbers, PyCountry, TheFuzz (Levenshtein Distance)
- **Frontend**: HTML5, Tailwind CSS, JavaScript (ES6+)
- **AI/ML**: Fuzzy Logic, NLP Heuristics

## 📂 Project Structure

```
country_finder/
├── backend/
│   ├── core/
│   │   └── country_service.py  # Core AI Logic
│   ├── main.py                 # FastAPI Entry Point
│   └── requirements.txt        # Dependencies
└── frontend/
    ├── index.html              # UI
    ├── style.css               # Styles
    └── script.js               # Logic
```

## ⚡ Quick Start

### 1. Backend Setup
1. Navigate to `backend`:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
   Server will start at `http://localhost:8000`

### 2. Frontend Setup
1. Open `frontend/index.html` in your browser.
2. Ensure the backend is running.
3. Type a code (`+44`) or query (`Japan code`) to see results!

## 🧠 How It Works

1. **Input Normalization**: Cleans user input (removes extra spaces, sanitizes format).
2. **Regex Analysis**: Checks if input is a numeric code.
3. **Phonenumbers Library**: If numeric, queries the Google `libphonenumber` database for precise region matching.
4. **Fuzzy Logic (TheFuzz)**: If text, calculates Levenshtein distance against a dataset of country names to correct typos.
5. **NLP Heuristics**: Extracts intent from phrases like "dialing code for X".

## 🛡️ API Endpoints

- `POST /predict`
  - Body: `{"input": "string", "deep_search": boolean}`
  - Response: `{"country": "India", "code": "+91", "state": "Delhi", "carrier": "Airtel", ...}`

## 🔑 Configuration (Optional)

### Truecaller Integration
To use Truecaller for name lookup:
1. Run `python setup_truecaller.py` to login and generate `truecaller_auth.json`.

### Numverify Integration
To use Numverify for detailed location/carrier info:
1. Set `NUMVERIFY_API_KEY` environment variable.
2. Or update `backend/core/numverify_handler.py` directly.

## 🔮 Future Improvements

- Add a flag image dataset (SVG) locally instead of Emoji.
- Train a proper Named Entity Return (NER) model for complex queries.
- Deploy effectively using Docker/Kubernetes.

---
*Created by Lokesh Agarwal*
