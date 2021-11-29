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
    return render(request, 'polls/mainPage.html')

def spreadsheet(request):
    return render(request, 'polls/spreadsheet.html')

def mongo_index(request):
    return render(request, 'polls/mongoPage.html')

def neo4j_index(request):
    return render(request, 'polls/neo4jPage.html')

def cassandra_index(request):
    return render(request, 'polls/cassandraPage.html')
