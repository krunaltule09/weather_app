from django.shortcuts import render
import requests 
from django.http import HttpResponse
from .models import City
from .forms import CityForm

def HomePageView(request):
	weather_info=[]
	cities=City.objects.all().order_by('-id')
	url='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=6b05727b5364c2cf4f8116db57893c26'
	if request.method=='POST':
		form=CityForm(request.POST)
		form.save()
	form=CityForm()
	for city in cities:
		r=requests.get(url.format(city)).json()

		weather_data={
		'city':city.name,
		'temperature':r['main']['temp'],
		'humidity':r['main']['humidity'],
		'wind':r['wind']['speed'],
		'description':r['weather'][0]['description'],
		'icon':r['weather'][0]['icon']
		}
		weather_info.append(weather_data)

	context={
	'weather_data':weather_info,
	'form':form
	}
	return render(request,'index.html',context)