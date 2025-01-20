from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("", lambda request: redirect("home/", permanent=True)),
    path("home/", views.index, name="index"),
]