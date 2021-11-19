
from django.urls import path
from . import views
import polls.dash_app
import polls.spreadsheet
import polls.dash_app_mongo
import polls.dash_app_neo4j

urlpatterns = [
    path('', views.index, name="index"),
    path('spreadsheet/', views.spreadsheet, name="spreadsheet"),
    path('mongo_backend/', views.mongo_index, name="mongo_index"),
    path('neo4j_backend/', views.neo4j_index, name="neo4j_index")
]