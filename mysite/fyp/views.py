from unittest import result
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout

from ml_model.new_approach import detect_video
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings

LOADED_MODEL = getattr(settings, "LOADED_MODEL", None)

User=get_user_model()

from .models import Video
from .forms import VideoForm

def index(request):
    return render(request,'fyp/index.html')

def team(request):
    return render(request,'fyp/team.html')

def login_page(request):
    if request.method=='POST':
        form=LoginForm(request.POST or None)
        context={'form':form}
        if form.is_valid():
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                login(request,user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('/')
            else:
                return HttpResponse('Invalid Login')
    else:
        form=LoginForm()
        context={'form':form}
    return render(request,'fyp/login.html',context)

def signup_page(request):
    form=RegisterForm(request.POST or None)
    context={'form':form}
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request,'fyp/signup.html',context)

@login_required(login_url='/login/')
def video_upload(request):
    form= VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj=form.save(commit=False)
        obj.user=User.objects.get(pk=request.user.id)
        obj.save()
        return redirect('/video_detail/')
    context={'form':form}
    return render(request, 'fyp/admin-panel.html', context)

@login_required(login_url='/login/')
def video_detail(request):
    current_user = request.user
    videos=Video.objects.filter(user=current_user).order_by('-id')
    return render(request,'fyp/video-page.html',{'videos':videos})

@login_required(login_url='/login/')
def output(request, slug):
    video=Video.objects.get(slug=slug)
    if video.result:
        
        return render(request,'fyp/demo.html',{'video':video})
    else:
        detect_video(video, LOADED_MODEL)
        video.result=True
        video.save()
        return render(request,'fyp/demo.html',{'video':video}) 




@login_required(login_url='/login/')
def demo(request):
    current_user = request.user
    videos=Video.objects.filter(user=current_user).order_by('-id')

    return render(request,'fyp/check.html')


# def check(request):
#     detect_video('media/upload_test_videos/tmn2.mp4', LOADED_MODEL)
#     return render(request,'fyp/check.html')

    