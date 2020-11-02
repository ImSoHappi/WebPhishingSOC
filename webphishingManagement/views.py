from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from webphishingAuth.models import *
from .forms import *

# Create your views here.
@login_required
def home(request):
    context = {}
    return render(request, 'management/home.html', context)

@login_required
def client_list(request):
    context = {}

    context['client_list'] = ClientModel.getClients()
    return render(request, 'management/client_list.html', context=context)

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
    print(client)
    
    if client is None:
        messages.error(request, "El cliente seleccionado no existe.")
        return redirect('management_client_list')

    context = {}
    context['client'] = client

    return render(request, 'management/client/addXLS.html', context)