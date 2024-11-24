from django.db import models

# forms.py
from django import forms
from django.contrib.auth.models import User

class Alumno(models.Model):
    nombre = models.CharField(max_length=75)
    apellido = models.CharField(max_length=75)
    telefono = models.CharField(max_length=12)
    fecha_nacimiento = models.DateField()
    codigo = models.IntegerField()

