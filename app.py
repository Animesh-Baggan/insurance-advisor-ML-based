from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schema.premium_schema import InsuranceInput
from model.predict_model import InsuranceModel

# -------------------------------------------------
# CREATE FASTAPI APP
# -------------------------------------------------
app = FastAPI(
    title="Insurance Premium Prediction API",
    description="Predict insurance premium based on user profile",
    version="1.0.0"
)

# -------------------------------------------------
# CORS CONFIGURATION (REQUIRED FOR STREAMLIT)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow Streamlit Cloud
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# LOAD MODEL
# -------------------------------------------------
model = InsuranceModel()

# -------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------
@app.get("/")
def home():
    return {"message": "Insurance Premium Prediction API is running!"}

# -------------------------------------------------
# PREDICTION ENDPOINT
# -------------------------------------------------
@app.post("/predict")
def predict_premium(data: InsuranceInput):
    # Pydantic v2 compatible
    input_data = data.model_dump()

    # Model prediction
    prediction = model.predict(input_data)

    return {
        "input": input_data,
        "predicted_premium": prediction
    }
