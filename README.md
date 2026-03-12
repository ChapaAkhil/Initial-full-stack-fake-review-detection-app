# Fake Product Review Detection System

Final Year Project: Machine Learning based detection of genuine vs fake product reviews.

## Overview

This full-stack app analyzes review text and behavioral signals (rating patterns, helpful votes, reviewer activity, burstiness) to estimate review authenticity. It supports:

- Product URL input (best-effort scraping for future support)
- Manual review input (reliable for demos and testing)

## Project Structure

```
backend/
  app/
    __init__.py
    features.py
    main.py
    model.py
    schemas.py
    scraper.py
  .env.example
  requirements.txt
frontend/
  src/
    components/
      Header.jsx
      ManualReviewInput.jsx
      Overview.jsx
      Results.jsx
      URLAnalyzer.jsx
    pages/
      Dashboard.jsx
    api.js
    App.jsx
    main.jsx
    styles.css
  index.html
  package.json
  postcss.config.js
  tailwind.config.js
```

## Backend Setup (Local)

1. Put your model files in `backend/`:
   - `model.pkl`
   - `vectorizer.pkl`

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the API:

```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Backend Endpoints

- `GET /health`
- `POST /analyze-url`
- `POST /analyze-reviews`
- `GET /sample-reviews`
- `POST /analyze-sample`

## Frontend Setup (Local)

1. Install dependencies:

```
npm install
```

2. Run the app:

```
npm run dev
```

Set the API URL if needed:

```
VITE_API_URL=http://localhost:8000
```

## Notes on Scraping

Many marketplaces block automated scraping. When blocked, the API returns a clear message and the UI recommends Manual Review Input. Manual input is the most reliable path for demos.

## Deployment (Free Tiers)

### Backend (Render)

1. Create a Web Service
2. Root directory: `backend`
3. Build:

```
pip install -r requirements.txt
```

4. Start:

```
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

5. Environment variables:

```
MODEL_PATH=model.pkl
VECTORIZER_PATH=vectorizer.pkl
```

### Frontend (Vercel)

1. Import the `frontend` folder
2. Build: `npm run build`
3. Output: `dist`
4. Env var:

```
VITE_API_URL=https://<your-backend-url>
```

## Model Files and GitHub

If `model.pkl` is large (near 100 MB), GitHub may reject it. Use Git LFS in that case.
