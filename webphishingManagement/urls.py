from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='management_home'),
    path('client_list', views.client_list, name='management_client_list'),
    path('client/add_client/', views.add_client, name='management_add_client'),

    path('<str:client_pk>/addXLS', views.client_addXLS, name='management_client_addXLS'),
    path('<str:client_pk>/view', views.client_view, name='management_client_view'),
    path('<str:client_pk>/', views.client_view, name='management_client_view'),
    #path('campaign_list/', webviews.campaign_list, name='campaign_list'),
    #path('campaign_list/add_campaign/', webviews.add_campaign, name='add_campaign'),
    #path('campaign_detail/<int:campaign_pk>/', webviews.campaign_detail, name='campaign_detail'),
    
    #path('client/<int:client_pk>/exercise_list/', webviews.exercise_list, name='exercise_list'),
    #path('client/<int:client_pk>/add_exercise/', webviews.add_exercise, name='add_exercise'),
    #path('client/<int:client_pk>/<int:exercise_pk>/exercise_detail/', webviews.exercise_detail, name='exercise_detail'),
    
    #path('client/<int:client_pk>/<int:exercise_pk>/add_employees', webviews.add_employees, name='add_employees'),
]