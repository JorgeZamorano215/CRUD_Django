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
    Telefono = models.CharField(max_length=20)
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
    
#Tabla Maestra de Productos
class mProductos(models.Model):
    Codigo = models.CharField(max_length=13)
    Producto = models.CharField(max_length=50)
    PreCompra = models.FloatField()
    PreVenta = models.FloatField()
    Utilidad = models.FloatField()
    Stock = models.IntegerField()
    MinStock = models.IntegerField()
    FechaCaducidad = models.DateField()
    Proveedor = models.IntegerField()

#Tabla Maestra de Vetas
class mVentas(models.Model):
    Empleado = models.IntegerField()
    Cliente = models.IntegerField()
    FechaVenta = models.DateField()
    SubTotal = models.FloatField()
    Impuesto = models.FloatField()
    Total = models.FloatField()

#Tabla Transaccional de tVetas    
class tVentas(models.Model):
    CvVenta = models.IntegerField()
    Codigo = models.CharField(max_length=13)
    PrecioVenta = models.FloatField()
    Cantidad = models.IntegerField()
    SubTot = models.FloatField()
    
    
#Tabla Maestra de Peidos
class mPedidos(models.Model):
    Empleado = models.IntegerField()
    Proveedor = models.IntegerField()
    FechaPedido = models.DateField()
    FechaEntrega = models.DateField()
    SubTotal = models.FloatField()
    Impuesto = models.FloatField()
    Total = models.FloatField()
    Anticipo = models.FloatField()
    Pagado = models.BooleanField()
    Recibido = models.BooleanField()    
    
    
#Tabla Transaccional de tVetas    
class tPedidos(models.Model):
    CvPedido = models.IntegerField()
    Codigo = models.CharField(max_length=13)
    PrecioPedido = models.FloatField()
    Cantidad = models.IntegerField()
    SubTot = models.FloatField()


#Tabla Maestra de Recepcion
class mRecepcion(models.Model):
    Empleado = models.IntegerField()
    Proveedor = models.IntegerField()
    FechaPedido = models.DateField()
    FechaRecepcion = models.DateField()
    SubTotal = models.FloatField()
    Impuesto = models.FloatField()
    Total = models.FloatField() 
    Observacion = models.CharField(max_length=200)   
    
#Tabla Transaccional de tRecepcion    
class tRecepcion(models.Model):
    CvRecepcion = models.IntegerField()
    Codigo = models.CharField(max_length=13)
    PrecioRecepcion = models.FloatField()
    Cantidad = models.IntegerField()
    SubTot = models.FloatField()
    Observacion = models.CharField(max_length=200)
    
#Tabla Lista de Faltates    
class listaFaltantes(models.Model):
    Codigo = models.CharField(max_length=13)
    FechaAlerta = models.DateField()
    Pedido = models.BooleanField()
    
#Tabla maestra de Caja Chica    
class mCajaChica(models.Model):
    Monto = models.FloatField()
    CvVenta = models.IntegerField()
    EdoCorte = models.BooleanField()
    FecMovim = models.DateField()
    Empleado = models.IntegerField()
    FecCorte= models.DateField(null=True, blank=True)

#Catalagos para mCajaGrande
class cTpTransaccion(models.Model):
    Ds = models.CharField(max_length=25)
    
class cConcepto(models.Model):
    Ds = models.CharField(max_length=25)
 
#Tabla maestra de Caja Grande    
class mCajaGrande(models.Model):
    Anterior = models.FloatField()
    Monto = models.FloatField()
    Actual = models.FloatField()
    CvTpTransaccion = models.IntegerField()
    CvConcepto = models.IntegerField()
    InfConcepto = models.IntegerField()
    Empleado = models.IntegerField()
    Fecha= models.DateField()
    Observacion = models.CharField(max_length=200)
    
#Tabla maestra de Corte de Caja    
class mCorteCaja(models.Model):
    Empleado = models.IntegerField()
    Monto = models.FloatField()
    Diferencia = models.FloatField()
    Fecha= models.DateField()
    Observacion = models.CharField(max_length=200)    