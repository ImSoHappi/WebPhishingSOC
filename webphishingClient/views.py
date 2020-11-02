from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def select_exercise(request):
    context = {}
    return render(request, 'client/select_exercise.html', context = context)

@login_required
def dashboard(request):
    context = {}
    return render(request, 'client/dashboard.html', context = context)

@login_required
def campaigns(request):
    context = {}
    return render(request, 'client/campaigns.html', context = context)