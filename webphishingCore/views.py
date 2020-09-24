from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import clientModel, exerciseModel, csvModel, employeesModel, campaignModel
import csv, re
from .forms import clientForm, exerciseForm, csvForm, campaignForm
from django.contrib import messages
from django.core.mail.message import EmailMultiAlternatives
from django.core.mail import get_connection
from django.contrib.auth.decorators import login_required

# Create your views here.


################################################################
######################### CLIENT VIEWS #########################
################################################################

@login_required
def client_list(request):

    context = {}
    context['client_list'] = clientModel.objects.all()
    context['exercises_list'] = exerciseModel.objects.all()
    context['employees_list'] = employeesModel.objects.all()

    return render(request, 'client_list.html', context=context)

@login_required
def add_client(request):

    if request.method == "POST":
        form = clientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = clientForm()

    return render(request, 'add_client.html', {'form': form})


################################################################
####################### EXERCISES VIEWS ########################
################################################################

@login_required
def add_exercise(request, client_pk):
    client = clientModel.objects.get(pk=client_pk)
    if request.method == 'POST':
        form = exerciseForm(request.POST)
        
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.client = client
            exercise.save()
            form.save_m2m()
            
            return redirect('exercise_list', client_pk=client_pk)

    else:
        form = exerciseForm()

    context = {}
    context['client'] = client
    context['form'] = form
    
    return render(request, 'add_exercise.html', context=context)


@login_required
def exercise_list(request, client_pk):

    context = {}
    context['client'] = clientModel.objects.get(pk=client_pk)
    context['exercise_list'] = exerciseModel.objects.filter(client=client_pk)

    return render(request, 'exercise_list.html', context=context)

@login_required
def exercise_detail(request, client_pk, exercise_pk):

    if request.method == 'POST':

        if 'send_mail' in request.POST:
            
            with get_connection(
                host="smtp.live.com", 
                port="25", 
                username="picachus253@hotmail.com", 
                password="s15081998", 
                use_tls=True
            ) as connection:
                EmailMultiAlternatives('diditwork?', 'test message multiemail', 'picachus253@hotmail.com', bcc=['kitivi8869@a6mail.net','sakkuliyda@enayu.com'], connection=connection).send(fail_silently=False)
                return redirect('exercise_detail', client_pk=client_pk, exercise_pk=exercise_pk)

    context = {}
    context['employees_list'] = employeesModel.objects.filter(exercise=exercise_pk)
    context['exercise'] = exerciseModel.objects.get(pk=exercise_pk)
    context['client'] = clientModel.objects.get(pk=client_pk)

    return render(request, 'exercise_detail.html', context=context)

@login_required
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

    context = {}
    context['exercise'] = exerciseModel.objects.get(pk=exercise_pk)
    context['client'] = clientModel.objects.get(pk=client_pk)
    context['form'] = form
    
    return render(request, 'add_employees.html', context=context )


################################################################
####################### CAMPAIGNS VIEWS ########################
################################################################

@login_required
def campaign_list(request):

    context = {}
    context['campaign_list'] = campaignModel.objects.all()

    return render(request, 'campaign_list.html', context=context)

@login_required
def add_campaign(request):

    if request.method == 'POST':
        form = campaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('campaign_list')
    else:
        form = campaignForm()

    return render(request, 'add_campaign.html', {'form':form})

@login_required
def campaign_detail(request, campaign_pk):

    context = {}
    context['campaign'] = campaignModel.objects.get(pk=campaign_pk)

    return render(request, 'campaign_detail.html', context=context)

