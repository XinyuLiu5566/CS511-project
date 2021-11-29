
from django.urls import path
from . import views
import polls.dash_app
import polls.spreadsheet
import polls.dash_app_mongo
import polls.dash_app_neo4j
import polls.dash_app_cassandra

urlpatterns = [
    path('', views.index, name="index"),
    path('spreadsheet/', views.spreadsheet, name="spreadsheet"),
    path('mongo_backend/', views.mongo_index, name="mongo_index"),
    path('neo4j_backend/', views.neo4j_index, name="neo4j_index"),
    path('cassandra_backend/', views.cassandra_index, name="cassandra_index")
]