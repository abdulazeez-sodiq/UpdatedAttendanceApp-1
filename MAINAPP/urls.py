from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Welcome Page'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('terminal', views.terminal, name='terminal'),
    path('about', views.about, name='about'),
    path('about2', views.about2, name='about2'),
    path('connect', views.connect, name='connect'),
    path('disconnect', views.disconnect, name='disconnect'),
    path('enable', views.enable, name='enable'),
    path('disable', views.disable, name='disable'),
]
