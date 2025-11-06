from flask import Flask, request, jsonify
import joblib

from model.train_model import is_masculine

app = Flask(__name__) # app = instance of the Flask application

# Load pre-trained model and vectorizer
clf = joblib.load("./model/bias_model.pkl")
vectorizer = joblib.load("./model/vectorizer.pkl")

# Keyword → tailored suggestions
keyword_suggestions = {
    "rockstar": ["motivated", "collaborative", "innovative"],
    "dominate": ["lead", "guide", "contribute"],
    "crush": ["achieve", "complete", "succeed"],
    "aggressive": ["assertive", "proactive", "confident"]
}

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
    found_suggestions = {seed_word: keyword_suggestions[seed_word] for seed_word in keyword_suggestions if seed_word in text.lower()}

    return jsonify({
        "text": text,
        "ai_label": label,
        "confidence": round(confidence, 3),
        "tailored_suggestions": found_suggestions
    })


if __name__ == "__main__":
    app.run(port=5000)