from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('<str:inverseForm>/inverse/', views.inverse, name='inverse'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/camera', views.camera, name='camera'),
    path('dashboard/threatLog', views.threatLog, name='threatLog'),
    path('dashboard/settings', views.settings, name='settings'),
    #path('dashboard/camera/', views.camera, name='camera'),
    path('logout/', views.logout, name='logout')

]
