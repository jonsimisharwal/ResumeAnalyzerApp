import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import os

def train_and_save_model():
    data = pd.DataFrame({
        "skills": [
            "python machine learning sql",
            "html css javascript react",
            "java spring sql",
            "python flask django",
            "c++ sql python"
        ],
        "role": [
            "Data Scientist",
            "Frontend Developer",
            "Backend Developer",
            "Fullstack Developer",
            "Software Engineer"
        ]
    })

    model = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB())
    ])

    model.fit(data["skills"], data["role"])
    joblib.dump(model, "model.pkl")

if not os.path.exists("model.pkl"):
    train_and_save_model()

def predict_job_role(skills_list):
    model = joblib.load("model.pkl")
    input_text = " ".join(skills_list)
    return model.predict([input_text])[0]
