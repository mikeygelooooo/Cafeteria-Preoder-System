from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .forms import LoginForm

# Create your views here.
@login_required(login_url="user-login")
def profile(request):
    return render(request, "user/profile.html")


@login_required(login_url="user-login")
def edit_profile(request):
    return render(request, "user/edit_profile.html")


@login_required(login_url="user-login")
def order_history(request):
    return render(request, "user/order_history.html")


@login_required(login_url="user-login")
def account_settings(request):
    return render(request, "user/account_settings.html")


def signup(request):
    if request.user.is_authenticated:
        return redirect("index")
    
    return render(request, "user/signup.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)

                if not remember_me:
                    request.session.set_expiry(0)

                next_page = request.GET.get('next', 'index')

                return redirect(next_page)
            
            else:
                messages.error(request, 'Invalid username or password.')

    else:
        form = LoginForm()

    context = {'form': form}

    return render(request, "user/login.html", context)


@login_required(login_url="user-login")
def logout(request):
    if request.method == "POST":
        auth_logout(request)

    return redirect("user-login")