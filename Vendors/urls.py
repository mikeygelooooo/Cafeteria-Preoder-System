from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("", lambda request: redirect("dashboard/", permanent=True)),
    path("dashboard/", views.dashboard, name="vendor-dashboard"),
]
