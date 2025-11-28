from flask import Flask, request, jsonify
import joblib

from model.train_model import is_masculine

app = Flask(__name__) # app = instance of the Flask application

# Load pre-trained model and vectorizer
clf = joblib.load("./model/bias_model.pkl")
vectorizer = joblib.load("./model/vectorizer.pkl")

# Keyword → tailored suggestions
keyword_suggestions = {
    # Assertive → Collaborative
    "aggressive": ["assertive", "proactive", "confident"],
    "dominate": ["lead", "guide", "support"],
    "driven": ["motivated", "committed", "focused"],
    "competitive": ["goal-oriented", "ambitious"],
    "fearless": ["willing to take initiative", "confident"],
    "decisive": ["thoughtful", "deliberate", "clear-thinking"],

    # Action-heavy → Inclusive
    "crush": ["complete", "succeed", "achieve"],
    "rockstar": ["skilled", "collaborative", "high-performing"],
    "ninja": ["expert", "specialist"],
    "guru": ["expert", "experienced professional"],
    "bro": ["professional"],
    "hustle": ["work diligently", "maintain momentum"],
    "push": ["advance", "move forward", "progress"],
    "take charge": ["take initiative", "lead collaboratively"],

    # Power words → Team-oriented
    "dominating": ["leading", "influencing"],
    "command": ["oversee", "manage"],
    "superior": ["high quality", "excellent"],
    "challenge": ["opportunity", "project"],
    "driving": ["leading", "guiding"],

    # Stoic → Professional
    "tough": ["resilient", "capable"],
    "strong": ["capable", "effective"],
    "fast-paced": ["dynamic", "active"],
    "ambitious": ["motivated", "goal-oriented"],
    "independent": ["autonomous", "self-directed"],

    # Workaholic → Sustainable
    "work under pressure": ["manage deadlines", "handle time-sensitive tasks"],
    "tight deadlines": ["clear timelines"],
    "long hours": ["flexible schedule expectations"],

    # Leadership-coded (male-typed) → Balanced
    "assertive": ["confident", "clear-communicating"],
    "confident": ["capable", "self-assured"],
    "outspoken": ["communicative", "articulate"],
    "ambitious": ["motivated", "goal-oriented"],
    "bros": ["people", "humans", "employees"],
}

def find_suggestions(text):
    text_low = text.lower()
    found = {}

    for keyword, suggestions in keyword_suggestions.items():
        if keyword in text_low:
            found[keyword] = suggestions

    return found


@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.get_json().get("text", "")
    
    # Original model prediction
    text_vec = vectorizer.transform([text])
    label = clf.predict(text_vec)[0]
    confidence = clf.predict_proba(text_vec).max()
    
    # Embedding-based override
    masculine_detected, word_found, seed_word = is_masculine(text)
    if masculine_detected:
        label = "masculine"
        confidence = 0.99
    
    # Tailored suggestions
    found_suggestions = find_suggestions(text)

    return jsonify({
        "text": text,
        "ai_label": label,
        "confidence": round(confidence, 3),
        "tailored_suggestions": found_suggestions
    })


if __name__ == "__main__":
    app.run(port=5000)