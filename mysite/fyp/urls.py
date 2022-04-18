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
    path('all_videos/',views.all_videos,name='all_videos'),
    path('redirect-page/<slug:slug>/',views.redirect_page,name='redirect_page'),
    path('generate_report/',views.generate_report,name='generate_report'),
    path('<slug:slug>/',views.demo,name='demo'),
    

]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
