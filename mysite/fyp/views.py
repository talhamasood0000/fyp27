from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'fyp/index.html')

def team(request):
    return render(request,'fyp/team.html')

def login_page(request):
    return render(request,'fyp/login.html')

def signup_page(request):
    return render(request,'fyp/signup.html')