from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", RedirectView.as_view(pattern_name='vendor-dashboard', permanent=False)),
    path("dashboard/", views.dashboard, name="vendor-dashboard"),
    path("orders/", views.order_management, name="vendor-orders"),
    path("menu/", views.menu_management, name="vendor-menu"),
    path("sales/", views.sales_tracking, name="vendor-sales"),
    path("stall/", views.stall_settings, name="vendor-stall"),
    path("login/", views.login, name="vendor-login"),
    path("logout/", views.logout, name="vendor-logout"),
]
