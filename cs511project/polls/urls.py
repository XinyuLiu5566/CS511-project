
from django.urls import path
from . import views
import polls.dash_app
import polls.dash_app_mongo

urlpatterns = [
    path('', views.index, name="index"),
    path('mongo_backend/', views.mongo_index, name="mongo_index")
]