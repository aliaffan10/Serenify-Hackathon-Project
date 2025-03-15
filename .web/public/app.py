from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import os

app = Flask(__name__)

# Load emotion dataset
emotion_data = pd.read_csv("text_emotion.csv")
emotion_data.dropna(subset=['content', 'sentiment'], inplace=True)

# Encode emotion labels into numeric values
label_encoder = LabelEncoder()
emotion_data['sentiment'] = label_encoder.fit_transform(emotion_data['sentiment'])

# Train emotion detection model
X_emotion = emotion_data['content']
y_emotion = emotion_data['sentiment']

X_train_em, X_test_em, y_train_em, y_test_em = train_test_split(X_emotion, y_emotion, test_size=0.2, random_state=42)

emotion_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))
X_train_em_vec = emotion_vectorizer.fit_transform(X_train_em)
X_test_em_vec = emotion_vectorizer.transform(X_test_em)

emotion_model = XGBClassifier(learning_rate=0.1, max_depth=4, n_estimators=200, use_label_encoder=False,
                              eval_metric='logloss', n_jobs=-1)
emotion_model.fit(X_train_em_vec, y_train_em)

y_pred_em = emotion_model.predict(X_test_em_vec)
acc_em = accuracy_score(y_test_em, y_pred_em)
print(f"Emotion Detection Model Accuracy: {acc_em:.3f}")

# Load suicide detection dataset
sd_data = pd.read_csv("Suicide_Detection.csv")
sd_data.dropna(subset=['text', 'class'], inplace=True)
sd_data['label'] = sd_data['class'].apply(lambda x: 1 if str(x).strip().lower() == "suicide" else 0)

X_sd = sd_data['text']
y_sd = sd_data['label']
X_train_sd, X_test_sd, y_train_sd, y_test_sd = train_test_split(X_sd, y_sd, test_size=0.2, random_state=42)

sd_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))
X_train_sd_vec = sd_vectorizer.fit_transform(X_train_sd)
X_test_sd_vec = sd_vectorizer.transform(X_test_sd)

suicide_model = XGBClassifier(learning_rate=0.1, max_depth=4, n_estimators=200, use_label_encoder=False,
                              eval_metric='logloss', n_jobs=-1)
suicide_model.fit(X_train_sd_vec, y_train_sd)

y_pred_sd = suicide_model.predict(X_test_sd_vec)
acc_sd = accuracy_score(y_test_sd, y_pred_sd)
print(f"Suicide Detection Model Accuracy: {acc_sd:.3f}")

# Load master.csv safely
master_data = pd.read_csv("master.csv")
for col in master_data.columns:
    master_data[col] = pd.to_numeric(master_data[col], errors='coerce')
master_data.dropna(axis=1, how='all', inplace=True)

# Generate heatmap
def generate_heatmap():
    plt.figure(figsize=(10, 6))
    sns.heatmap(master_data.corr(), annot=True, cmap='Oranges', fmt=".2f", linewidths=0.5)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()

    heatmap_path = os.path.join("static", "heatmap.png")
    plt.savefig(heatmap_path)
    return heatmap_path


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Please enter a message!"}), 400

    # Check for suicide-related keywords directly in the message
    suicide_keywords = ['kill myself', 'suicide', 'end my life', 'take my life', 'want to die', 'hurt myself']
    if any(keyword in user_message.lower() for keyword in suicide_keywords):
        response = {
            "emotion": "suicide_risk_detected",
            "suicide_risk": True
        }
        return jsonify(response)

    # Emotion Detection
    user_vec_em = emotion_vectorizer.transform([user_message])
    predicted_emotion = emotion_model.predict(user_vec_em)[0]
    predicted_emotion_label = label_encoder.inverse_transform([predicted_emotion])[0]

    response = {
        "emotion": predicted_emotion_label,
        "suicide_risk": False
    }

    # Suicide Detection
    user_vec_sd = sd_vectorizer.transform([user_message])
    prediction_sd = suicide_model.predict(user_vec_sd)[0]
    if prediction_sd == 1:
        response["suicide_risk"] = True

    return jsonify(response)


@app.route('/heatmap')
def heatmap():
    heatmap_path = generate_heatmap()
    return jsonify({"heatmap_url": heatmap_path})


if __name__ == '__main__':
    app.run(debug=True)