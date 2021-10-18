
from django.urls import path
from . import views
import polls.dash_app

urlpatterns = [
    path('', views.index, name="index"),
]