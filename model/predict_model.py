import joblib
import numpy as np

class InsuranceModel:
    def __init__(self):
        # For now use a dummy model coefficient
        # Later you can load a real model using joblib.load("model/model.pkl")
        self.coeff = 120.5

    def predict(self, data):
        # Fake formula for prediction
        # You can replace this with: model.predict(...)
        prediction = (data["age"] * 10) + (data["bmi"] * 3) + (data["children"] * 2)
        if data["smoker"].lower() == "yes":
            prediction += 15000
        return round(prediction, 2)
