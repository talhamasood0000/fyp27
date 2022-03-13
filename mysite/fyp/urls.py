from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('team/',views.team,name='team'),
    path('login/',views.login_page,name='login'),
    path('signup/',views.signup_page,name='signup'),
]