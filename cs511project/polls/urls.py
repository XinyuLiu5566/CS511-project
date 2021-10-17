
from django.urls import path, include
from . import views
import polls.dash_app

urlpatterns = [
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('', views.index, name="index"),
]