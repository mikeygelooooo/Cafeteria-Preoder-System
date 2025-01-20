from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .forms import LoginForm

# Create your views here.
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


def signup(request):
    return render(request, "user/signup.html")


def profile(request):
    return render(request, "user/profile.html")