from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
import io


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from datetime import date,datetime

from ml_model.new_approach import detect_video
from ml_model.people_aproach import detect_people
from .forms import RegisterForm, LoginForm,VideoForm, NewsletterForm
from .models import Video,VideoOutput
import json

LOADED_MODEL = getattr(settings, "LOADED_MODEL", None) 
User=get_user_model()

today = date.today()

def index(request):
    if request.method== 'POST':
        form=NewsletterForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form=NewsletterForm()
    context={'form':form}   
    return render(request,'fyp/index.html',context)

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
    if request.method=='POST':
        form= VideoForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.user=User.objects.get(pk=request.user.id)
            print(obj.user)
            obj.save()
            return redirect('/all_videos/')
    else:
        form=VideoForm()           
    context={'form':form}
    return render(request, 'fyp/video-upload.html', context)

@login_required(login_url='/login/')
def all_videos(request):
    current_user = request.user
    videos=Video.objects.filter(user=current_user).order_by('-id')
    return render(request,'fyp/videos-page.html',{'videos':videos})

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

@login_required(login_url='/login/')
def people(request,slug):
    video=get_object_or_404(Video, slug=slug)
    all_items=VideoOutput.objects.filter(video=video)
    car_detected=[item.total_detected_card for item in all_items]
    time_detected=[item.detected_time for item in all_items]
    context={"people_detected":json.dumps(car_detected),"time_detected":json.dumps(time_detected)}
    return render(request,'fyp/demo-people.html',context)

@login_required(login_url='/login/')
def redirect_people(request, slug):
    video=get_object_or_404(Video, slug=slug)
    # video=Video.objects.get(slug=slug)
    if video.result:
        return render(request,'fyp/redirect-people.html',{'video':video})
    else:
        detect_people(video)
        video.result=True
        video.save()
        return render(request,'fyp/redirect-people.html',{'video':video}) 

# @login_required(login_url='/login/')
def generate_report(request):
# http://127.0.0.1:8000/generate_report
    buf=io.BytesIO()
    c=canvas.Canvas(buf,pagesize=letter)

#  added one inch margin from all sides
    c.translate(0.75*inch, 0.75*inch)

    c.setStrokeColorRGB(40/256, 167/256, 69/256)

    c.setFillColorRGB(0,0,0)

    c.setFont("Helvetica",40)
    x,y=1,650
    m_x=400
# image
    logo=ImageReader(r'C:\Users\Talha Masood\Documents\GitHub\fyp27\mysite\static\images\logo.JPG')
    c.drawImage(logo,x,y)


# drawString(x-cor,y-cord,"Text")
    c.drawRightString(500,670,"Report")

    c.setFont("Helvetica",15)

# First right Info Section
    c.drawString(x,y-50,"University of Engineering and Technology")
    c.drawString(x,y-70,"Lahore, Pakistan")
    c.drawString(x,y-90,"Phone: +92-42-36-955-955")
    c.drawString(x,y-110,"Email: contact@zavitite.com")
    c.drawString(x,y-130,"Website: zavirite.com")

# First Left Info Section
    c.drawRightString(m_x,y-50,"Date:")
    c.drawString(m_x+10,y-50,str(today.strftime("%B %d, %Y")))

    c.drawRightString(400,y-70,"Time:")
    c.drawString(m_x+10,y-70,str(datetime.now().strftime('%H:%M:%S')))

    c.drawRightString(m_x+40,y-90,"Report No.:")
    c.drawString(m_x+50,y-90,"2358")


    c.line(x,y-140,7*inch,y-140)

# Report  To Section
    new_x, new_y=4, 480
    c.setStrokeColorRGB(0/256, 34/256, 34/256)
    c.setFillColorRGB(0/256, 34/256, 34/256)
    c.rect(new_x-3, new_y, 150, 20, fill=1)

    c.setFillColorRGB(255/256,255/256,255/256)
    c.drawString(new_x,new_y+5,"Report To")

    c.setFillColorRGB(0,0,0)


    c.setFont("Helvetica-Bold",12)
    c.drawString(new_x+4,new_y-16,"Name:")
    c.setFont("Helvetica",12)
    c.drawString(new_x+45,new_y-16,str(request.user.username))

    c.setFont("Helvetica-Bold",12)
    c.drawString(new_x+4,new_y-32,"Phone:")
    c.setFont("Helvetica",12)
    c.drawString(new_x+50,new_y-32,str(request.user.phonenumber))

    c.setFont("Helvetica-Bold",12)
    c.drawString(new_x+4,new_y-48,"Email")
    c.setFont("Helvetica",12)
    c.drawString(new_x+45,new_y-48,str(request.user.email))
    c.setFont("Helvetica",15)

    c.setStrokeColorRGB(40/256, 167/256, 69/256)
    c.line(new_x-3,new_y-60,7*inch,new_y-60)

    # Table Section
    c.setStrokeColorRGB(0/256, 34/256, 34/256)
    c.setFillColorRGB(0/256, 34/256, 34/256)
    c.rect(new_x-3, new_y-90, 150, 20, fill=1)

    c.setFillColorRGB(255/256,255/256,255/256)
    c.drawString(new_x,new_y-85,"Activity")

    c.setFont("Helvetica",10)

# First Column
    c.setStrokeColorRGB(0/256, 34/256, 34/256)
    c.setFillColorRGB(0/256, 34/256, 34/256)
    c.rect(new_x-3, new_y-120, 80, 15, fill=1)

    c.setFillColorRGB(255/256,255/256,255/256)
    c.drawString(new_x+17,new_y-116,"Sr No.")

# 2nd Column
    c.setStrokeColorRGB(0/256, 1/256, 0/256)
    c.setFillColorRGB(0/256, 34/256, 34/256)
    c.rect(80, new_y-120, 180, 15, fill=1)

    c.setFillColorRGB(255/256,255/256,255/256)
    c.drawString(126,new_y-116,"Total Cars")

# 3rd Column
    c.setStrokeColorRGB(0/256, 1/256, 0/256)
    c.setFillColorRGB(0/256, 34/256, 34/256)
    c.rect(260, new_y-120, 245, 15, fill=1)

    c.setFillColorRGB(255/256,255/256,255/256)
    c.drawString(310,new_y-116,"Time of Detection")

# First Row
    row_x1,rowx2,rowx3,row_y=new_x+28,142,316,new_y-116
    c.setFillColorRGB(0/256,0/256,0/256)

    for i in range(0,3):
        row_y=row_y-15

        c.drawString(row_x1,row_y,str(i))
        c.drawString(rowx2,row_y,str(i*2))
        c.drawString(rowx3,row_y,"Time of Detection")

    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='report.pdf')
     