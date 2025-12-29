from fastapi import FastAPI
from schema.premium_schema import InsuranceInput
from model.predict_model import InsuranceModel

app = FastAPI()

# Load the dummy model
model = InsuranceModel()

@app.get("/")
def home():
    return {"message": "Insurance Premium Prediction API is running!"}

@app.post("/predict")
def predict_premium(data: InsuranceInput):
    # Convert Pydantic model to dictionary
    input_data = data.dict()

    # Make prediction using dummy model
    prediction = model.predict(input_data)

    return {
        "input": input_data,
        "predicted_premium": prediction
    }
