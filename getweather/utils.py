from .models import WeatherV1, OutputV1
from .ml_models import load_best_gb_model,load_Pipedata_model,load_model_and_scaler_RFC,load_model_and_scaler
import numpy as np
import pandas as pd


#Function to predict solidification
def predict_solidification(temp, humidity, precip, windspeed, solarradiation, solarenergy):
    # Load models and scalers
    best_gradient_boosting_model, scaler = load_model_and_scaler()
    features = np.array([temp, humidity, precip, windspeed, solarradiation, solarenergy]).reshape(1, -1)
    scaled_features = scaler.transform(features)
    prediction = best_gradient_boosting_model.predict(scaled_features)
    return prediction[0]



def predict_generate_and_demand(temp, humidity, precip, windspeed, solarradiation, solarenergy):
    # Load models 
    input_data = np.array([temp, humidity, precip, windspeed, solarradiation, solarenergy]).reshape(1, -1)
    best_gb_model= load_best_gb_model()
    prediction = best_gb_model.predict(input_data)
    return prediction[0][0], prediction[0][1]
    

#Algorithms
#when sum is less than 0 
def message_Predict(GBModel_Array,Sum_DeltaT):
    msg_dic={}
    SumgGD25=0
    SumgGD50=0
    SumgGD75=0
    SumgGD90=0
    
    DeltaGD_Label_Array=['25','50','75','90']
    for i in range(len(GBModel_Array)):
        SumgGD25+=GBModel_Array[i][0]-(GBModel_Array[i][1]*(1-0.25))
        print("SumgGD25",SumgGD25)
        SumgGD90+=GBModel_Array[i][0]-(GBModel_Array[i][1]*(1-0.9))
        SumgGD50+=GBModel_Array[i][0]-(GBModel_Array[i][1]*(1-0.50))
        SumgGD75+=GBModel_Array[i][0]-(GBModel_Array[i][1]*(1-0.75))

    
    DeltaGD_Array=[SumgGD25,SumgGD50,SumgGD75,SumgGD90]
    print("GBMODEL ARRAY")
    print(GBModel_Array)
    print("DeltaGD_Array")
    print(DeltaGD_Array)

    for i in range(len(DeltaGD_Array)):
        msg_dic[DeltaGD_Label_Array[i]]=f"If we turn OFF {DeltaGD_Label_Array[i]}% of turbines, we can prevent {DeltaGD_Array[i]-Sum_DeltaT} degree fall in temperature of Hot Tank, Which will help us to prevent solidification."

    return msg_dic


#anamoly
def detect_anomalies(input_data):
    input_df = pd.DataFrame([input_data])
    model=load_Pipedata_model();
    messages = model.detect_anomalies(input_df.iloc[0])
    return '\n'.join(messages)





#RUL
def predict_rul(input_data):
    input_data = pd.DataFrame(input_data)
    loaded_model,scaler2=load_model_and_scaler_RFC();
    input_data_scaled = scaler2.transform(input_data)
    predicted_rul = loaded_model.predict(input_data_scaled)[0]
    return predicted_rul
