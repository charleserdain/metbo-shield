from functools import lru_cache
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

TRAINING_DATA = [
    ("Urgent action required. Verify your account immediately.",1),
    ("Your password expires today. Click this link now.",1),
    ("Unusual login detected. Confirm your identity.",1),
    ("Invoice attached. Enable macros to view it.",1),
    ("Purchase gift cards and send the codes.",1),
    ("The weekly team meeting is tomorrow at 10 AM.",0),
    ("Your support ticket has been resolved.",0),
    ("The project report is attached as a PDF.",0),
    ("Lunch has been moved to Friday.",0),
    ("No action is required for scheduled maintenance.",0),
]

@lru_cache(maxsize=1)
def get_model():
    texts, labels = zip(*TRAINING_DATA)
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2))),
        ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
    ])
    model.fit(texts, labels)
    return model

def predict(text: str) -> dict:
    probability = float(get_model().predict_proba([text or ""])[0][1])
    return {
        "probability": round(probability*100,1),
        "prediction": "Phishing" if probability >= .5 else "Legitimate",
        "confidence": round(max(probability,1-probability)*100,1),
    }
