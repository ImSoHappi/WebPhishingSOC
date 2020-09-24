from django.urls import path
from webphishingAuth import views

urlpatterns = [
    path('', views.authentication, name='authentication'),
    path('logout/', views.logout_view, name='logout'),
]