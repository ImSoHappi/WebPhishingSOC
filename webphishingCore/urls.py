from django.urls import path
from . import views as webviews

urlpatterns = [
    path('', webviews.user_redirector, name="redirector"),
]