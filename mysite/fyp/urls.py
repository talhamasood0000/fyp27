from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('team/',views.team,name='team'),
    path('login/',views.login_page,name='login'),
    path('signup/',views.signup_page,name='signup'),
    path('video_upload/',views.video_upload,name='video_upload'),
]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)