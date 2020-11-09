from django.urls import path
from webphishingApi import views 
 
urlpatterns = [ 
    path('ex/reportSent', views.api_ex_reportSent, name='api_ex_reportSent'),
    #path('api/gethooks', views.api_gethooks, name='api_gethooks'),
    #path('api/posthooks', views.api_posthooks, name='api_posthooks'),
    #path('fishinghooks_list/', views.fishinghook_list , name='fishinghook_list'),
]