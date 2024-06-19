from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from .models import WeatherV1, OutputV1
from .ml_models import load_model_and_scaler
import numpy as np
import requests

Data_Array=[];

#Function to predict solidification
def predict_solidification(temp, humidity, precip, windspeed, solarradiation, solarenergy):
    # Load models and scalers
    best_gradient_boosting_model, scaler = load_model_and_scaler()
    features = np.array([temp, humidity, precip, windspeed, solarradiation, solarenergy])
    scaled_features = scaler.transform(features)
    prediction = best_gradient_boosting_model.predict(scaled_features)
    return prediction[0]



#Views
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def show_weather_data(request):
    date='2024-06-19'
    pincode='144411'
    time="15:00:00"
    time_to_ind=int(time[0:2])
    print("time_to_ind",time_to_ind)
    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{zipcode}/{date}/{date}?unitGroup=metric&include=hours&key=PQ6T4N7XPRBXVXWYJN9YZ829K&contentType=json".format(zipcode=pincode,date=date)
    try:
        if(time_to_ind>17):
            return JsonResponse({"error": "Time is not available"}, status=500)
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            weather_data = response.json()
            timed_weather_data=weather_data.get('days', [])[0].get('hours', [])
            # timed_weather_data=weather_data.get('days', [])[0].get('hours', [])[time_to_ind]
            #dew_data = timed_weather_data
            for i in range(time_to_ind,((time_to_ind+7))):
                #print("temp ->",timed_weather_data[i].get('temp', "-999"))
                row=[timed_weather_data[i].get('temp', "-999"),timed_weather_data[i].get('humidity', "-999"),timed_weather_data[i].get('precip', "-999"),timed_weather_data[i].get('windspeed', "-999"),timed_weather_data[i].get('solarradiation', "-999"),timed_weather_data[i].get('solarenergy', "-999")]
                Data_Array.append(row)
                print(row)
            print("DATA ARRAY AT 0 INDEX \n")
            print(Data_Array[0])
            # Predict solidification
            solidification = predict_solidification(Data_Array[0][0], Data_Array[0][1], Data_Array[0][2], Data_Array[0][3], Data_Array[0][4], Data_Array[0][5])
            print("solidification",solidification)
            weather = WeatherV1(
            date_w=date,
            time_w=time,
            temperature=Data_Array[0][0],
            humidity=Data_Array[0][1],
            precipitation=Data_Array[0][2],
            windspeed=Data_Array[0][3],
            solar_rad=Data_Array[0][4],
            solar_engy=Data_Array[0][5],
            delta_t=solidification,
            place="Chandigarh",
            zipcode=str(pincode)
             )
            weather.save()
            
            return JsonResponse(weather_data)
        else:
            return JsonResponse({"error": "Failed to fetch weather data"}, status=500)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse, HttpResponseBadRequest
# import requests

# @csrf_exempt
# def show_weather(request):
#     if request.method == "POST":
#         # Extract parameters from POST request
#         location_id = request.POST.get('location_id')
#         unit_group = request.POST.get('unitGroup', 'us')  # Default to 'us' if not provided
        
#         # Validate input
#         if not location_id:
#             return HttpResponseBadRequest("Location ID is required.")
        
#         # Construct the URL dynamically
#         url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location_id}?unitGroup={unit_group}&key=PQ6T4N7XPRBXVXWYJN9YZ829K&contentType=json"
        
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 weather_data = response.json()
#                 return JsonResponse(weather_data)
#             else:
#                 return JsonResponse({"error": "Failed to fetch weather data"}, status=response.status_code)
#         except requests.RequestException as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     else:
#         return HttpResponseBadRequest("This endpoint only supports POST requests.")