from django.shortcuts import render, HttpResponse

# Create your views here.
def profile(request):
    return HttpResponse("User Profile")