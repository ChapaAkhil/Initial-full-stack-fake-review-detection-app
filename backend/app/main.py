import logging
import os

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    AnalyzeReviewsRequest,
    ManualReview,
    SampleReviewsResponse,
)
from .scraper import fetch_reviews, ScrapeError
from .features import build_features
from .model import ModelArtifacts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fake-review-app")

MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")
VECTORIZER_PATH = os.getenv("VECTORIZER_PATH", "vectorizer.pkl")
MAX_PAGES = int(os.getenv("MAX_PAGES", "5"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "20"))

app = FastAPI(title="Fake Review Detector", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    artifacts = ModelArtifacts(MODEL_PATH, VECTORIZER_PATH)
except Exception as exc:
    logger.exception("Failed to load model artifacts: %s", exc)
    artifacts = None


@app.get("/health")
def health():
    if artifacts is None:
        return {"status": "error", "detail": "Model artifacts not loaded"}
    return {"status": "ok"}


def _build_response(df: pd.DataFrame, product_id: str) -> AnalyzeResponse:
    features_df = build_features(df, product_id)

    preds = artifacts.predict(features_df)
    total_reviews = len(preds)
    if total_reviews == 0:
        raise HTTPException(status_code=404, detail="No reviews provided for analysis.")

    fake_count = artifacts.count_fake(preds)
    genuine_count = total_reviews - fake_count

    fake_pct = (fake_count / total_reviews) * 100
    genuine_pct = (genuine_count / total_reviews) * 100

    return AnalyzeResponse(
        fake_reviews_percentage=round(fake_pct, 2),
        genuine_reviews_percentage=round(genuine_pct, 2),
        total_reviews=total_reviews,
    )


def _ensure_artifacts_loaded():
    if artifacts is None:
        raise HTTPException(status_code=500, detail="Model artifacts are not loaded.")


def _reviews_to_dataframe(reviews):
    rows = []
    for review in reviews:
        if isinstance(review, ManualReview):
            review_data = review.dict()
        else:
            review_data = dict(review)

        helpful_votes = review_data.get("helpful_votes") or 0
        helpful_num = (
            review_data.get("helpfulness_numerator")
            if review_data.get("helpfulness_numerator") is not None
            else helpful_votes
        )
        helpful_den = (
            review_data.get("helpfulness_denominator")
            if review_data.get("helpfulness_denominator") is not None
            else helpful_votes
        )

        rows.append(
            {
                "review_text": review_data.get("review_text", ""),
                "rating": review_data.get("rating", 0),
                "helpfulness_numerator": helpful_num,
                "helpfulness_denominator": helpful_den,
                "timestamp": review_data.get("timestamp"),
                "reviewer_id": review_data.get("reviewer_id"),
            }
        )

    return pd.DataFrame(rows)


def _sample_reviews():
    return [
        ManualReview(
            review_text="Fantastic quality and comfortable fit. Would buy again!",
            rating=5,
            helpful_votes=4,
            timestamp="2024-03-01",
            reviewer_id="user_103",
        ),
        ManualReview(
            review_text="The product is okay, but delivery was delayed.",
            rating=3,
            helpful_votes=1,
            timestamp="2024-03-05",
            reviewer_id="user_204",
        ),
        ManualReview(
            review_text="Terrible quality, stitching came off in a week.",
            rating=1,
            helpful_votes=2,
            timestamp="2024-03-07",
            reviewer_id="user_501",
        ),
        ManualReview(
            review_text="Looks premium and matches the description perfectly.",
            rating=4,
            helpful_votes=0,
            timestamp="2024-03-08",
            reviewer_id="user_777",
        ),
    ]


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest):
    return analyze_url(payload)


@app.post("/analyze-url", response_model=AnalyzeResponse)
def analyze_url(payload: AnalyzeRequest):
    _ensure_artifacts_loaded()

    try:
        reviews, product_id = fetch_reviews(
            str(payload.product_url), max_pages=MAX_PAGES, timeout=REQUEST_TIMEOUT
        )
    except ScrapeError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected scrape error: {exc}")

    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this product.")

    df = pd.DataFrame(reviews)
    return _build_response(df, product_id)


@app.post("/analyze-reviews", response_model=AnalyzeResponse)
def analyze_reviews(payload: AnalyzeReviewsRequest):
    _ensure_artifacts_loaded()

    if not payload.reviews:
        raise HTTPException(status_code=400, detail="No manual reviews provided.")

    df = _reviews_to_dataframe(payload.reviews)
    return _build_response(df, "manual_input")


@app.get("/sample-reviews", response_model=SampleReviewsResponse)
def sample_reviews():
    return SampleReviewsResponse(reviews=_sample_reviews())


@app.post("/analyze-sample", response_model=AnalyzeResponse)
def analyze_sample():
    _ensure_artifacts_loaded()
    df = _reviews_to_dataframe(_sample_reviews())
    return _build_response(df, "sample_input")
