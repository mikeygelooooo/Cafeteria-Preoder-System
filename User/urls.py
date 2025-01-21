from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.profile, name="user-profile"),
    path("profile/edit", views.edit_profile, name="user-edit-profile"),
    path("profile/history/", views.order_history, name="user-order-history"),
    path("profile/settings/", views.account_settings, name="user-account-settings"),
    path("signup/", views.signup, name="user-signup"),
    path("login/", views.login, name="user-login"),
    path("logout/", views.logout, name="user-logout"),
]