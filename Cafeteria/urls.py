from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", RedirectView.as_view(pattern_name='index', permanent=True)),
    path("home/", views.index, name="index"),
]
