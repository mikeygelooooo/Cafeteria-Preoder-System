from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", RedirectView.as_view(pattern_name='vendor-dashboard', permanent=False)),
    path("dashboard/", views.dashboard, name="vendor-dashboard"),
    path("login/", views.login, name="vendor-login"),
    path("logout/", views.logout, name="vendor-logout"),
]
