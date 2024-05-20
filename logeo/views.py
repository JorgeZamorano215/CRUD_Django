from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

from apps.logeo.forms import FormularioLogeoUsuario


# Create your views here.
def inicioSession(request):
    if request.method == 'GET':
        usuario = FormularioLogeoUsuario()
        return render(request, "loginUsuarios.html", {"form":usuario})
    else:
        if request.POST['password1'] == '':
            return render(request, "loginUsuarios.html", {"form":usuario, "error": 'Campo vacio'})    
    


def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'loginUsuarios.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #registarr usuario
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password2'])
                user.save()
                return HttpResponse('User created successfully')
            except:
                return render(request, 'loginUsuarios.html', {
                    'form': UserCreationForm,
                    "error": 'username already exists'            
                })
        return HttpResponse('Password do not match')


    
    