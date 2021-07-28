from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('<str:inverseForm>/inverse/', views.inverse, name='inverse'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/camera/', views.camera, name='camera'),
    path('camera/<int:feedID>/', views.findThreat, name='findThreat'),
    path('dashboard/camera/<str:function>/', views.cameraModify, name='cameraModify'),
    path('dashboard/threatLog/', views.threatLog, name='threatLog'),
    path('dashboard/recorded/', views.recorded, name='recorded'),
    path('recorded/<str:fileName>/', views.processRecorded, name='processFileName'),
    path('dashboard/settings/', views.settings, name='settings'),
    path('logout/', views.logout, name='logout')

]
