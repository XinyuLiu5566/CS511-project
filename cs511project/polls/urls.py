
from django.urls import path
from . import views
import polls.dash_app
import polls.spreadsheet
import polls.customizeSQL
import polls.bar_chart
import polls.scatter_plot
import polls.dash_app_mongo
import polls.dash_app_neo4j
import polls.dash_app_cassandra

urlpatterns = [
    path('', views.index, name="index"),
    path('barchart/', views.barchart, name="barchart"),
    path('scatterplot/', views.scatterplot, name="scatterplot"),
    path('spreadsheet/', views.spreadsheet, name="spreadsheet"),
    path('customizeSQL/', views.customizeSQL, name="customizeSQL"),
    path('mongo_backend/', views.mongo_index, name="mongo_index"),
    path('neo4j_backend/', views.neo4j_index, name="neo4j_index"),
    path('cassandra_backend/', views.cassandra_index, name="cassandra_index")
]