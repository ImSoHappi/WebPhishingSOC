from django.urls import path
from . import views as webviews

urlpatterns = [
    path('dashboard/', webviews.dashboard, name='client_dashboard'),
    path('campaigns/', webviews.campaigns, name='client_campaigns'),
    path('select_exercise/', webviews.select_exercise, name='client_select_exercise')
]