from django.shortcuts import render
from django.http import HttpResponse
from .models import Phone

def home(request):
	phones = Phone.objects.all()
	context = {'phones': phones}
	return render(request, 'dashboard/home.html', context)

def show(request):
	return HttpResponse('<h1> Welcome show! </h1>')
