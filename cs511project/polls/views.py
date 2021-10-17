from django.shortcuts import render
from .models import *



def index(request):
    title = "all app info"
    queryset = AppInfo.objects.all()
    context = {
        "title": title,
        "queryset": queryset,
    }
    return render(request, 'polls/mainPage.html', context)