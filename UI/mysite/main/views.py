# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import UserInfo
# Create your views here.

def index(response, id):
	user = UserInfo.objects.get(id=id)
	return render(response, "main/dashboard.html", {"user":user})

def home(response):
	return render(response, "main/home.html", {})
