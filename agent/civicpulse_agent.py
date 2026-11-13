import re
import uuid
from datetime import datetime

from agent.classifier import classify_complaint
from agent.department_router import recommend_department


# ------------------------------------------
# Priority rules (simple, transparent, editable)
# ------------------------------------------

HIGH_PRIORITY_KEYWORDS = [
    "accident", "injured", "injury", "emergency", "danger",
    "gas leak", "fire", "electric shock", "live wire", "exposed wire",
    "collapse", "flood", "sewage overflow", "open manhole", "burst",
    "no water", "hospital", "school", "children",
]

MEDIUM_PRIORITY_KEYWORDS = [
    "pothole", "huge", "large", "broken", "damaged", "not working",
    "blocked", "clogged", "leak", "overflow", "garbage", "stagnant",
    "for days", "weeks",
]


def detect_priority(complaint):
    """
    Rule-based urgency check.
    Returns (priority_level, keyword_that_triggered_it).
    """
    text = complaint.lower()

    for level, keywords in (
        ("High", HIGH_PRIORITY_KEYWORDS),
        ("Medium", MEDIUM_PRIORITY_KEYWORDS),
    ):
        for keyword in keywords:
            # \b at the start so "accidents" still matches "accident"
            if re.search(rf"\b{re.escape(keyword)}", text):
                return level, keyword

    return "Low", ""


def generate_ticket_id():
    return f"CP-{datetime.now().year}-{uuid.uuid4().hex[:6].upper()}"


def process_complaint(complaint):

    # Step 1: Classify complaint using ML
    classification = classify_complaint(complaint)

    if "error" in classification:
        return classification

    category = classification["predicted_category"]

    # Step 2: Recommend responsible department
    department = recommend_department(category)

    # Step 3: Assess urgency
    priority, priority_reason = detect_priority(complaint)

    # Step 4: Prepare decision-support output
    result = {
        "complaint": complaint,
        "category": category,
        "recommended_department": department,
        "confidence": classification.get("confidence"),
        "priority": priority,
        "priority_reason": priority_reason,
        "ticket_id": generate_ticket_id(),
        "submitted_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "status": "Ready for review"
    }

    return result


if __name__ == "__main__":

    complaint = "A huge pothole has formed on our road."

    decision = process_complaint(complaint)

    print("\n===== CIVICPULSE REPORT =====")

    for key, value in decision.items():
        print(f"{key}: {value}")