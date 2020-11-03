from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from webphishingAuth.models import *
from webphishingClient.models import ClientFiles

from io import StringIO

import pandas as pd
import numpy as np
from .forms import *
from .tasks import CreateUsersFromXLS

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