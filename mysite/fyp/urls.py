from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('team/',views.team,name='team'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_page,name='logout'),
    path('signup/',views.signup_page,name='signup'),
    path('video_upload/',views.video_upload,name='video_upload'),
    path('video_detail/',views.video_detail,name='video_detail'),
    path('<slug:slug>/',views.output,name='output'),


    # path('check/',views.check,name='check'),
    # path('demo/',views.demo,name='demo'),
    
    
]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
