from django.shortcuts import render

# Create your views here.

def index(request):


    return render(request,'stations/index.html')

def add_station(request):
    return render(request,'stations/add_station.html')