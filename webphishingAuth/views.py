from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def authentication(request):

    if request.user.is_authenticated:
        return redirect('client_list')

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)
            return redirect('client_list')
        else:
            messages.error(request, 'Usuario o contraseña invalidos.')

    return render(request, 'auth/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('authentication')