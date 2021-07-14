from django.urls import path
from . import views


urlpatterns = [
    path('', views.startup_graph, name="startup")
]