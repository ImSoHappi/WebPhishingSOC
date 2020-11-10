from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse

from webphishingAuth.models import *
from webphishingClient.models import ClientFiles

from io import StringIO, BytesIO

import pandas as pd
import numpy as np
import csv 

from .forms import *
from .tasks import CreateUsersFromXLS, DistributeUsersTask

# Create your views here.
@login_required
def home(request):
    context = {}
    return render(request, 'management/home.html', context)

@login_required
def client_list(request):
    context = {}

    context['client_list'] = ClientModel.getClients()
    return render(request, 'management/client/list.html', context=context)

@login_required
def add_client(request):
    if request.method == "POST":
        form = AddClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('management_client_list')
    else:
        form = AddClientForm()

    return render(request, 'management/add_client.html', {'form': form})

@login_required
def client_view(request, client_pk):
    client = ClientModel.getClient(client_pk)
    
    if client is None:
        messages.error(request, "El cliente seleccionado no existe.")
        return redirect('management_client_list')

    context = {}

    #if request.method == "POST":
    #    pages = Paginator(client.getColaborators(), 20)
    #else:
    #    pages = Paginator(client.getColaborators(), 20)

    # Pagination
    pages = Paginator(client.getColaborators(), 20)
    page_number = request.GET.get('page')
    page_obj = pages.get_page(page_number)

    # Ejercicios
    #exercises = client.getExercises()

    context['client'] = client
    context['colaborator_pagination'] = page_obj
    return render(request, 'management/client/view.html', context)

@login_required
def client_addXLS(request, client_pk):
    client = ClientModel.getClient(client_pk)
    
    if client is None:
        messages.error(request, "El cliente seleccionado no existe.")
        return redirect('management_client_list')

    context = {}

    if request.method == "POST":
        form = AddXLSToClientForm(request.POST, request.FILES)
        if form.is_valid():
            xlsfile = ClientFiles()
            xlsfile.client = client
            xlsfile.file_data = form.cleaned_data.get('xls')           
            xlsfile.save()
            messages.success(request, "Se ha cargado el archivo correctamente.")

            return redirect('management_client_xls_preview', client_pk = client.pk, file_id = xlsfile.pk)
            
        else:
            messages.error(request, "Ha ocurrido un error al cargar el archivo.")

    else:
        form = AddXLSToClientForm()

    context['client'] = client
    context['form'] = form

    return render(request, 'management/client/addXLS.html', context)

@login_required
def client_xls_preview(request, client_pk, file_id):
    context = {}

    client = ClientModel.getClient(client_pk)
    if client is None:
        messages.error(request, "El cliente seleccionado no existe.")
        return redirect('management_client_list')

    file_xls = client.getFileById(file_id)
    if file_xls is None:
        messages.error(request, "El archivo no existe en ese cliente.")
        return redirect('management_client_list')

    # Pandas Process file
    df = pd.read_excel(file_xls.file_data.open('rb'), header = 0)
    df.columns = df.columns.str.strip().str.lower()
    fields = list(df.columns)

    # Clean nan
    df = df.replace(np.nan, '-', regex=True)

    # Data
    context['file_headers'] = list(df.columns)
    context['data'] = df.head(25)
    context['client'] = client
    context['file'] = file_xls
    context['field_analytics'] = fields
    context['row_count'] = df["email"].count()
    context['column_count'] = len(fields)
    
    return render(request, 'management/client/previewXLS.html', context)

@login_required
def client_xls_delete(request, client_pk, file_id):
    context = {}

    client = ClientModel.getClient(client_pk)
    if client is None:
        messages.error(request, "El cliente seleccionado no existe.")
        return redirect('management_client_list')

    file_xls = client.getFileById(file_id)
    if file_xls is None:
        messages.error(request, "El archivo no existe en ese cliente.")
        return redirect('management_client_list')

    file_xls.delete()
    messages.success(request, "Se ha eliminado el archivo correctamente.")
    return redirect('management_client_addXLS', client_pk = client.pk)

@login_required
def client_xls_process(request, client_pk, file_id):
    context = {}

    client = ClientModel.getClient(client_pk)
    if client is None:
        messages.error(request, "El cliente seleccionado no existe.")
        return redirect('management_client_list')

    file_xls = client.getFileById(file_id)
    if file_xls is None:
        messages.error(request, "El archivo no existe en ese cliente.")
        return redirect('management_client_list')
    
    # Create task
    task = CreateUsersFromXLS.delay(client_pk, file_id)
    client.last_task = task
    client.save()
    messages.success(request, "El archivo fue enviado a procesamiento.")

    return redirect('management_client_list')

@login_required
def client_xls_export(request, client_pk):
    context = {}

    client = ClientModel.getClient(client_pk)
    if client is None:
        messages.error(request, "El cliente seleccionado no existe.")
        return redirect('management_client_list')

    # Creating data
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="list.csv"'

    writer = csv.writer(response)
    writer.writerow(['guid', 'email'])

    for colaborator in client.getColaborators():
        writer.writerow([colaborator.pk, colaborator.email])

    return response

@login_required
def client_exercise_crud(request, client_pk, exercise_pk = None):
    context = {}

    client = ClientModel.getClient(client_pk)
    if client is None:
        messages.error(request, "El cliente seleccionado no existe.")
        return redirect('management_client_list')

    if exercise_pk is not None:
        exercise = client.getExerciseById(exercise_pk)
        if exercise is None:
            messages.error(request, "El ejercicio no exite dentro de este cliente")
            return redirect('management_client_view', client_pk = client.pk)
    else:
        exercise = None
    
    form = AddModifyExercise(instance = exercise)
    if request.method == "POST":
        if "delete_exercise" in request.POST and exercise_pk is not None:
            exercise.delete()
            messages.success(request, "El ejercicio ha sido eliminado")
            return redirect('management_client_view', client_pk = client.pk) 

        form = AddModifyExercise(request.POST, instance = exercise)
        if form.is_valid():
            dataobject = form.save(commit=False)
            dataobject.client = client
            dataobject.save()

            messages.success(request, "Ejercicio editado o agregado correctamente")
            return redirect('management_client_view', client_pk = client.pk)
    
    context['form'] = form
    context['client'] = client
    return render(request, 'management/exercise/crud.html', context)

@login_required
def client_exercise_distribute_users(request, client_pk, exercise_pk):
    context = {}

    client = ClientModel.getClient(client_pk)
    if client is None:
        messages.error(request, "El cliente seleccionado no existe.")
        return redirect('management_client_list')

    exercise = client.getExerciseById(exercise_pk)
    if exercise is None:
        messages.error(request, "El ejercicio seleccionado no existe.")
        return redirect('management_client_view', client_pk = client.pk)

    ## Get colaborators from client
    campaigns = exercise.getCampanas()
    totalColab = client.getColaborators().count()
    availableFields = client.getColaboratorFilters()

    # Apply filter
    if request.method == "POST":
        form = DistributeClientUsersForm(request.POST)
        form.fields['campaign'].queryset = campaigns

        if form.is_valid():
            # Get campaign
            campaignId = request.POST.get("campaign", None)

            # Filter colabns
            colabFilter = request.POST.get('query', None)
            context['colabFilter'] = colabFilter
            colaborators = client.getFilteredColaborators(colabFilter)

            if not "filter" in request.POST:
                task = DistributeUsersTask.delay(client.pk, campaignId, colabFilter)
                client.last_task = task
                client.save()

                messages.success(request, "Distribución en progreso...")
                return redirect('management_client_view', client_pk = client.pk)
            
        else:
            colaborators = client.getColaborators()
    else:
        colaborators = client.getColaborators()
        form = DistributeClientUsersForm()
        form.fields['campaign'].queryset = campaigns
    

    ## Build form
    context['availableFields'] = availableFields
    context['colaborators'] = colaborators
    context['totalColab'] = totalColab
    context['colabPercentage'] = round(colaborators.count() / totalColab * 100, 2)
    context['campaigns'] = campaigns
    context['client'] = client
    context['form'] = form
    return render(request, 'management/exercise/distribute_users.html', context = context)

@login_required
def client_campaign_crud(request, client_pk, exercise_pk, campaign_pk = None):
    context = {}

    client = ClientModel.getClient(client_pk)
    if client is None:
        messages.error(request, "El cliente seleccionado no existe.")
        return redirect('management_client_list')

    exercise = client.getExerciseById(exercise_pk)
    if exercise is None:
        messages.error(request, "El ejercicio seleccionado no existe.")
        return redirect('management_client_view', client_pk = client.pk)

    if campaign_pk is not None:
        campaign = exercise.getCampaingById(campaign_pk)
        if campaign is None:
            messages.error(request, "La campaña no exite dentro de este ejercicio")
            return redirect('management_client_view', client_pk = client.pk)
    else:
        campaign = None

    form = AddModifyCampaign(instance = campaign)
    if request.method == "POST":
        if "delete_campaign" in request.POST and campaign_pk is not None:
            campaign.delete()
            messages.success(request, "La campaña ha sido eliminada")
            return redirect('management_client_view', client_pk = client.pk) 

        form = AddModifyCampaign(request.POST, request.FILES, instance = campaign)
        if form.is_valid():
            dataobject = form.save(commit=False)
            dataobject.client = client
            dataobject.exercise = exercise
            dataobject.save()

            messages.success(request, "Campaña editada o agregada correctamente")
            return redirect('management_client_view', client_pk = client.pk)
    
    # Load colaborators in this campaign

    context['form'] = form
    context['client'] = client
    context['campaign'] = campaign
    return render(request, 'management/exercise/campaign_crud.html', context)

@login_required
def client_colaborator_crud(request, client_pk, colaborator_pk = None):
    context = {}

    client = ClientModel.getClient(client_pk)
    if client is None:
        messages.error(request, "El cliente seleccionado no existe.")
        return redirect('management_client_list')

    if colaborator_pk is not None:
        colaborator = client.getColaboratorById(colaborator_pk)
        if colaborator is None:
            messages.error(request, "El colaborador no exite dentro de este cliente")
            return redirect('management_client_view', client_pk = client.pk)
    else:
        colaborator = None
    
    form = AddModifyColaborator(instance = colaborator)
    if request.method == "POST":
        if "delete_colaborator" in request.POST and colaborator_pk is not None:
            colaborator.delete()
            messages.success(request, "El colaborador ha sido eliminado")
            return redirect('management_client_view', client_pk = client.pk) 

        form = AddModifyColaborator(request.POST, instance = colaborator)
        if form.is_valid():
            dataobject = form.save(commit=False)
            dataobject.client = client
            dataobject.save()

            messages.success(request, "Colaborador editado o agregado correctamente")
            return redirect('management_client_view', client_pk = client.pk)
    
    context['form'] = form
    context['client'] = client
    return render(request, 'management/client/colaborator_crud.html', context)