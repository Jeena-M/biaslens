# model/train_model.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

# Load dataset
df = pd.read_csv("../data.csv")  # text,label

# Split
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

# TF-IDF vectorization
vectorizer = TfidfVectorizer(max_features=500)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train binary classifier
clf = LogisticRegression()
clf.fit(X_train_vec, y_train)

# Test
print("Test accuracy:", clf.score(X_test_vec, y_test))

# Save model & vectorizer
joblib.dump(clf, "bias_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model and vectorizer saved!")
