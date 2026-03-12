import { useState } from "react";

const initialReview = {
  review_text: "",
  rating: "5",
  helpful_votes: "0",
  timestamp: "",
  reviewer_id: "",
};

export default function ManualReviewInput({ onRun, isLoading }) {
  const [review, setReview] = useState(initialReview);
  const [reviews, setReviews] = useState([]);
  const [error, setError] = useState("");

  const updateField = (field, value) => {
    setReview((prev) => ({ ...prev, [field]: value }));
  };

  const handleAddReview = () => {
    if (!review.review_text.trim()) {
      setError("Review text is required.");
      return;
    }

    const newReview = {
      review_text: review.review_text.trim(),
      rating: Number(review.rating),
      helpful_votes: Number(review.helpful_votes || 0),
      timestamp: review.timestamp || null,
      reviewer_id: review.reviewer_id.trim() || "anonymous",
    };

    setReviews((prev) => [...prev, newReview]);
    setReview(initialReview);
    setError("");
  };

  const handleRun = async () => {
    if (reviews.length === 0) {
      setError("Add at least one review before running detection.");
      return;
    }
    setError("");
    await onRun(reviews).catch((err) => {
      const detail = err?.response?.data?.detail;
      setError(detail || err?.message || "Failed to analyze manual reviews.");
    });
  };

  return (
    <section className="mt-10">
      <div className="glass-card p-6">
        <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="section-subtitle">Manual Review Input</p>
            <h3 className="section-title mt-2">Add Reviews for Testing</h3>
          </div>
          <span className="text-xs text-white/60">Reviews added: {reviews.length}</span>
        </div>

        <div className="mt-6 grid gap-4 md:grid-cols-2">
          <textarea
            className="input-field min-h-[120px] md:col-span-2"
            placeholder="Review Text"
            value={review.review_text}
            onChange={(event) => updateField("review_text", event.target.value)}
          />
          <select
            className="input-field"
            value={review.rating}
            onChange={(event) => updateField("rating", event.target.value)}
          >
            {[1, 2, 3, 4, 5].map((value) => (
              <option key={value} value={value}>
                Rating: {value}
              </option>
            ))}
          </select>
          <input
            className="input-field"
            type="number"
            min="0"
            placeholder="Helpful Votes"
            value={review.helpful_votes}
            onChange={(event) => updateField("helpful_votes", event.target.value)}
          />
          <input
            className="input-field"
            type="date"
            value={review.timestamp}
            onChange={(event) => updateField("timestamp", event.target.value)}
          />
          <input
            className="input-field"
            placeholder="Reviewer ID"
            value={review.reviewer_id}
            onChange={(event) => updateField("reviewer_id", event.target.value)}
          />
        </div>

        <div className="mt-6 flex flex-wrap gap-3">
          <button className="secondary-button" onClick={handleAddReview}>
            Add Review
          </button>
          <button className="primary-button" onClick={handleRun} disabled={isLoading}>
            {isLoading ? "Running..." : "Run Fake Review Detection"}
          </button>
        </div>

        {error && <p className="mt-3 text-sm text-red-300">{error}</p>}
      </div>
    </section>
  );
}
