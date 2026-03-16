import logging
import os
from typing import Any

import joblib
from scipy.sparse import hstack

from .features import NUM_FEATURES

logger = logging.getLogger(__name__)


class ModelArtifacts:
    def __init__(self, model_path: str, vectorizer_path: str):
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        self.fake_label = self._infer_fake_label()

    def _infer_fake_label(self) -> Any:
        env_label = os.getenv("FAKE_LABEL")
        if env_label is not None:
            return self._coerce_label(env_label)

        classes = list(getattr(self.model, "classes_", []))
        lowered = [str(c).lower() for c in classes]

        if "fake" in lowered and "genuine" in lowered:
            return classes[lowered.index("fake")]

        if set(classes) >= {0, 1}:
            return 1

        if classes:
            logger.warning("Unknown class labels. Defaulting fake label to last class: %s", classes[-1])
            return classes[-1]

        raise ValueError("Model classes are missing; cannot infer fake label.")

    def _coerce_label(self, value: str) -> Any:
        try:
            return int(value)
        except ValueError:
            return value

    def predict(self, df):
        X_text = self.vectorizer.transform(df["review_text"])
        X_num = df[NUM_FEATURES].fillna(0).values
        X = hstack([X_text, X_num])
        return self.model.predict(X)

    def count_fake(self, preds) -> int:
        return int((preds == self.fake_label).sum())
