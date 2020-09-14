from django.urls import path
from . import views as webviews


urlpatterns = [
    path('campaign_list/', webviews.campaign_list, name='campaign_list'),
    path('campaign_list/add_campaign/', webviews.add_campaign, name='add_campaign'),
    path('campaign_detail/<int:campaign_pk>/', webviews.campaign_detail, name='campaign_detail'),
    path('', webviews.client_list, name='client_list'),
    path('client/<int:client_pk>/exercise_list/', webviews.exercise_list, name='exercise_list'),
    path('client/<int:client_pk>/add_exercise/', webviews.add_exercise, name='add_exercise'),
    path('client/<int:client_pk>/<int:exercise_pk>/exercise_detail/', webviews.exercise_detail, name='exercise_detail'),
    path('client/add_client/', webviews.add_client, name='add_client'),
    path('client/<int:client_pk>/<int:exercise_pk>/add_employees', webviews.add_employees, name='add_employees'),
]