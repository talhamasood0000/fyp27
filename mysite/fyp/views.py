from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings

from ml_model.new_approach import detect_video
from .forms import RegisterForm, LoginForm,VideoForm
from .models import Video,VideoOutput
import json

LOADED_MODEL = getattr(settings, "LOADED_MODEL", None) 

User=get_user_model()


def index(request):
    return render(request,'fyp/index.html')

def team(request):
    return render(request,'fyp/team.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')

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

def logout_page(request):
    logout(request)
    return redirect('/login/')

def signup_page(request):
    if request.user.is_authenticated:
        return redirect('/')

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
        print(obj.user)
        obj.save()

        return redirect('/all_videos/')
    context={'form':form}
    return render(request, 'fyp/video-upload.html', context)

@login_required(login_url='/login/')
def all_videos(request):
    current_user = request.user
    videos=Video.objects.filter(user=current_user).order_by('-id')
    return render(request,'fyp/all-videos.html',{'videos':videos})

@login_required(login_url='/login/')
def redirect_page(request, slug):
    video=get_object_or_404(Video, slug=slug)
    # video=Video.objects.get(slug=slug)
    if video.result:
        return render(request,'fyp/redirect.html',{'video':video})
    else:
        detect_video(video, LOADED_MODEL)
        video.result=True
        video.save()
        return render(request,'fyp/redirect.html',{'video':video}) 

@login_required(login_url='/login/')
def demo(request,slug):
    video=get_object_or_404(Video, slug=slug)
    all_items=VideoOutput.objects.filter(video=video)
    car_detected=[item.total_detected_card for item in all_items]
    time_detected=[item.detected_time for item in all_items]
    context={"car_detected":json.dumps(car_detected),"time_detected":json.dumps(time_detected)}
    return render(request,'fyp/demo.html',context)


    