from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import clientModel, exerciseModel, csvModel, employeesModel, campaignModel
import csv, re
from .forms import clientForm, exerciseForm, csvForm, campaignForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def client_list(request):

    context = {}
    context['client_list'] = clientModel.objects.all()

    return render(request, 'client_list.html', context=context)

def add_client(request):

    if request.method == "POST":
        form = clientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = clientForm()

    return render(request, 'add_client.html', {'form': form})


def add_exercise(request, client_pk):
    
    if request.method == 'POST':
        form = exerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.client = clientModel.objects.get(pk=client_pk)
            exercise.save()
            return redirect('exercise_list', client_pk=client_pk)

    else:
        form = exerciseForm()
    
    return render(request, 'add_exercise.html', {'form': form})

def exercise_list(request, client_pk):

    context = {}
    context['client'] = clientModel.objects.get(pk=client_pk)
    context['exercise_list'] = exerciseModel.objects.filter(client=client_pk)

    return render(request, 'exercise_list.html', context=context)

def exercise_detail(request, client_pk, exercise_pk):

    context = {}
    context['employees_list'] = employeesModel.objects.filter(exercise=exercise_pk)
    context['exercise'] = exerciseModel.objects.get(pk=exercise_pk)
    context['client'] = clientModel.objects.get(pk=client_pk)

    return render(request, 'exercise_detail.html', context=context)

def add_employees(request, client_pk, exercise_pk):

    form = csvForm(request.POST, request.FILES)
    if form.is_valid():

        csvfile = request.FILES['csvfile'] 
        decoded_file = csvfile.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        next(reader, None)

        for i, row in enumerate(reader):
        
            row = "".join(row)
            row = row.replace(";", " / ")  

            email = (re.findall(r'[\w\.-]+@[\w\.-]+', row))
            email = "".join(email)

            employeesModel.objects.create(
                exercise = exerciseModel.objects.get(pk=exercise_pk),
                company = clientModel.objects.get(pk=client_pk),
                email = email,
                data = row,
            )
        return redirect('exercise_detail', client_pk=client_pk, exercise_pk=exercise_pk)  

    else:
        form = csvForm()       
    
    return render(request, 'upload.html', {'form':form} )


def campaign_list(request):

    context = {}
    context['campaign_list'] = campaignModel.objects.all()

    return render(request, 'campaign_list.html', context=context)
       
def add_campaign(request):

    if request.method == 'POST':
        form = campaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('campaign_list')
    else:
        form = campaignForm()

    return render(request, 'add_campaign.html', {'form':form})

def campaign_detail(request, campaign_pk):

    context = {}
    context['campaign'] = campaignModel.objects.get(pk=campaign_pk)

    return render(request, 'campaign_detail.html', context=context)