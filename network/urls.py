from django.urls import path
from . import views


urlpatterns = [
    path('', views.startup_graph, name="startup"),
    path('graph/', views.base_graph, name="test"),
    path('test/', views.test)
]