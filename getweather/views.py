from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import WeatherV1, OutputV1
import requests
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from .utils import predict_generate_and_demand,message_Predict,predict_rul,detect_anomalies,predict_solidification

#Temp Storage
Data_Array=[]
DeltaT_Array=[]
GBModel_Array=[]
Sum_DeltaT=0.0
time_w=0
date_w=0



class RULView(generic.View):
    model = WeatherV1
    template_name = "getweather/rul.html"
    def get(self,requests):
        return render(requests,self.template_name);

    def post(self, request):
        # Retrieve data from the form
        input_data = {
        'temperature': [float(request.POST.get('temperature'))],
        'pressure': [float(request.POST.get('pressure'))],
        'flow_rate': [float(request.POST.get('flow_rate'))],
        'vibration': [float(request.POST.get('vibration'))],
        'motor_current': [float(request.POST.get('motor_current'))],
        'operating_hours': [float(request.POST.get('operating_hours'))]
    }
        
        result=predict_rul(input_data)
        result=str(result).strip()
        result=result if len(result)>0 else "NO RUL DETECTED"
        # print(result)
        # Pass the result back to the template
        return render(request, self.template_name, {'result': result})




class AnomalyView(generic.View):
    template_name = "getweather/anomaly.html"

    def get(self,requests):
        return render(requests,self.template_name);

    def post(self, request):
        # Retrieve data from the form
        input_data = {
        'CL_out_temp': float(request.POST.get('CL_out_temp')),
        'Fluid_temp_at_3V_in': float(request.POST.get('Fluid_temp_at_3V_in')),
        'HT_out_fluid_temp': float(request.POST.get('HT_out_fluid_temp')),
        'HE_fluid_in_temp': float(request.POST.get('HE_fluid_in_temp')),
        'HE_fluid_out_temp': float(request.POST.get('HE_fluid_out_temp')),
        'CT_in_Fluid_temp':float(request.POST.get('CT_in_Fluid_temp')),
        'CT_out_fluid_temp': float(request.POST.get('CT_out_fluid_temp')),
        'CL_in_fluid_temp': float(request.POST.get('CL_in_fluid_temp'))
    }
        # print(input_data['CL_in_fluid_temp'])
        result=detect_anomalies(input_data).strip()
        result=result if len(result)>0 else "NO ANOMALY DETECTED"

        # print(result)
        
        
        # Pass the result back to the template
        return render(request, self.template_name, {'result': result})


#Views

def solidification(request):
    result_dict = request.session.pop('result_dict', {})
    return render(request, "getweather/solidification.html",{'result_dict': result_dict})



#API FOR MESSAGE
def solidificationAPI(request):
    global Data_Array, DeltaT_Array, Sum_DeltaT, time_w, date_w, GBModel_Array
    Data_Array = []
    GBModel_Array=[]
    DeltaT_Array = []
    Sum_DeltaT = 0.0
    time_w = 0
    date_w = 0
   
    if request.method == "POST":
        time_w = request.POST.get('time_w')
        if time_w:
            time_o = time_w
            time_w = time_o[11:13]
            date_w = time_o[0:10]
            show_weather_data(date_w,time_w,144411)
            msg=""
            # for Message Framework
            if(Sum_DeltaT>0):
                msg=f"Everything Going Good ! , In Next 3 Hours There will an increase of {Sum_DeltaT} degree in Hot Tank Temperature.Hence, Solidification is NOT Possible"
            else:
                 # Store the dictionary in the session
                request.session['result_dict'] = message_Predict(GBModel_Array,Sum_DeltaT)
                msg=f"Solidification is Possible ! In Next 3 Hours from Time: {time_w}:00 and Date: {date_w} "

            if(Sum_DeltaT>0):
                messages.success(request, msg)
            else:
                messages.error(request, msg)
            # Redirect to a view where you want to display the messages
            return redirect(reverse("getweather:solidification"))
        else:
            messages.error(request, "Missing 'time_w' parameter.")
            # Redirect back to the form or some other view
            return redirect(reverse("getweather:solidification"))
    else:
        messages.error(request, "Only POST method is allowed.")
        # Redirect back to the form or some other view
        return redirect(reverse("getweather:solidification"))



# Leave the rest of the views (detail, results, vote) unchanged & CALC
def show_weather_data(date_w,time_w,pincode_w):
    global Sum_DeltaT
    global Data_Array
    global DeltaT_Array
    global GBModel_Array
    date=date_w
    pincode=pincode_w
    time_to_ind=int(time_w)
    # print("time_to_ind",time_to_ind)
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
            for i in range(time_to_ind,((time_to_ind+3))):
                #print("temp ->",timed_weather_data[i].get('temp', "-999"))
                row=[timed_weather_data[i].get('temp', "-999"),timed_weather_data[i].get('humidity', "-999"),timed_weather_data[i].get('precip', "-999"),timed_weather_data[i].get('windspeed', "-999"),timed_weather_data[i].get('solarradiation', "-999")/980,timed_weather_data[i].get('solarenergy', "-999")]
                Data_Array.append(row)
                
            # print("DATA ARRAY AT ALL INDEX")
            # print(Data_Array)
            
            # Predict solidification
            for i in range(len(Data_Array)):
                del_T=predict_solidification(Data_Array[i][0], Data_Array[i][1], Data_Array[i][2], Data_Array[i][3], Data_Array[i][4], Data_Array[i][5])
                del_GD=predict_generate_and_demand(Data_Array[i][0], Data_Array[i][1], Data_Array[i][2], Data_Array[i][3], Data_Array[i][4], Data_Array[i][5])
                DeltaT_Array.append(del_T)
                GBModel_Array.append(del_GD)
                weather = WeatherV1(
                date_w=date,
                time_w=f"{time_to_ind+i:02d}:00:00",
                temperature=Data_Array[i][0],
                humidity=Data_Array[i][1],
                precipitation=Data_Array[i][2],
                windspeed=Data_Array[i][3],
                solar_rad=Data_Array[i][4],
                solar_engy=Data_Array[i][5],
                delta_t=del_T,
                place="Chandigarh",
                zipcode=str(pincode)
                )
                #removing backend storage
                weather.save()
                Sum_DeltaT+=DeltaT_Array[i]
                
            output=OutputV1(remark_text=f"Solidification depends on sum of delta T for 3 hours is {Sum_DeltaT} with input date: {date_w} time{time_w} for pincode {pincode} and input array is {Data_Array} and output array is {DeltaT_Array} ", avg_delta_t=Sum_DeltaT)
            #removing backend storage
            output.save()
            
            # print("GBMODEL ARRAY")
            # print(GBModel_Array)
            #func(GBModel_Array,Sum_DeltaT)
            #print(GBModel_Array[0][0])
            # print("DELTA T ARRAY")
            # print(DeltaT_Array)
            # print("sum is " ,Sum_DeltaT)
            # print("NEWWW GB MODEL ANSWER")
            # print(predict_generate_and_demand(Data_Array[0][0], Data_Array[0][1], Data_Array[0][2], Data_Array[0][3], Data_Array[0][4], Data_Array[0][5]))
            
            
            return JsonResponse({"formatted data":timed_weather_data})
        else:
            return JsonResponse({"error": "Failed to fetch weather data"}, status=500)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

