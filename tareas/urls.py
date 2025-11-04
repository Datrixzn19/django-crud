from django.urls import path 
from . import views 

urlpatterns = [
    
    path('', views.home, name='home'),
    
    path('hello/', views.hello, name='hello'),

    path('signup/', views.signup, name='signup'),

    path('tareas/', views.tareas, name='tareas'),

    path('logout/', views.signout, name='logout'),

    path('signin/', views.signin, name='signin')


    ]