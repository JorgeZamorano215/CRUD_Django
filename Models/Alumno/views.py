from django.http import HttpRequest
from django.shortcuts import render

from Models.Alumno.forms import FormularioAlumno
from Models.Alumno.models import Alumno

    # views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import SuperuserCreationForm


class FormularioAlumnoView(HttpRequest):
    
    def index(request):
        alumno = FormularioAlumno()
        return render(request, "AlumnoIndex.html", {"form":alumno})
    
    def procesar_formulario(request):
        alumno = FormularioAlumno(request.POST)
        if alumno.is_valid():
            alumno.save()
            alumno = FormularioAlumno()
        return render(request, "AlumnoIndex.html", {"form":alumno, "mensaje":"OK"})
    
    def listar_alumnos(request):
        alumnos = Alumno.objects.all()
        return render(request, "ListaAlumnos.html", {"alumnos":alumnos})
    
    def edit(request, id_alumno):
        alumno = Alumno.objects.filter(id=id_alumno).first()
        form = FormularioAlumno(instance=alumno)
        return render(request, "AlumnoEdit.html", {"form":form, "alumno":alumno})
    
    def actualizar_alumno(request, id_alumno):
        alumno = Alumno.objects.get(pk=id_alumno)
        form = FormularioAlumno(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
        alumnos = Alumno.objects.all()
        return render(request, "ListaAlumnos.html", {"alumnos":alumnos})
    
    def delete(request, id_alumno):
        alumno = Alumno.objects.get(pk=id_alumno)
        alumno.delete()
        alumnos = Alumno.objects.all()
        return render(request, "ListaAlumnos.html", {"alumnos":alumnos, "mensaje":"OK"})
    
    def create_superuser_view(request):
        if request.method == 'POST':
            form = SuperuserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_superuser = True
                user.is_staff = True
                user.password = make_password(form.cleaned_data['password'])  # Hashear la contraseña
                user.save()
                return redirect('crear_superusuario') # Redirigir a una página de éxito o de inicio de sesión
        else:
            form = SuperuserCreationForm()
        return render(request, 'create_superuser.html', {'form': form})