# getweather/ml_models/__init__.py
import os
import joblib
from django.conf import settings
import pandas as pd

# Function to load the model and scaler
def load_model_and_scaler():
    model_path = os.path.join(settings.BASE_DIR, 'getweather', 'ml_models', 'best_gradient_boosting_model.pkl')
    scaler_path = os.path.join(settings.BASE_DIR, 'getweather', 'ml_models','scalers.pkl')
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler


def load_best_gb_model():
    model_path = os.path.join(settings.BASE_DIR, 'getweather', 'ml_models', 'best_gb_model.pkl')
    model = joblib.load(model_path)
    return model

def load_model_and_scaler_RFC():
    model_path = os.path.join(settings.BASE_DIR, 'getweather', 'ml_models', 'random_forest_regression_modell.pkl')
    scaler_path = os.path.join(settings.BASE_DIR, 'getweather', 'ml_models','scalerp.pkl')
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler


class AnomalyDetector:
    def __init__(self, data_path):
        self.data = pd.read_excel(data_path)
        self.calculate_mean_differences()

    def calculate_mean_differences(self):
        self.mean_diff_1 = abs(self.data['CL_out_temp'] - self.data['Fluid_temp_at_3V_in']).mean()
        self.mean_diff_3 = abs(self.data['HT_out_fluid_temp'] - self.data['HE_fluid_in_temp']).mean()
        self.mean_diff_4 = abs(self.data['HE_fluid_out_temp'] - self.data['CT_in_Fluid_temp']).mean()
        self.mean_diff_6 = abs(self.data['CT_out_fluid_temp'] - self.data['CL_in_fluid_temp']).mean()

    def detect_anomalies(self, input_data):
        messages = []
        if abs(input_data['CL_out_temp'] - input_data['Fluid_temp_at_3V_in']) > self.mean_diff_1:
            messages.append("Attention!!! Anomaly in Pipe 1")
        if abs(input_data['HT_out_fluid_temp'] - input_data['HE_fluid_in_temp']) > self.mean_diff_3:
            messages.append("Attention!!! Anomaly in P3")
        if abs(input_data['HE_fluid_out_temp'] - input_data['CT_in_Fluid_temp']) > self.mean_diff_4:
            messages.append("Attention!!! Anomaly in P4")
        if abs(input_data['CT_out_fluid_temp'] - input_data['CL_in_fluid_temp']) > self.mean_diff_6:
            messages.append("Attention!!! Anomaly in P6")
        return messages


def load_Pipedata_model():
    model_path = os.path.join(settings.BASE_DIR, 'getweather', 'ml_models', 'PipesData.xlsx')
    model = AnomalyDetector(model_path)
    return model