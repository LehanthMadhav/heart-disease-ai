import joblib
import pandas as pd

from pathlib import Path
from fastapi import HTTPException
from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ML artifact paths
MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "best_model.joblib"
PREPROCESSOR_PATH = PROJECT_ROOT / "ml" / "models" / "preprocessor.joblib"

# Load trained model and preprocessor
try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)

    print("ML model loaded successfully.")
    print("Preprocessor loaded successfully.")

except Exception as error:
    model = None
    preprocessor = None
    print(f"ML loading error: {error}")

# Initialize FastAPI application
app = FastAPI(
    title="Heart Disease AI API",
    description="Clinical Data Analytics and Heart Disease Research Prototype",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ClinicalAssessment(BaseModel):
    age: int = Field(ge=1, le=120)
    sex: Literal[0, 1]
    cp: Literal[1, 2, 3, 4]
    trestbps: int = Field(ge=50, le=250)
    chol: int = Field(ge=0, le=700)
    fbs: Literal[0, 1]
    restecg: Literal[0, 1, 2]
    thalach: int = Field(ge=50, le=250)
    exang: Literal[0, 1]
    oldpeak: float = Field(ge=0, le=10)
    slope: Literal[1, 2, 3]
    ca: Literal[0, 1, 2, 3]
    thal: Literal[3, 6, 7]


class AssessmentResponse(BaseModel):
    success: bool
    message: str
    prediction: None = None
    model_connected: bool = False
    feature_count: int
    features_received: list[str]


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to the Heart Disease AI API"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/assessment")
def submit_assessment(data: ClinicalAssessment):

    if model is None or preprocessor is None:
        raise HTTPException(
            status_code=503,
            detail="ML model or preprocessor is not available."
        )

    try:
        # Convert the 13 submitted clinical values into a DataFrame
        input_data = pd.DataFrame([data.model_dump()])

        # Apply the same preprocessing used during model training
        processed_data = preprocessor.transform(input_data)

        # Generate model prediction
        prediction = int(model.predict(processed_data)[0])

        # Get class-1 probability, if supported
        probability = None

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(processed_data)[0]
            classes = list(model.classes_)

            if 1 in classes:
                probability = float(probabilities[classes.index(1)])

        # Interpret the binary class
        prediction_label = (
            "Disease Label"
            if prediction == 1
            else "No Disease Label"
        )

        return {
            "success": True,
            "message": "Clinical assessment processed successfully.",
            "prediction": prediction,
            "prediction_label": prediction_label,
            "class_1_probability": probability,
            "model_connected": True,
            "feature_count": len(input_data.columns),
            "model_name": "Logistic Regression",
            "disclaimer": (
                "Research prototype only. This output is not a "
                "medical diagnosis or a substitute for professional "
                "clinical evaluation."
            )
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )