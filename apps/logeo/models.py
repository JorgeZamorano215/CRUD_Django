from django.db import models

# Create your models here.


class mUsuario(models.Model):
    CvPerson = models.IntegerField()
    Login = models.CharField(max_length=20)
    Password = models.CharField(max_length=20)
    FecIni = models.DateField()
    FecFin = models.DateField()
    EdoCta = models.BooleanField()

class mRegistro(models.Model):
    CvUsuario = models.IntegerField()
    CvPerson = models.IntegerField()

#Catalagos para mDireccion
class cCalle(models.Model):
    Ds = models.CharField(max_length=25)

class cColonia(models.Model):
    Ds = models.CharField(max_length=25)
    
class cMunicipio(models.Model):
    Ds = models.CharField(max_length=25)
    
class cCiudad(models.Model):
    Ds = models.CharField(max_length=25)
    
#Tabla Maestra mDireccion
class mDireccion(models.Model):
    CvCalle = models.IntegerField()
    Numero = models.IntegerField()
    CvColonia = models.IntegerField()
    CvMunicipio = models.IntegerField()
    CvCiudad = models.IntegerField()
    CodPos = models.IntegerField()

#Catalagos para mDtPerson
class cNombre(models.Model):
    Ds = models.CharField(max_length=25)
    
class cApellido(models.Model):
    Ds = models.CharField(max_length=25)
    
class cGenero(models.Model):
    Ds = models.CharField(max_length=25)
    
class cTrabajo(models.Model):
    Ds = models.CharField(max_length=25)
    
class cTpPerson(models.Model):
    Ds = models.CharField(max_length=25)
    
class cAficion(models.Model):
    Ds = models.CharField(max_length=25)

#Tabla Maestra mDtPerson
class mDtPerson(models.Model):
    Curp = models.CharField(max_length=18)
    CvNombre = models.IntegerField()
    ApePat = models.IntegerField()
    ApeMat = models.IntegerField()
    CvDireccion = models.IntegerField()
    Telefono = models.IntegerField()
    E_mail = models.CharField(max_length=30)
    CvGenero = models.IntegerField()
    CvTrabajo = models.IntegerField()
    FecNac = models.DateField()
    CvTpPerson = models.IntegerField()
    CvAficion = models.IntegerField()
    Notas = models.CharField(max_length=150)
    
#Tala de Catalagos existentes
class cCatalagos(models.Model):
    Seleccion = models.CharField(max_length=25)
    Nombre = models.CharField(max_length=25)
    
#Tabla Maestra de aplicaciones
class mAplicaciones(models.Model):
    CvAplicaciones = models.CharField(max_length=6)
    DsAplicacion = models.CharField(max_length=50)
    Nivel = models.IntegerField()
    
#Tabla Maestra de aplicaciones
class mAccesos(models.Model):
    CvUsuario = models.IntegerField()
    CvAplicacion = models.IntegerField()
    DsAplicaciones = models.CharField(max_length=6)


    