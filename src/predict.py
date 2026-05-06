import pickle
import pandas as pd

def load_model(model_path: str = "models/best_model.pkl"):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

def predict(model, features: dict) -> dict:
    df = pd.DataFrame([features])
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return {
        "approved": bool(prediction == 1),
        "probability": round(float(probability), 4),
        "label": "Aprovado ✅" if prediction == 1 else "Recusado ❌"
    }