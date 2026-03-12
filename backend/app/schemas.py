from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator


class AnalyzeRequest(BaseModel):
    product_url: HttpUrl


class ManualReview(BaseModel):
    review_text: str = Field(..., min_length=1)
    rating: float = Field(..., ge=1, le=5)
    helpful_votes: Optional[int] = Field(0, ge=0)
    helpfulness_numerator: Optional[int] = Field(None, ge=0)
    helpfulness_denominator: Optional[int] = Field(None, ge=0)
    timestamp: Optional[str] = None
    reviewer_id: Optional[str] = None

    @field_validator("review_text")
    @classmethod
    def _strip_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("review_text cannot be empty")
        return cleaned

    @model_validator(mode="after")
    def _validate_helpfulness(self):
        if (
            self.helpfulness_numerator is not None
            and self.helpfulness_denominator is not None
            and self.helpfulness_numerator > self.helpfulness_denominator
        ):
            raise ValueError("helpfulness_numerator cannot be greater than helpfulness_denominator")

        return self


class AnalyzeReviewsRequest(BaseModel):
    reviews: List[ManualReview]


class SampleReviewsResponse(BaseModel):
    reviews: List[ManualReview]


class AnalyzeResponse(BaseModel):
    fake_reviews_percentage: float
    genuine_reviews_percentage: float
    total_reviews: int
