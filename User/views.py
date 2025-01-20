from django.shortcuts import render, HttpResponse

# Create your views here.
def login(request):
    return render(request, "user/login.html")


def signup(request):
    return render(request, "user/signup.html")


def profile(request):
    return render(request, "user/profile.html")