import re
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import *
from django.db.models import Avg


# def index(request):
#     title = "all app info"
#     queryset = AppInfo.objects.all()
#     context = {
#         "title": title,
#         "queryset": queryset,
#     }
#     return render(request, 'polls/mainPage.html', context)


def index(request):
    rating_avg = AppInfo.objects.values('category').annotate(average = Avg('rating'))
    rating_count_avg = AppInfo.objects.values('category').annotate(average = Avg('rating_count'))
    install_avg = AppInfo.objects.values('category').annotate(average = Avg('install_number'))
    price_avg = AppInfo.objects.values('category').annotate(average = Avg('price'))
    all_info = AppInfo.objects.all()
    context = {
        "all" : all_info,
        "rating" : rating_avg,
        "rating_count" : rating_count_avg,
        "install" : install_avg,
        "price" : price_avg,
    }
    return render(request, 'polls/mainPage.html', context)