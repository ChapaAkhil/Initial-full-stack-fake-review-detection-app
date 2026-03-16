import numpy as np
import pandas as pd

NUM_FEATURES = [
    "rating",
    "pos_rating_pct",
    "review_len",
    "burstiness",
    "product_diversity",
    "rating_consistency",
    "helpful_ratio",
]


def clean_text(text: str) -> str:
    if pd.isna(text):
        return ""
    return str(text).lower().strip()


def _parse_datetime(series: pd.Series) -> pd.Series:
    if pd.api.types.is_datetime64_any_dtype(series):
        return series
    return pd.to_datetime(series, errors="coerce")


def _compute_burstiness(df: pd.DataFrame) -> pd.Series:
    df_sorted = df.sort_values(["reviewer_id", "timestamp"]).copy()

    def _burst_for_user(group: pd.DataFrame) -> pd.Series:
        if group["timestamp"].isna().all():
            return pd.Series([0] * len(group), index=group.index)

        group = group.set_index("timestamp")
        burst = group["review_text"].rolling("24H").count()
        burst = burst.reset_index(drop=True)
        burst.index = group.index
        return burst

    burstiness = df_sorted.groupby("reviewer_id", group_keys=False).apply(_burst_for_user)
    return burstiness.reindex(df.index).fillna(0)


def build_features(df: pd.DataFrame, product_id: str) -> pd.DataFrame:
    data = df.copy()

    data["review_text"] = data["review_text"].apply(clean_text)
    data["review_len"] = data["review_text"].apply(lambda x: len(x.split()))

    data["rating"] = pd.to_numeric(data["rating"], errors="coerce")
    rating_median = data["rating"].median()
    data["rating"] = data["rating"].fillna(rating_median if not np.isnan(rating_median) else 0)

    data["reviewer_id"] = data["reviewer_id"].fillna("").astype(str)
    missing_mask = data["reviewer_id"].str.strip() == ""
    data.loc[missing_mask, "reviewer_id"] = [f"anon_{i}" for i in data.index[missing_mask]]

    data["product_id"] = product_id
    data["timestamp"] = _parse_datetime(data["timestamp"])

    # Positive rating percentage per reviewer
    data["pos_rating_pct"] = data.groupby("reviewer_id")["rating"].transform(
        lambda x: (x >= 4).mean()
    )

    # Product diversity per reviewer
    data["product_diversity"] = data.groupby("reviewer_id")["product_id"].transform("nunique")

    # Rating consistency per reviewer
    data["rating_consistency"] = data.groupby("reviewer_id")["rating"].transform(
        lambda x: np.std(x, ddof=0)
    )

    # Helpful vote ratio
    def _helpful_ratio(row):
        denom = row.get("helpfulness_denominator", 0)
        num = row.get("helpfulness_numerator", 0)
        if not denom:
            return 0.0
        return float(num) / float(denom)

    data["helpful_ratio"] = data.apply(_helpful_ratio, axis=1)

    # Burstiness within 24 hours per reviewer
    data["burstiness"] = _compute_burstiness(data)

    return data
