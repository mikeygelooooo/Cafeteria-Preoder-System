from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib import messages
from User.forms import (
    LoginForm,
)
from django.http import HttpResponseForbidden
from functools import wraps


# Create your views here.
def vendor_only(login_url=None):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url=login_url)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_staff:
                messages.error(
                    request, "Only vendors have permissions to access this page."
                )
                return redirect(login_url)
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


@vendor_only(login_url="vendor-login")
def dashboard(request):
    return render(request, "vendor/dashboard.html")


@vendor_only(login_url="vendor-login")
def order_management(request):
    return render(request, "vendor/order_management.html")


@vendor_only(login_url="vendor-login")
def menu_management(request):
    return render(request, "vendor/menu_management.html")


@vendor_only(login_url="vendor-login")
def sales_tracking(request):
    return render(request, "vendor/sales_tracking.html")


@vendor_only(login_url="vendor-login")
def stall_settings(request):
    return render(request, "vendor/stall_settings.html")


def login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("vendor-dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_staff:
                    auth_login(request, user)

                    if not remember_me:
                        request.session.set_expiry(0)

                    next_page = request.GET.get("next", "vendor-dashboard")

                    return redirect(next_page)

                else:
                    messages.error(request, "Only vendors can log in.")

            else:
                messages.error(request, "Invalid username or password.")

    else:
        form = LoginForm()

    context = {"form": form}

    return render(request, "vendor/login.html", context)


@vendor_only(login_url="vendor-login")
def logout(request):
    if request.method == "POST":
        auth_logout(request)

    return redirect("vendor-login")
