import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

class DefaultPredictionModel:

    def __init__(self):
        self.model = LogisticRegression()

    def train(self, X, y):
        self.model.fit(X, y)
        joblib.dump(self.model, "default_model.pkl")

    def load(self):
        self.model = joblib.load("default_model.pkl")

    def predict_default_probability(self, features):
        prob = self.model.predict_proba([features])[0][1]
        return float(round(prob, 3))


[income, expenses, credit_score, outage_hours]


