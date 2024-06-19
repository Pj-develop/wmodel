# getweather/ml_models/__init__.py
import os
import joblib
from django.conf import settings

# Function to load the model and scaler
def load_model_and_scaler():
    model_path = os.path.join(settings.BASE_DIR, 'getweather', 'ml_models', 'best_gradient_boosting_model.pkl')
    scaler_path = os.path.join(settings.BASE_DIR, 'getweather', 'ml_models','scalers.pkl')
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler
