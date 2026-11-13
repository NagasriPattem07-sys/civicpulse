import joblib
import numpy as np

# Load the trained ML pipeline
model = joblib.load("models/citizen_complaint_model.pkl")

# Sharpness of the confidence curve (higher = more decisive scores)
CONFIDENCE_SCALE = 3.0


def get_confidence(complaint):
    """
    Returns model confidence (0-100) for the predicted category,
    or None if the model can't provide scores.

    - If the model has predict_proba, use it directly.
    - Otherwise (plain Linear SVM) convert decision scores with a
      softmax. This is a RELATIVE score, not a calibrated probability.
    """
    try:
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba([complaint])[0]
            return round(float(np.max(probs)) * 100, 1)

        scores = np.atleast_1d(model.decision_function([complaint])[0])

        if scores.size == 1:
            # Binary case: squash the single margin into 0-1
            conf = 1 / (1 + np.exp(-CONFIDENCE_SCALE * abs(scores[0])))
        else:
            z = CONFIDENCE_SCALE * scores
            z = z - np.max(z)  # numerical stability
            probs = np.exp(z) / np.sum(np.exp(z))
            conf = np.max(probs)

        return round(float(conf) * 100, 1)

    except Exception:
        return None


def classify_complaint(complaint):
    if not complaint or not complaint.strip():
        return {
            "error": "Please enter a complaint."
        }

    prediction = model.predict([complaint])[0]

    return {
        "complaint": complaint,
        "predicted_category": prediction,
        "confidence": get_confidence(complaint)
    }


# Test
if __name__ == "__main__":
    result = classify_complaint(
        "A huge pothole has formed on our road."
    )

    print(result)