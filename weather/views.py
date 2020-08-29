import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=2ffef26845ce26c60ce700d37494216c'
    #city = 'Solapur'   #call by city name but if we have to take it out from API dont use this

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)  # to add input data to db

        if form.is_valid():

            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod']==200 :               # to check the error message using error code
                    form.save()                #it will save entered data to database

                else:
                    err_msg = "This city not exits in the world"



            else:
                err_msg = " City already exists"

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = "City is created successfully!"
            message_class = 'is-success'

    print(err_msg)

    form = CityForm

    cities = City.objects.all()    # to show the all added cities detail we fetch city list from database

   # its dictionary created for each #city
    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()  #receive info in json object   # takes city data from url , we got city name,temprature,description and icon
        # here 'r' is a python dictionary

    #create dictionary that shows all that information

        city_weather = {
         'city': city.name,
         'temprature': r['main']['temp'],    #"main":{"temp":81.28,"feels_like":72.9,"temp_min":78.8,"temp_max":84,"pressure":1017,"humidity":9}
         'description':r['weather'][0]['description'], #"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}]
         'icon':r['weather'][0]['icon'],    #"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}]

        }

        weather_data.append(city_weather)   # to get data of all the added cities in database


    #print(weather_data)

    #now pass this all information in context

    context = {
        'weather_data': weather_data,
        'form':form,
        'message':message,
        'message_class': message_class
        }
    return render (request, 'weather/weather.html',context)

def DeleteCity(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
