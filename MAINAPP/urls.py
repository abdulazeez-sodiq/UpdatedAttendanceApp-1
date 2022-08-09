from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Welcome Page'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboardadmin', views.dashboardadmin, name='dashboardadmin'),
    path('terminal', views.terminal, name='terminal'),
    path('about', views.about, name='about'),
    path('about2', views.about2, name='about2'),
    path('enable', views.enable, name='enable'),
    path('disable', views.disable, name='disable'),
    path('register', views.register, name='register'),
    path('scan', views.scan, name='scan'),
    path('deletestaff', views.deletestaff, name='deletestaff'),
    path('showallstaff', views.showallstaff, name='showallstaff'),
    path('showallusers', views.showallusers, name='showallusers'),
    path('savescan', views.savescan, name='savescan'),
    path('delete', views.delete, name='delete'),
    path('deletealluser', views.deletealluser, name='deletealluser'),
    path('checkforID', views.checkforID, name='checkforID'),
    path('showpresentstaffs', views.showpresentstaffs, name='showpresentstaffs'),
    path('showabsentstaffs', views.showabsentstaffs, name='showabsentstaffs'),
    path('confirmdelete', views.confirmdelete, name='confirmdelete'),
    
]
