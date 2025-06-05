import joblib
import os

def load_model(model_path='models/best_model.pkl'):
    model = joblib.load(model_path)
    return model