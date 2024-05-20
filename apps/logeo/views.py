from audioop import reverse
from datetime import date
import datetime
import re
from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q

from django.db.models import Max

from apps.logeo.forms import FormularioLogeoUsuario
from apps.logeo.forms import CambioPassword
from apps.logeo.forms import FormularioRegistrarUsuario
from apps.logeo.forms import FormularioModificarUsuario

from apps.logeo.forms import FormularioRegistrarPersonas
from apps.logeo.forms import FormularioRegistrarDireccion

from apps.logeo.models import mUsuario

from apps.logeo.models import mDtPerson
from apps.logeo.models import cNombre
from apps.logeo.models import cApellido
from apps.logeo.models import cTpPerson
from apps.logeo.models import cGenero
from apps.logeo.models import cTrabajo
from apps.logeo.models import cAficion

from apps.logeo.models import mDireccion
from apps.logeo.models import cColonia
from apps.logeo.models import cCiudad
from apps.logeo.models import cMunicipio
from apps.logeo.models import cCalle

from apps.logeo.models import cCatalagos


from apps.logeo.forms import FormularioApellido
from apps.logeo.forms import FormularioNombre
from apps.logeo.forms import FormularioGenero
from apps.logeo.forms import FormularioTpPerson
from apps.logeo.forms import FormularioTrabajo
from apps.logeo.forms import FormularioAficion
from apps.logeo.forms import FormularioColonia
from apps.logeo.forms import FormularioCiudad
from apps.logeo.forms import FormularioMunicipio
from apps.logeo.forms import FormularioCalle

from apps.logeo.models import mAplicaciones
from apps.logeo.forms import FormularioRegistrarAplicaciones
from apps.logeo.forms import FormularioModificarAplicaciones

from apps.logeo.models import mAccesos
from apps.logeo.models import mRegistro

# Create your views here.
CvPerson=0
CvDireccion=0

Cv = 0
Cv2 = 0
MensajeUsuarios = ''
MensajePersonas = ''
MensajeCatalagos = ''
MensajeAplicaciones = ''
MensajeAccesos = ''
Cvp = 0
NomCat = ''

def inicioSession(request):
    usuario = FormularioLogeoUsuario()
    if request.method == 'GET':
        return render(request, "loginUsuarios.html", {"form":usuario})
    else:
        l = mUsuario.objects.filter(Login=request.POST['Login']).count()
        if l > 0:
            c = mUsuario.objects.filter(Login=request.POST['Login'], Password=request.POST['Password']).count()
            
            if c > 0:
                estado = mUsuario.objects.filter(Login=request.POST['Login'], Password=request.POST['Password'],EdoCta=True).count()
                if estado > 0:
                    from datetime import datetime
                    actual=datetime.today().strftime("%Y-%m-%d")
                    
                    fecha = mUsuario.objects.filter(Login=request.POST['Login'], Password=request.POST['Password'], FecIni__lte=actual).count()
                    #fecha = mUsuario.objects.filter(Login=request.POST['Login'], Password=request.POST['Password'], FecIni__lte=actual, FecFin__gte=actual).count()
                    
                    #p = fecha.get
                    #return render(request, "loginUsuarios.html", {"form":usuario, "error":p})
                    #usuario2 = FormularioCambioPassword()
                    #return render(request, "cambioPassword.html", {"form":usuario2})
                    #today = now().date()
                    if fecha > 0:
                        fecha = mUsuario.objects.filter(Login=request.POST['Login'], Password=request.POST['Password'],  FecFin__gte=actual).count()
                        if fecha > 0:
                            global Cv
                            global Cv2
                            registros = mUsuario.objects.filter(Login=request.POST['Login'], Password=request.POST['Password'])
                            registro = registros[0]
                            Cv = registro.id
                            Cv2 = registro.CvPerson
                            crear_mRegistro(Cv, Cv2)
                            return redirect('Inicio')
                            #return render(request, "home.html")
                        else:
                            fechas = mUsuario.objects.filter(Login=request.POST['Login'], Password=request.POST['Password'])
                            fecha = fechas[0]
                            m = fecha.FecFin
                            registros = mUsuario.objects.filter(Login=request.POST['Login'], Password=request.POST['Password'])
                            registro = registros[0]
                            id_u = registro.id
                            CambioEstado(id_u)
                            return render(request, "loginUsuarios.html", {"form":usuario, "error": f'Cuenta caducada, pongase en contacto con el administrador'})
                    else:
                        fechas = mUsuario.objects.filter(Login=request.POST['Login'], Password=request.POST['Password'])
                        fecha = fechas[0]
                        m = fecha.FecIni
                        return render(request, "loginUsuarios.html", {"form":usuario, "error": f'Cuenta por activar pongase en contacto con su administrador'})
                        #return render(request, "loginUsuarios.html", {"form":usuario, "error": f'Podrás ingresar a partir del {m}'})
                else:
                    return render(request, "loginUsuarios.html", {"form":usuario, "error": 'Su cuenta se ha vencido'})
            else:
                return render(request, "loginUsuarios.html", {"form":usuario, "error": 'Usuario o contraseña incorrectos'})
        else:
            return render(request, "loginUsuarios.html", {"form":usuario, "error": 'Usuario o contraseña incorrectos'})

def crear_mRegistro(CvUsuario, CvPerson):
    nuevo_registro = mRegistro(CvUsuario=CvUsuario, CvPerson=CvPerson)
    nuevo_registro.save()

def cambioPassword(request):
    r = mRegistro.objects.latest('id')
    
    usuario = CambioPassword()
    if request.method == 'GET':
        return render(request, "cambioPassword.html", {"form":usuario})
    else:  
        c = mUsuario.objects.filter(id=r.CvUsuario, Password=request.POST['Password']).count()
        if c > 0:
            if request.POST['Password1'] == request.POST['Password2']:
                c = mUsuario.objects.filter(Password=request.POST['Password1']).count()
                if c == 0:
                    registro = mUsuario.objects.get(id=r.CvUsuario)
                    registro.Password = request.POST['Password1']
                    registro.save()
                    return redirect('login')
                else:
                    return render(request, "cambioPassword.html", {"form":usuario, "error": 'El Password ya lo utiliza un usuario crea otro'})
            else:
                return render(request, "cambioPassword.html", {"form":usuario, "error": 'No coinciden el nuevo Password'})
        else:
            return render(request, "cambioPassword.html", {"form":usuario, "error": 'El Password no es correcto'})
    
def home(request):
    r = mRegistro.objects.latest('id')
    Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()
    
    return render(request, 'home.html', {"Catalago":Catalago, "Personas":Personas, "Usuarios":Usuarios, "Aplicaciones":Aplicaciones, "Accesos":Accesos})

def Menu(request):
    r = mRegistro.objects.latest('id')
    Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    
    return render(request, 'Menu.html', {"Catalago":Catalago, "Personas":Personas, "Usuarios":Usuarios, "Aplicaciones":Aplicaciones})

def inicio(request):
    r = mRegistro.objects.latest('id')
    
    registro = mDtPerson.objects.get(id=r.CvPerson)
    registro.nombre = cNombre.objects.filter(id=registro.CvNombre).first()
    registro.aP = cApellido.objects.filter(id=registro.ApePat).first()
    registro.aM = cApellido.objects.filter(id=registro.ApeMat).first()
    registro.tp = cTpPerson.objects.filter(id=registro.CvTpPerson).first()
    registro.t = cTrabajo.objects.filter(id=registro.CvTrabajo).first()
    
    M =  mAccesos.objects.all()
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()
    
    return render(request, "inicio.html", {"registro":registro, "M":M})

def CambioEstado(id_usuario):
    registro = mUsuario.objects.get(id=id_usuario)
    registro.EdoCta = 0
    registro.save()

def listar_usuarios(request):
    usuarios = mUsuario.objects.all()
    
    for usuario in usuarios:
        usuario.busqueda = mDtPerson.objects.filter(id=usuario.CvPerson).first()
        usuario.nombre = cNombre.objects.filter(id=usuario.busqueda.CvNombre).first()
        usuario.aP = cApellido.objects.filter(id=usuario.busqueda.ApePat).first()
        usuario.aM = cApellido.objects.filter(id=usuario.busqueda.ApeMat).first()
        usuario.tp = cTpPerson.objects.filter(id=usuario.busqueda.CvTpPerson).first()
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=310000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=320000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=330000).count()    
    global MensajeUsuarios
    Mensaje = MensajeUsuarios
    MensajeUsuarios = ""
    
    return render(request, "ListaUsuarios.html", {"usuarios":usuarios, "mensaje":Mensaje, "M":M}) 

def registrar_usuarios(request):
    usuario = FormularioRegistrarUsuario()
    Personas = mDtPerson.objects.all()
    usuarios = mUsuario.objects.all()

    for p in Personas:
        p.n = cNombre.objects.filter(id=p.CvNombre).first()
        p.aP = cApellido.objects.filter(id=p.ApePat).first()
        p.aM = cApellido.objects.filter(id=p.ApeMat).first()
        p.tp = cTpPerson.objects.filter(id=p.CvTpPerson).first()
    for u in usuarios:
        u.busqueda = mDtPerson.objects.filter(id=u.CvPerson).first()
        u.nombre = cNombre.objects.filter(id=u.busqueda.CvNombre).first()
        u.aP = cApellido.objects.filter(id=u.busqueda.ApePat).first()
        u.aM = cApellido.objects.filter(id=u.busqueda.ApeMat).first()
        u.tp = cTpPerson.objects.filter(id=u.busqueda.CvTpPerson).first()
        
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=310000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=320000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=330000).count() 
    
    if request.method == 'GET':
        global MensajeUsuarios
        MensajeUsuarios = ''
        return render(request, "RegistroUsuarios.html", {"form":usuario, "Personas":Personas,"usuarios":usuarios, "M":M})
    else:
        l = mUsuario.objects.filter(Login=request.POST['Login']).count()
        if l == 0:
            p = mUsuario.objects.filter(Password=request.POST['Password']).count()
            if p == 0:
                if request.POST['FecFin'] >= request.POST['FecIni']:
                    seleccion = request.POST['lenguajes']
                    u = FormularioRegistrarUsuario(request.POST)
                    if u.is_valid():
                        u.instance.CvPerson = seleccion
                        u.save()
                        
                        MensajeUsuarios = 'Usuario registrado exitosamente!'
                        return redirect('listarUsuarios')
                    else:
                        return render(request, "RegistroUsuarios.html", {"form":usuario, "Personas":Personas, "usuarios":usuarios, "M":M})
                else:
                    return render(request, "RegistroUsuarios.html", {"form":usuario, "Personas":Personas, "usuarios":usuarios, "error": 'Fecha de Termino debe ser mayor que Fecha de Inicio', "M":M})
            else:
                return render(request, "RegistroUsuarios.html", {"form":usuario, "Personas":Personas, "usuarios":usuarios, "error": 'Utiliza otro Password el que ingresas ya esta registrado', "M":M})
        else:
            return render(request, "RegistroUsuarios.html", {"form":usuario, "Personas":Personas, "usuarios":usuarios, "error": 'Utiliza otro Login el que ingresas ya esta registrado', "M":M})

def editar_usuarios(request, id_usuario):
    usuario = mUsuario.objects.filter(id=id_usuario).first()
    form = FormularioModificarUsuario(instance=usuario)
    usuarios = mUsuario.objects.all()
    Personas = mDtPerson.objects.all()
    
    registro = mDtPerson.objects.get(id=usuario.CvPerson)
    registro.n = cNombre.objects.filter(id=registro.CvNombre).first()
    registro.aP = cApellido.objects.filter(id=registro.ApePat).first()
    registro.aM = cApellido.objects.filter(id=registro.ApeMat).first()
    registro.tp = cTpPerson.objects.filter(id=registro.CvTpPerson).first()
    
    for p in Personas:
        p.n = cNombre.objects.filter(id=p.CvNombre).first()
        p.aP = cApellido.objects.filter(id=p.ApePat).first()
        p.aM = cApellido.objects.filter(id=p.ApeMat).first()
        p.tp = cTpPerson.objects.filter(id=p.CvTpPerson).first()
        
    for u in usuarios:
        u.busqueda = mDtPerson.objects.filter(id=u.CvPerson).first()
        u.nombre = cNombre.objects.filter(id=u.busqueda.CvNombre).first()
        u.aP = cApellido.objects.filter(id=u.busqueda.ApePat).first()
        u.aM = cApellido.objects.filter(id=u.busqueda.ApeMat).first()
        u.tp = cTpPerson.objects.filter(id=u.busqueda.CvTpPerson).first()
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=310000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=320000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=330000).count() 
    
    return render(request, "EditarUsuarios.html", {"form":form, "Personas":Personas, "usuario":usuario, "usuarios":usuarios, "registro":registro, "M":M})
       
def aplicar_editar_usuarios(request, id_usuario):
    usuario = mUsuario.objects.filter(id=id_usuario).first()
    form = FormularioModificarUsuario(instance=usuario)
    usuarios = mUsuario.objects.all()
    Personas = mDtPerson.objects.all()
    
    registro = mDtPerson.objects.get(id=usuario.CvPerson)
    registro.n = cNombre.objects.filter(id=registro.CvNombre).first()
    registro.aP = cApellido.objects.filter(id=registro.ApePat).first()
    registro.aM = cApellido.objects.filter(id=registro.ApeMat).first()
    registro.tp = cTpPerson.objects.filter(id=registro.CvTpPerson).first()
    
    for p in Personas:
        p.n = cNombre.objects.filter(id=p.CvNombre).first()
        p.aP = cApellido.objects.filter(id=p.ApePat).first()
        p.aM = cApellido.objects.filter(id=p.ApeMat).first()
        p.tp = cTpPerson.objects.filter(id=p.CvTpPerson).first()
        
    for u in usuarios:
        u.busqueda = mDtPerson.objects.filter(id=u.CvPerson).first()
        u.nombre = cNombre.objects.filter(id=u.busqueda.CvNombre).first()
        u.aP = cApellido.objects.filter(id=u.busqueda.ApePat).first()
        u.aM = cApellido.objects.filter(id=u.busqueda.ApeMat).first()
        u.tp = cTpPerson.objects.filter(id=u.busqueda.CvTpPerson).first()
        
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=310000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=320000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=330000).count() 
        
    if request.method == 'GET':
        global MensajeUsuarios
        MensajeUsuarios = ''
        return render(request, "EditarUsuarios.html", {"form":form, "Personas":Personas, "usuario":usuario, "usuarios":usuarios, "registro":registro, "M":M})
    else:
        if request.POST['Login'] == usuario.Login:
            if request.POST['Password'] == usuario.Password:
                if request.POST['FecFin'] >= request.POST['FecIni']:
                    usuario = mUsuario.objects.get(pk=id_usuario)
                    form = FormularioModificarUsuario(request.POST, instance=usuario)
                    Cvp = request.POST['lenguajes']
                    if form.is_valid():
                        form.instance.CvPerson = Cvp
                        form.save()
                        MensajeUsuarios = 'Usuario modificado exitosamente!'
                        return redirect('listarUsuarios')
                    else:
                        return render(request, "EditarUsuarios.html", {"form":form, "Personas":Personas, "usuario":usuario, "usuarios":usuarios, "registro":registro, "M":M})
                else:
                    return render(request, "EditarUsuarios.html", {"form":form, "Personas":Personas, "usuario":usuario, "usuarios":usuarios, "registro":registro, "error": 'Fecha de Termino debe ser mayor que Fecha de Inicio', "M":M})    
            else:
                p = mUsuario.objects.filter(Password=request.POST['Password']).count()
                if p == 0:
                    if request.POST['FecFin'] >= request.POST['FecIni']:
                        usuario = mUsuario.objects.get(pk=id_usuario)
                        form = FormularioModificarUsuario(request.POST, instance=usuario)
                        Cvp = request.POST['lenguajes']
                    
                        if form.is_valid():
                            form.instance.CvPerson = Cvp
                            form.save()
                            MensajeUsuarios = 'Usuario modificado exitosamente!'
                            return redirect('listarUsuarios')
                        else:
                            return render(request, "EditarUsuarios.html", {"form":form, "Personas":Personas, "usuario":usuario, "usuarios":usuarios, "registro":registro, "M":M})
                    else:
                        return render(request, "EditarUsuarios.html", {"form":form, "Personas":Personas, "usuario":usuario, "usuarios":usuarios, "registro":registro, "error": 'Fecha de Termino debe ser mayor que Fecha de Inicio', "M":M})    
                else:
                    return render(request, "EditarUsuarios.html", {"form":form, "Personas":Personas, "usuario":usuario, "usuarios":usuarios, "registro":registro, "error": 'Utiliza otro Password el que ingresas ya esta registrado', "M":M})       
        else:        
            l = mUsuario.objects.filter(Login=request.POST['Login']).count()
            if l == 0:
                if request.POST['Password'] == usuario.Password:
                    if request.POST['FecFin'] >= request.POST['FecIni']:
                        usuario = mUsuario.objects.get(pk=id_usuario)
                        form = FormularioModificarUsuario(request.POST, instance=usuario)
                        Cvp = request.POST['lenguajes']
                        if form.is_valid():
                            form.instance.CvPerson = Cvp
                            form.save()
                            MensajeUsuarios = 'Usuario modificado exitosamente!'
                            return redirect('listarUsuarios')
                        else:
                            return render(request, "EditarUsuarios.html", {"form":form, "Personas":Personas, "usuario":usuario, "usuarios":usuarios, "registro":registro, "M":M})
                    else:
                        return render(request, "EditarUsuarios.html", {"form":form, "Personas":Personas, "usuario":usuario, "usuarios":usuarios, "registro":registro, "error": 'Fecha de Termino debe ser mayor que Fecha de Inicio', "M":M})    
                else:
                    p = mUsuario.objects.filter(Password=request.POST['Password']).count()
                    if p == 0:
                        if request.POST['FecFin'] >= request.POST['FecIni']:
                            usuario = mUsuario.objects.get(pk=id_usuario)
                            form = FormularioModificarUsuario(request.POST, instance=usuario)
                            Cvp = request.POST['lenguajes']
                            if form.is_valid():
                                form.instance.CvPerson = Cvp
                                form.save()
                                MensajeUsuarios = 'Usuario modificado exitosamente!'
                                return redirect('listarUsuarios')
                            else:
                                return render(request, "EditarUsuarios.html", {"form":form, "Personas":Personas, "usuario":usuario, "usuarios":usuarios, "registro":registro, "M":M})
                        else:
                            return render(request, "EditarUsuarios.html", {"form":form, "Personas":Personas, "usuario":usuario, "usuarios":usuarios, "registro":registro, "error": 'Fecha de Termino debe ser mayor que Fecha de Inicio, "M":M'})    
                    else:
                        return render(request, "EditarUsuarios.html", {"form":form, "Personas":Personas, "usuario":usuario, "usuarios":usuarios, "registro":registro, "error": 'Utiliza otro Password el que ingresas ya esta registrado', "M":M})     
            else:
                return render(request, "EditarUsuarios.html", {"form":form, "Personas":Personas, "usuario":usuario, "usuarios":usuarios, "registro":registro, "error": 'Utiliza otro Login el que ingresas ya esta registrado', "M":M})
        
def validar_eliminar_usuarios(request, id_usuario):
    usuarios = mUsuario.objects.all()
    for usuario in usuarios:
        usuario.busqueda = mDtPerson.objects.filter(id=usuario.CvPerson).first()
        usuario.nombre = cNombre.objects.filter(id=usuario.busqueda.CvNombre).first()
        usuario.aP = cApellido.objects.filter(id=usuario.busqueda.ApePat).first()
        usuario.aM = cApellido.objects.filter(id=usuario.busqueda.ApeMat).first()
        usuario.tp = cTpPerson.objects.filter(id=usuario.busqueda.CvTpPerson).first()
        
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=310000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=320000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=330000).count()
        
    c = mAccesos.objects.filter(CvUsuario=id_usuario).count()
    if c == 0:
        usuario2 = mUsuario.objects.get(pk=id_usuario)
        usuario2.busqueda = mDtPerson.objects.filter(id=usuario2.CvPerson).first()
        usuario2.nombre = cNombre.objects.filter(id=usuario2.busqueda.CvNombre).first()
        usuario2.aP = cApellido.objects.filter(id=usuario2.busqueda.ApePat).first()
        usuario2.aM = cApellido.objects.filter(id=usuario2.busqueda.ApeMat).first()
        usuario2.tp = cTpPerson.objects.filter(id=usuario2.busqueda.CvTpPerson).first()
        error2 = f"Esta seguro de eliminar a  {usuario2.nombre.Ds}  {usuario2.aP.Ds}  {usuario2.aM.Ds}  ({usuario2.tp.Ds})?"
        return render(request, "ListaUsuarios.html", {"usuarios":usuarios, "error2":error2, "d":usuario2, "M":M})
    else:
        return render(request, "ListaUsuarios.html", {"usuarios":usuarios, "mensaje2":'El usuario cuenta con accesos', "M":M})
    
def eliminar_usuario(request, id_usuario):
    usuario = mUsuario.objects.get(pk=id_usuario)
    usuario.delete()
    global MensajeUsuarios
    MensajeUsuarios = 'Usuario eliminado exitosamente!'
    return redirect('listarUsuarios')

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
            
def listar_catalagos_buscar(request,busqueda):
    global NomCat
    modelo = globals()[NomCat]
    catalagos = modelo.objects.filter(Ds__startswith=busqueda)
    
    listas = cCatalagos.objects.all()
    
    consulta = cCatalagos.objects.filter(Seleccion=NomCat)
    titulo = consulta[0]
    global MensajeCatalagos
    MensajeCatalagos2 = MensajeCatalagos
    MensajeCatalagos = ''
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=110000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=120000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=130000).count() 
    
    return render(request, "ListacatalagosBusqueda.html", {"titulo":titulo.Nombre, "agregar":NomCat, "catalagos":catalagos, "listas":listas, "mensaje":MensajeCatalagos2, "busqueda":busqueda, "M":M}) 

def listar_catalagos(request,modelo_nombre):
    global NomCat 
    NomCat = modelo_nombre
    modelo = globals()[modelo_nombre]
    catalagos = modelo.objects.all()
    
    listas = cCatalagos.objects.all()
    
    consulta = cCatalagos.objects.filter(Seleccion=modelo_nombre)
    titulo = consulta[0]
    global MensajeCatalagos
    MensajeCatalagos2 = MensajeCatalagos
    MensajeCatalagos = ''
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=110000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=120000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=130000).count() 
    
    return render(request, "Listacatalagos.html", {"titulo":titulo.Nombre, "agregar":modelo_nombre, "catalagos":catalagos, "listas":listas, "mensaje":MensajeCatalagos2, "M":M}) 

def registrar_catalagos(request, modelo_nombre):
    if modelo_nombre == "cNombre" or modelo_nombre == "cApellido":
        catalago = FormularioNombre()
    if modelo_nombre == "cApellido":
        catalago = FormularioApellido()
    if modelo_nombre == "cTpPerson":
        catalago = FormularioTpPerson()
    if modelo_nombre == "cGenero":
        catalago = FormularioGenero()
    if modelo_nombre == "cTrabajo":
        catalago = FormularioTrabajo()
    if modelo_nombre == "cAficion":
        catalago = FormularioAficion()
    if modelo_nombre == "cColonia":
        catalago = FormularioColonia()
    if modelo_nombre == "cCiudad":
        catalago = FormularioCiudad()
    if modelo_nombre == "cMunicipio":
        catalago = FormularioMunicipio()
    if modelo_nombre == "cCalle":
        catalago = FormularioCalle()

    modelo = globals()[modelo_nombre]
    catalagos = modelo.objects.all()
    listas = cCatalagos.objects.all()
    consulta = cCatalagos.objects.filter(Seleccion=modelo_nombre)
    titulo = consulta[0]
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=110000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=120000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=130000).count()
    
    if request.method == 'GET':
        global MensajeCatalagos
        MensajeCatalagos = ''
        return render(request, "RegistroCategorias.html", {"Seleccion":titulo.Seleccion, "titulo":titulo.Nombre,"form":catalago, "catalagos":catalagos, "listas":listas, "M":M})
    else:
        c = modelo.objects.filter(Ds=request.POST['Ds']).count()
        if c == 0:
            if modelo_nombre == "cNombre":
                c = FormularioNombre(request.POST)
            if  modelo_nombre == "cApellido":
                c = FormularioApellido(request.POST)
            if modelo_nombre == "cTpPerson":
                c = FormularioTpPerson(request.POST)
            if modelo_nombre == "cGenero":
                c = FormularioGenero(request.POST)
            if modelo_nombre == "cTrabajo":
                c = FormularioTrabajo(request.POST)
            if modelo_nombre == "cAficion":
                c = FormularioAficion(request.POST)
            if modelo_nombre == "cColonia":
                c = FormularioColonia(request.POST)
            if modelo_nombre == "cCiudad":
                c = FormularioCiudad(request.POST)
            if modelo_nombre == "cMunicipio":
                c = FormularioMunicipio(request.POST)
            if modelo_nombre == "cCalle":
                c = FormularioCalle(request.POST)
            
            if c.is_valid():
                
                c.save()
                            
                MensajeCatalagos ='Registrado exitosamente!!!'
                
            
                return redirect('listarCatalagos', modelo_nombre=titulo.Seleccion)
            
            else:
                return render(request, "RegistroCategorias.html", {"Seleccion":titulo.Seleccion, "titulo":titulo.Nombre, "form":catalago, "catalagos":catalagos, "listas":listas, "M":M})
        else:
            return render(request, "RegistroCategorias.html", {"Seleccion":titulo.Seleccion, "titulo":titulo.Nombre, "form":catalago, "catalagos":catalagos, "listas":listas, "mensaje":"Ya existente!!!", "M":M})
                 
def editar_catalagos(request, modelo_nombre, id_catalago):
    modelo = globals()[modelo_nombre]
    catalago = modelo.objects.filter(id=id_catalago).first()
    catalagos = modelo.objects.all()
    listas = cCatalagos.objects.all()
    if modelo_nombre == "cNombre":
        form = FormularioNombre(instance=catalago)
    if modelo_nombre == "cApellido":
        form = FormularioApellido(instance=catalago)
    if modelo_nombre == "cTpPerson":
        form = FormularioTpPerson(instance=catalago)
    if modelo_nombre == "cGenero":
        form = FormularioGenero(instance=catalago)
    if modelo_nombre == "cTrabajo":
        form = FormularioTrabajo(instance=catalago)
    if modelo_nombre == "cAficion":
        form = FormularioAficion(instance=catalago)
    if modelo_nombre == "cColonia":
        form = FormularioColonia(instance=catalago)
    if modelo_nombre == "cCiudad":
        form = FormularioCiudad(instance=catalago)
    if modelo_nombre == "cMunicipio":
        form = FormularioMunicipio(instance=catalago)
    if modelo_nombre == "cCalle":
        form = FormularioCalle(instance=catalago)
    
    consulta = cCatalagos.objects.filter(Seleccion=modelo_nombre)
    titulo = consulta[0]
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=110000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=120000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=130000).count()
    
    return render(request, "EditarCategorias.html", {"Seleccion":titulo.Seleccion, "titulo":titulo.Nombre,"form":form, "catalagos":catalagos, "catalago":catalago, "listas":listas, "M":M})

def aplicar_editar_catalagos(request, modelo_nombre, id_catalago):
    modelo = globals()[modelo_nombre]
    catalago = modelo.objects.filter(id=id_catalago).first()
    catalagos = modelo.objects.all()
    listas = cCatalagos.objects.all()
    if modelo_nombre == "cNombre":
        form = FormularioNombre(instance=catalago)
    if modelo_nombre == "cApellido":
        form = FormularioApellido(instance=catalago)
    if modelo_nombre == "cTpPerson":
        form = FormularioTpPerson(instance=catalago)
    if modelo_nombre == "cGenero":
        form = FormularioGenero(instance=catalago)
    if modelo_nombre == "cTrabajo":
        form = FormularioTrabajo(instance=catalago)
    if modelo_nombre == "cAficion":
        form = FormularioAficion(instance=catalago)
    if modelo_nombre == "cColonia":
        form = FormularioColonia(instance=catalago)
    if modelo_nombre == "cCiudad":
        form = FormularioCiudad(instance=catalago)
    if modelo_nombre == "cMunicipio":
        form = FormularioMunicipio(instance=catalago)
    if modelo_nombre == "cCalle":
        form = FormularioCalle(instance=catalago)
    
    consulta = cCatalagos.objects.filter(Seleccion=modelo_nombre)
    titulo = consulta[0]
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=110000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=120000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=130000).count()
    
    if request.method == 'GET':
        global MensajeCatalagos
        MensajeCatalagos = ''
        return render(request, "EditarCategorias.html", {"Seleccion":titulo.Seleccion, "titulo":titulo.Nombre,"form":form, "catalagos":catalagos, "catalago":catalago, "listas":listas, "M":M})
    else:
        c = modelo.objects.filter(Ds=request.POST['Ds']).count()
        if c == 0:
            
            if modelo_nombre == "cNombre":
                c = FormularioNombre(request.POST, instance=catalago)
            if modelo_nombre == "cApellido":
                c = FormularioApellido(request.POST, instance=catalago)
            if modelo_nombre == "cTpPerson":
                c = FormularioTpPerson(request.POST, instance=catalago)
            if modelo_nombre == "cGenero":
                c = FormularioGenero(request.POST, instance=catalago)
            if modelo_nombre == "cTrabajo":
                c = FormularioTrabajo(request.POST, instance=catalago)
            if modelo_nombre == "cAficion":
                c = FormularioAficion(request.POST, instance=catalago)
            if modelo_nombre == "cColonia":
                c = FormularioColonia(request.POST, instance=catalago)
            if modelo_nombre == "cCiudad":
                c = FormularioCiudad(request.POST, instance=catalago)
            if modelo_nombre == "cMunicipio":
                c = FormularioMunicipio(request.POST, instance=catalago)
            if modelo_nombre == "cCalle":
                c = FormularioCalle(request.POST, instance=catalago)
            
            if c.is_valid():
                
                c.save()
                            
                MensajeCatalagos = 'Modificado exitosamente!!!'
                
            
                return redirect('listarCatalagos', modelo_nombre=titulo.Seleccion)
            
            else:
                return render(request, "EditarCategorias.html", {"Seleccion":titulo.Seleccion, "titulo":titulo.Nombre, "form":form, "catalagos":catalagos, "catalago":catalago, "listas":listas, "M":M})
        else:
            return render(request, "EditarCategorias.html", {"Seleccion":titulo.Seleccion, "titulo":titulo.Nombre, "form":form, "catalagos":catalagos, "catalago":catalago, "listas":listas, "mensaje":"Ya existente!!!", "M":M})
            
def eliminar_catalagos(request, id_catalago):
    
    global NomCat
    modelo = globals()[NomCat]
    
    c = 0
    
    if NomCat == "cNombre":
        c = mDtPerson.objects.filter(CvNombre=id_catalago).count()
    if NomCat == "cApellido":
        c = mDtPerson.objects.filter(ApePat=id_catalago).count() + mDtPerson.objects.filter(ApeMat=id_catalago).count()
    if NomCat == "cTpPerson":
        c = mDtPerson.objects.filter(CvTpPerson=id_catalago).count()
    if NomCat == "cGenero":
        c = mDtPerson.objects.filter(CvGenero=id_catalago).count()
    if NomCat == "cTrabajo":
        c = mDtPerson.objects.filter(CvTrabajo=id_catalago).count()
    if NomCat == "cAficion":
        c = mDtPerson.objects.filter(CvAficion=id_catalago).count()
    if NomCat == "cColonia":
        c = mDireccion.objects.filter(CvColonia=id_catalago).count()
    if NomCat == "cCiudad":
        c = mDireccion.objects.filter(CvCiudad=id_catalago).count()
    if NomCat == "cMunicipio":
        c = mDireccion.objects.filter(CvMunicipio=id_catalago).count()
    if NomCat == "cCalle":
        c = mDireccion.objects.filter(CvCalle=id_catalago).count()
    
    if c == 0:
        return redirect('confirmarEliminarCatalagos', id_catalago=id_catalago)
    else:
        consulta = cCatalagos.objects.filter(Seleccion=NomCat)
        titulo = consulta[0]
        global MensajeCatalagos
        MensajeCatalagos = 'No se puede realizar completa informacion'
        return redirect('listarCatalagos', modelo_nombre=titulo.Seleccion)
    
def confirmacion_eliminar_catalagos(request,id_catalago):
    global NomCat
    modelo = globals()[NomCat]
    catalagos = modelo.objects.all()
    
    listas = cCatalagos.objects.all()
    
    consulta = cCatalagos.objects.filter(Seleccion=NomCat)
    titulo = consulta[0]
    
    Descripcion = modelo.objects.get(pk=id_catalago)
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=110000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=120000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=130000).count()
    
    return render(request, "EliminarCatalagos.html", {"titulo":titulo.Nombre, "agregar":NomCat, "catalagos":catalagos, "listas":listas, "Descripcion":Descripcion, "M":M}) 

def aplicar_eliminar_catalagos(request, id_catalago):
    
    global NomCat
    modelo = globals()[NomCat]
    
    catalago = modelo.objects.get(pk=id_catalago)
    catalago.delete()
    consulta = cCatalagos.objects.filter(Seleccion=NomCat)
    titulo = consulta[0]
    global MensajeCatalagos
    MensajeCatalagos = 'Eliminado exitosamente!!!'
    return redirect('listarCatalagos', modelo_nombre=titulo.Seleccion)
    
def listar_personas(request):
    personas = mDtPerson.objects.all()
    
    for persona in personas:
        persona.Nombre = cNombre.objects.filter(id=persona.CvNombre).first()
        persona.ApellidoPaterno = cApellido.objects.filter(id=persona.ApePat).first()
        persona.ApellidoMaterno = cApellido.objects.filter(id=persona.ApeMat).first()
        persona.Genero = cGenero.objects.filter(id=persona.CvGenero).first()
        persona.Trabajo = cTrabajo.objects.filter(id=persona.CvTrabajo).first()
        persona.TpPerson = cTpPerson.objects.filter(id=persona.CvTpPerson).first()
        persona.Aficion = cAficion.objects.filter(id=persona.CvAficion).first()
        direccion = mDireccion.objects.filter(id=persona.CvDireccion).first()
        calle = cCalle.objects.filter(id=direccion.CvCalle).first()
        colonia = cColonia.objects.filter(id=direccion.CvColonia).first()
        ciudad = cCiudad.objects.filter(id=direccion.CvCiudad).first()
        municipio = cMunicipio.objects.filter(id=direccion.CvMunicipio).first()
    
        persona.DireccionNombre = f"Av. {calle.Ds} {direccion.Numero}, Col. {colonia.Ds}, {municipio.Ds}, {ciudad.Ds} C.P. {direccion.CodPos}."
        
    global MensajePersonas
    MensajePersonas2 = MensajePersonas
    MensajePersonas = ''
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=210000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=220000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=230000).count()
    
    return render(request, "ListaPersonas.html", {"personas":personas, "mensaje":MensajePersonas2, "M":M})

def registrar_personas(request):
    personar = FormularioRegistrarPersonas()
    fdireccion = FormularioRegistrarDireccion()
    
    Nombres = cNombre.objects.all()
    Apellidos = cApellido.objects.all()
    Generos = cGenero.objects.all()
    Trabajos = cTrabajo.objects.all()
    cTpPersons = cTpPerson.objects.all()
    Aficions = cAficion.objects.all()
    
    Calles = cCalle.objects.all()
    Colonias = cColonia.objects.all()
    Ciudads = cCiudad.objects.all()
    Municipios = cMunicipio.objects.all()
        
    personas = mDtPerson.objects.all()
    for persona in personas:
        persona.Nombre = cNombre.objects.filter(id=persona.CvNombre).first()
        persona.ApellidoPaterno = cApellido.objects.filter(id=persona.ApePat).first()
        persona.ApellidoMaterno = cApellido.objects.filter(id=persona.ApeMat).first()
        persona.Genero = cGenero.objects.filter(id=persona.CvGenero).first()
        persona.Trabajo = cTrabajo.objects.filter(id=persona.CvTrabajo).first()
        persona.TpPerson = cTpPerson.objects.filter(id=persona.CvTpPerson).first()
        persona.Aficion = cAficion.objects.filter(id=persona.CvAficion).first()
        direccion = mDireccion.objects.filter(id=persona.CvDireccion).first()
        calle = cCalle.objects.filter(id=direccion.CvCalle).first()
        colonia = cColonia.objects.filter(id=direccion.CvColonia).first()
        ciudad = cCiudad.objects.filter(id=direccion.CvCiudad).first()
        municipio = cMunicipio.objects.filter(id=direccion.CvMunicipio).first()
    
        persona.DireccionNombre = f"Av. {calle.Ds} {direccion.Numero}, Col. {colonia.Ds}, {municipio.Ds}, {ciudad.Ds} C.P. {direccion.CodPos}."
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=210000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=220000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=230000).count()
    
    if request.method == 'GET':
        global MensajePersonas
        MensajePersonas = ''
        return render(request, "RegistroPersonas.html", {"form":personar, "form2":fdireccion, "Nombres":Nombres,"Apellidos":Apellidos, "Generos":Generos, "Trabajos":Trabajos, "cTpPersons":cTpPersons,  "personas":personas, "Calles":Calles, "Colonias":Colonias, "Ciudads":Ciudads, "Municipios":Municipios, "Aficions":Aficions, "M":M})
    else:
        c = mDtPerson.objects.filter(Curp=request.POST['Curp'], CvTpPerson=request.POST['TipoPersona']).count()
        if c == 0:
            personar = FormularioRegistrarPersonas(request.POST)
            fdireccion = FormularioRegistrarDireccion(request.POST)
            if personar.is_valid():
                fdireccion.instance.CvCalle = request.POST['CalleDs']  
                fdireccion.instance.CvColonia = request.POST['ColoniaDs']  
                fdireccion.instance.CvMunicipio = request.POST['MunicipioDs']  
                fdireccion.instance.CvCiudad = request.POST['CiudadDs']                  
                fdireccion.save()
                
                personar.instance.Curp = request.POST['Curp']  
                personar.instance.CvNombre = request.POST['NombrePersona']  
                personar.instance.ApePat = request.POST['ApellidoPaterno']  
                personar.instance.ApeMat = request.POST['ApellidoMaterno']  
                personar.instance.CvGenero = request.POST['GeneroPersona']  
                personar.instance.CvTrabajo = request.POST['TrabajoPersona']  
                personar.instance.CvTpPerson = request.POST['TipoPersona']  
                personar.instance.CvAficion = request.POST['AficionDs']  
                personar.instance.CvDireccion = mDireccion.objects.aggregate(Max('id'))['id__max']  
                personar.save()
                            
                MensajePersonas = 'Registrado exitosamente!'
                return redirect('listarPersonas')
        else:
            existe = mDtPerson.objects.get(Curp=request.POST['Curp'], CvTpPerson=request.POST['TipoPersona'])
            
            return render(request, "RegistroPersonas.html", {"form":personar, "form2":fdireccion, "Nombres":Nombres,"Apellidos":Apellidos, "Generos":Generos, "Trabajos":Trabajos, "cTpPersons":cTpPersons,  "personas":personas, "Calles":Calles, "Colonias":Colonias, "Ciudads":Ciudads, "Municipios":Municipios, "Aficions":Aficions, "mensaje":"Dato repetido", "existe":existe, "M":M})

def validar_registrar_personas(request, curp, tp):
    personar = FormularioRegistrarPersonas()
    fdireccion = FormularioRegistrarDireccion()
    
    Nombres = cNombre.objects.all()
    Apellidos = cApellido.objects.all()
    Generos = cGenero.objects.all()
    Trabajos = cTrabajo.objects.all()
    cTpPersons = cTpPerson.objects.all()
    Aficions = cAficion.objects.all()
    
    Calles = cCalle.objects.all()
    Colonias = cColonia.objects.all()
    Ciudads = cCiudad.objects.all()
    Municipios = cMunicipio.objects.all()
        
    personas = mDtPerson.objects.all()
    for persona in personas:
        persona.Nombre = cNombre.objects.filter(id=persona.CvNombre).first()
        persona.ApellidoPaterno = cApellido.objects.filter(id=persona.ApePat).first()
        persona.ApellidoMaterno = cApellido.objects.filter(id=persona.ApeMat).first()
        persona.Genero = cGenero.objects.filter(id=persona.CvGenero).first()
        persona.Trabajo = cTrabajo.objects.filter(id=persona.CvTrabajo).first()
        persona.TpPerson = cTpPerson.objects.filter(id=persona.CvTpPerson).first()
        persona.Aficion = cAficion.objects.filter(id=persona.CvAficion).first()
        direccion = mDireccion.objects.filter(id=persona.CvDireccion).first()
        calle = cCalle.objects.filter(id=direccion.CvCalle).first()
        colonia = cColonia.objects.filter(id=direccion.CvColonia).first()
        ciudad = cCiudad.objects.filter(id=direccion.CvCiudad).first()
        municipio = cMunicipio.objects.filter(id=direccion.CvMunicipio).first()
    
        persona.DireccionNombre = f"Av. {calle.Ds} {direccion.Numero}, Col. {colonia.Ds}, {municipio.Ds}, {ciudad.Ds} C.P. {direccion.CodPos}."
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=210000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=220000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=230000).count()
    
    c = mDtPerson.objects.filter(Curp=curp, CvTpPerson=tp).count()
    
    if c == 0:
        t = cTpPerson.objects.filter(id=tp).first()
        return render(request, "RegistroPersonas.html", {"form":personar, "form2":fdireccion, "Nombres":Nombres,"Apellidos":Apellidos, "Generos":Generos, "Trabajos":Trabajos, "cTpPersons":cTpPersons,  "personas":personas, "Calles":Calles, "Colonias":Colonias, "Ciudads":Ciudads, "Municipios":Municipios, "Aficions":Aficions, "cur":curp, "t":t, "M":M})
    else:
        existe = mDtPerson.objects.get(Curp=curp, CvTpPerson=tp)
            
        return render(request, "RegistroPersonas.html", {"form":personar, "form2":fdireccion, "Nombres":Nombres,"Apellidos":Apellidos, "Generos":Generos, "Trabajos":Trabajos, "cTpPersons":cTpPersons,  "personas":personas, "Calles":Calles, "Colonias":Colonias, "Ciudads":Ciudads, "Municipios":Municipios, "Aficions":Aficions, "mensaje":"Dato repetido", "existe":existe, "M":M})
                    
def eliminar_persona(request, id_persona):
    global MensajePersonas

    c = mUsuario.objects.filter(CvPerson=id_persona).count()

    if c == 0:
        return redirect('confirmarEliminarPersonas', id_persona=id_persona)
    else:
        MensajePersonas = 'No se puede realizar completa informacion'
        return redirect('listarPersonas')
    
def confirmacion_eliminar_persona(request,id_persona):
    Descripcion = mDtPerson.objects.get(pk=id_persona)
    
    personas = mDtPerson.objects.all()
    
    for persona in personas:
        persona.Nombre = cNombre.objects.filter(id=persona.CvNombre).first()
        persona.ApellidoPaterno = cApellido.objects.filter(id=persona.ApePat).first()
        persona.ApellidoMaterno = cApellido.objects.filter(id=persona.ApeMat).first()
        persona.Genero = cGenero.objects.filter(id=persona.CvGenero).first()
        persona.Trabajo = cTrabajo.objects.filter(id=persona.CvTrabajo).first()
        persona.TpPerson = cTpPerson.objects.filter(id=persona.CvTpPerson).first()
        persona.Aficion = cAficion.objects.filter(id=persona.CvAficion).first()
        direccion = mDireccion.objects.filter(id=persona.CvDireccion).first()
        calle = cCalle.objects.filter(id=direccion.CvCalle).first()
        colonia = cColonia.objects.filter(id=direccion.CvColonia).first()
        ciudad = cCiudad.objects.filter(id=direccion.CvCiudad).first()
        municipio = cMunicipio.objects.filter(id=direccion.CvMunicipio).first()
    
        persona.DireccionNombre = f"Av. {calle.Ds} {direccion.Numero}, Col. {colonia.Ds}, {municipio.Ds}, {ciudad.Ds} C.P. {direccion.CodPos}."
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=210000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=220000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=230000).count()
          
    return render(request, "EliminarPersona.html", {"personas":personas, "Descripcion":Descripcion, "M":M})

def aplicar_eliminar_persona(request, id_persona):
    persona = mDtPerson.objects.get(pk=id_persona)
    persona.delete()
    global MensajePersonas
    MensajePersonas = 'Eliminado exitosamente!!!'
    return redirect('listarPersonas')

def editar_personas(request, id_persona, id_direccion):
    
    global CvPerson
    global CvDireccion
    CvPerson = id_persona
    CvDireccion = id_direccion
    
    p = mDtPerson.objects.filter(id=id_persona).first()
    p.n = cNombre.objects.filter(id=p.CvNombre).first()
    p.ap = cApellido.objects.filter(id=p.ApePat).first()
    p.am = cApellido.objects.filter(id=p.ApeMat).first()
    p.g = cGenero.objects.filter(id=p.CvGenero).first()
    p.t = cTrabajo.objects.filter(id=p.CvTrabajo).first()
    p.tp = cTpPerson.objects.filter(id=p.CvTpPerson).first()
    p.af = cAficion.objects.filter(id=p.CvAficion).first()
    
    d = mDireccion.objects.filter(id=id_direccion).first()
    d.ca = cCalle.objects.filter(id=d.CvCalle).first()
    d.co = cColonia.objects.filter(id=d.CvColonia).first()
    d.ci = cCiudad.objects.filter(id=d.CvCiudad).first()
    d.mu = cMunicipio.objects.filter(id=d.CvMunicipio).first()
    
    personar = FormularioRegistrarPersonas(instance=p)
    fdireccion = FormularioRegistrarDireccion(instance=d)
    
    Nombres = cNombre.objects.all()
    Apellidos = cApellido.objects.all()
    Generos = cGenero.objects.all()
    Trabajos = cTrabajo.objects.all()
    cTpPersons = cTpPerson.objects.all()
    Aficions = cAficion.objects.all()
    
    Calles = cCalle.objects.all()
    Colonias = cColonia.objects.all()
    Ciudads = cCiudad.objects.all()
    Municipios = cMunicipio.objects.all()
        
    personas = mDtPerson.objects.all()
    for persona in personas:
        persona.Nombre = cNombre.objects.filter(id=persona.CvNombre).first()
        persona.ApellidoPaterno = cApellido.objects.filter(id=persona.ApePat).first()
        persona.ApellidoMaterno = cApellido.objects.filter(id=persona.ApeMat).first()
        persona.Genero = cGenero.objects.filter(id=persona.CvGenero).first()
        persona.Trabajo = cTrabajo.objects.filter(id=persona.CvTrabajo).first()
        persona.TpPerson = cTpPerson.objects.filter(id=persona.CvTpPerson).first()
        persona.Aficion = cAficion.objects.filter(id=persona.CvAficion).first()
        direccion = mDireccion.objects.filter(id=persona.CvDireccion).first()
        calle = cCalle.objects.filter(id=direccion.CvCalle).first()
        colonia = cColonia.objects.filter(id=direccion.CvColonia).first()
        ciudad = cCiudad.objects.filter(id=direccion.CvCiudad).first()
        municipio = cMunicipio.objects.filter(id=direccion.CvMunicipio).first()
    
        persona.DireccionNombre = f"Av. {calle.Ds} {direccion.Numero}, Col. {colonia.Ds}, {municipio.Ds}, {ciudad.Ds} C.P. {direccion.CodPos}."
        
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=210000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=220000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=230000).count()
    
    return render(request, "EditarPersonas.html", {"form":personar, "form2":fdireccion, "Nombres":Nombres,"Apellidos":Apellidos, "Generos":Generos, "Trabajos":Trabajos, "cTpPersons":cTpPersons,  "personas":personas, "Calles":Calles, "Colonias":Colonias, "Ciudads":Ciudads, "Municipios":Municipios, "Aficions":Aficions, "p":p, "d":d, "M":M})

def validar_editar_personas(request, curp, tp):
    global CvPerson
    global CvDireccion
    
    p = mDtPerson.objects.filter(id=CvPerson).first()
    p.n = cNombre.objects.filter(id=p.CvNombre).first()
    p.ap = cApellido.objects.filter(id=p.ApePat).first()
    p.am = cApellido.objects.filter(id=p.ApeMat).first()
    p.g = cGenero.objects.filter(id=p.CvGenero).first()
    p.t = cTrabajo.objects.filter(id=p.CvTrabajo).first()
    p.tp = cTpPerson.objects.filter(id=p.CvTpPerson).first()
    p.af = cAficion.objects.filter(id=p.CvAficion).first()
    
    d = mDireccion.objects.filter(id=CvDireccion).first()
    d.ca = cCalle.objects.filter(id=d.CvCalle).first()
    d.co = cColonia.objects.filter(id=d.CvColonia).first()
    d.ci = cCiudad.objects.filter(id=d.CvCiudad).first()
    d.mu = cMunicipio.objects.filter(id=d.CvMunicipio).first()
    
    personar = FormularioRegistrarPersonas(instance=p)
    fdireccion = FormularioRegistrarDireccion(instance=d)
    
    Nombres = cNombre.objects.all()
    Apellidos = cApellido.objects.all()
    Generos = cGenero.objects.all()
    Trabajos = cTrabajo.objects.all()
    cTpPersons = cTpPerson.objects.all()
    Aficions = cAficion.objects.all()
    
    Calles = cCalle.objects.all()
    Colonias = cColonia.objects.all()
    Ciudads = cCiudad.objects.all()
    Municipios = cMunicipio.objects.all()
        
    personas = mDtPerson.objects.all()
    for persona in personas:
        persona.Nombre = cNombre.objects.filter(id=persona.CvNombre).first()
        persona.ApellidoPaterno = cApellido.objects.filter(id=persona.ApePat).first()
        persona.ApellidoMaterno = cApellido.objects.filter(id=persona.ApeMat).first()
        persona.Genero = cGenero.objects.filter(id=persona.CvGenero).first()
        persona.Trabajo = cTrabajo.objects.filter(id=persona.CvTrabajo).first()
        persona.TpPerson = cTpPerson.objects.filter(id=persona.CvTpPerson).first()
        persona.Aficion = cAficion.objects.filter(id=persona.CvAficion).first()
        direccion = mDireccion.objects.filter(id=persona.CvDireccion).first()
        calle = cCalle.objects.filter(id=direccion.CvCalle).first()
        colonia = cColonia.objects.filter(id=direccion.CvColonia).first()
        ciudad = cCiudad.objects.filter(id=direccion.CvCiudad).first()
        municipio = cMunicipio.objects.filter(id=direccion.CvMunicipio).first()
    
        persona.DireccionNombre = f"Av. {calle.Ds} {direccion.Numero}, Col. {colonia.Ds}, {municipio.Ds}, {ciudad.Ds} C.P. {direccion.CodPos}."
    
    
    c = mDtPerson.objects.filter(Q(Curp=curp, CvTpPerson=tp) & ~Q(id=CvPerson)).count()

    if c == 0:
        return render(request, "EditarPersonas.html", {"form":personar, "form2":fdireccion, "Nombres":Nombres,"Apellidos":Apellidos, "Generos":Generos, "Trabajos":Trabajos, "cTpPersons":cTpPersons,  "personas":personas, "Calles":Calles, "Colonias":Colonias, "Ciudads":Ciudads, "Municipios":Municipios, "Aficions":Aficions, "p":p, "d":d, "p.Curp":curp})

    else:
        existe = mDtPerson.objects.get(Curp=curp, CvTpPerson=tp)
        return render(request, "EditarPersonas.html", {"form":personar, "form2":fdireccion, "Nombres":Nombres,"Apellidos":Apellidos, "Generos":Generos, "Trabajos":Trabajos, "cTpPersons":cTpPersons,  "personas":personas, "Calles":Calles, "Colonias":Colonias, "Ciudads":Ciudads, "Municipios":Municipios, "Aficions":Aficions, "p":p, "d":d, "mensaje":"Dato repetido", "existe":existe})
    
def aplicar_editar_personas(request, id_persona, id_direccion):
    p = mDtPerson.objects.filter(id=id_persona).first()
    p.n = cNombre.objects.filter(id=p.CvNombre).first()
    p.ap = cApellido.objects.filter(id=p.ApePat).first()
    p.am = cApellido.objects.filter(id=p.ApeMat).first()
    p.g = cGenero.objects.filter(id=p.CvGenero).first()
    p.t = cTrabajo.objects.filter(id=p.CvTrabajo).first()
    p.tp = cTpPerson.objects.filter(id=p.CvTpPerson).first()
    p.af = cAficion.objects.filter(id=p.CvAficion).first()
    
    d = mDireccion.objects.filter(id=id_direccion).first()
    d.ca = cCalle.objects.filter(id=d.CvCalle).first()
    d.co = cColonia.objects.filter(id=d.CvColonia).first()
    d.ci = cCiudad.objects.filter(id=d.CvCiudad).first()
    d.mu = cMunicipio.objects.filter(id=d.CvMunicipio).first()
    
    personar = FormularioRegistrarPersonas(instance=p)
    fdireccion = FormularioRegistrarDireccion(instance=d)
    
    Nombres = cNombre.objects.all()
    Apellidos = cApellido.objects.all()
    Generos = cGenero.objects.all()
    Trabajos = cTrabajo.objects.all()
    cTpPersons = cTpPerson.objects.all()
    Aficions = cAficion.objects.all()
    
    Calles = cCalle.objects.all()
    Colonias = cColonia.objects.all()
    Ciudads = cCiudad.objects.all()
    Municipios = cMunicipio.objects.all()
        
    personas = mDtPerson.objects.all()
    for persona in personas:
        persona.Nombre = cNombre.objects.filter(id=persona.CvNombre).first()
        persona.ApellidoPaterno = cApellido.objects.filter(id=persona.ApePat).first()
        persona.ApellidoMaterno = cApellido.objects.filter(id=persona.ApeMat).first()
        persona.Genero = cGenero.objects.filter(id=persona.CvGenero).first()
        persona.Trabajo = cTrabajo.objects.filter(id=persona.CvTrabajo).first()
        persona.TpPerson = cTpPerson.objects.filter(id=persona.CvTpPerson).first()
        persona.Aficion = cAficion.objects.filter(id=persona.CvAficion).first()
        direccion = mDireccion.objects.filter(id=persona.CvDireccion).first()
        calle = cCalle.objects.filter(id=direccion.CvCalle).first()
        colonia = cColonia.objects.filter(id=direccion.CvColonia).first()
        ciudad = cCiudad.objects.filter(id=direccion.CvCiudad).first()
        municipio = cMunicipio.objects.filter(id=direccion.CvMunicipio).first()
    
        persona.DireccionNombre = f"Av. {calle.Ds} {direccion.Numero}, Col. {colonia.Ds}, {municipio.Ds}, {ciudad.Ds} C.P. {direccion.CodPos}."
    
    
    if request.method == 'GET':
        global MensajePersonas
        MensajePersonas = ''
        return render(request, "EditarPersonas.html", {"form":personar, "form2":fdireccion, "Nombres":Nombres,"Apellidos":Apellidos, "Generos":Generos, "Trabajos":Trabajos, "cTpPersons":cTpPersons,  "personas":personas, "Calles":Calles, "Colonias":Colonias, "Ciudads":Ciudads, "Municipios":Municipios, "Aficions":Aficions, "p":p, "d":d})
    else:
        c = mDtPerson.objects.filter(Q(Curp=request.POST['Curp'], CvTpPerson=request.POST['TipoPersona']) & ~Q(id=id_persona)).count()
        #MiModelo.objects.filter(Q(campo1=valor_campo1, campo2=valor_campo2) & ~Q(campo3=valor_campo3))
        if c == 0:
            personar = FormularioRegistrarPersonas(request.POST, instance=p)
            fdireccion = FormularioRegistrarDireccion(request.POST, instance=d)
            if personar.is_valid():
                fdireccion.instance.CvCalle = request.POST['CalleDs']  
                fdireccion.instance.CvColonia = request.POST['ColoniaDs']  
                fdireccion.instance.CvMunicipio = request.POST['MunicipioDs']  
                fdireccion.instance.CvCiudad = request.POST['CiudadDs']                  
                fdireccion.save()
                
                personar.instance.Curp = request.POST['Curp']  
                personar.instance.CvNombre = request.POST['NombrePersona']  
                personar.instance.ApePat = request.POST['ApellidoPaterno']  
                personar.instance.ApeMat = request.POST['ApellidoMaterno']  
                personar.instance.CvGenero = request.POST['GeneroPersona']  
                personar.instance.CvTrabajo = request.POST['TrabajoPersona']  
                personar.instance.CvTpPerson = request.POST['TipoPersona']  
                personar.instance.CvAficion = request.POST['AficionDs']  
                personar.instance.CvDireccion = mDireccion.objects.aggregate(Max('id'))['id__max']  
                personar.save()
                            
                MensajePersonas = 'Modificado exitosamente!'
                return redirect('listarPersonas')
        else:
            existe = mDtPerson.objects.get(Curp=request.POST['Curp'], CvTpPerson=request.POST['TipoPersona'])
            return render(request, "EditarPersonas.html", {"form":personar, "form2":fdireccion, "Nombres":Nombres,"Apellidos":Apellidos, "Generos":Generos, "Trabajos":Trabajos, "cTpPersons":cTpPersons,  "personas":personas, "Calles":Calles, "Colonias":Colonias, "Ciudads":Ciudads, "Municipios":Municipios, "Aficions":Aficions, "p":p, "d":d, "mensaje":"Dato repetido", "existe":existe})
        
def listar_aplicaciones(request):
    aplicaciones = mAplicaciones.objects.all().order_by('CvAplicaciones')
    global MensajeAplicaciones
    me = MensajeAplicaciones
    MensajeAplicaciones = ''
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=410000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=420000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=430000).count()
     
    return render(request, "ListaAplicaciones.html", {"aplicaciones":aplicaciones, "mensaje":me, "M":M})

def validar_Cvaplicaciones(request, Cvaplicacion):
    aplicacionr = FormularioRegistrarAplicaciones()
    aplicaciones = mAplicaciones.objects.all().order_by('CvAplicaciones')
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=410000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=420000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=430000).count()
    
    c1 = mAplicaciones.objects.filter(CvAplicaciones=Cvaplicacion).count()
    
    if c1 == 0:
        cantidad_de_ceros = Cvaplicacion.count('0')
        N = 0
        
        if cantidad_de_ceros == 5:
            N = 1
            cadena = Cvaplicacion
            primer_caracter = cadena[0]
            
            patron = re.compile('[A-Fa-f]')
            coincidencias = patron.search(primer_caracter)
            
            if coincidencias is not None:
                if primer_caracter == 'A':
                    CvAplicaciones2 ='900000'
                else:
                    primer_caracter = primer_caracter.upper()
                    # Verificar si la letra está dentro del rango A-F
                    if primer_caracter in 'ABCDEF':
                        # Retorna la letra anterior en el alfabeto
                        primer_caracter_l = chr(ord(primer_caracter) - 1)
                        CvAplicaciones2 = str(primer_caracter_l) + '00000'
                    
            else:
                primer_caracter_int = int(primer_caracter)
                primer_caracter_resta = primer_caracter_int - 1
                CvAplicaciones2 = str(primer_caracter_resta) + '00000'
            
            c = mAplicaciones.objects.filter(CvAplicaciones=CvAplicaciones2).count()
            
            if CvAplicaciones2 == '000000':
                return render(request, "RegistroAplicaciones.html", {"form":aplicacionr, "aplicaciones":aplicaciones, "Cv":Cvaplicacion})
                
            else:
                if c == 0:
                    #Mennsaje = 'El modulo anterior no ha sido registrado'
                    return render(request, "RegistroAplicaciones.html", {"form":aplicacionr, "aplicaciones":aplicaciones, "Cv":Cvaplicacion, "M":M})
                else:
                    return render(request, "RegistroAplicaciones.html", {"form":aplicacionr, "aplicaciones":aplicaciones, "Cv":Cvaplicacion, "M":M})
            
        else:
            N = 2
            
            cadena = Cvaplicacion
            
            primer_caracter = cadena[0]
            
            patron = re.compile('[A-Fa-f]')
            coincidencias = patron.search(primer_caracter)
            
            if coincidencias is not None:
                segundo_caracteres = cadena[1]  # Obtiene los primeros dos caracteres
                segundo_caracteres_int = int(segundo_caracteres)
                segundo_caracteres_resta = segundo_caracteres_int - 1
                CvAplicaciones2 = primer_caracter + str(segundo_caracteres_resta) + '0000'
                   
            else:
                primeros_dos_caracteres = cadena[:2]  # Obtiene los primeros dos caracteres
                primeros_dos_caracteres_int = int(primeros_dos_caracteres)
                primeros_dos_caracteres_resta = primeros_dos_caracteres_int - 1
                CvAplicaciones2 = str(primeros_dos_caracteres_resta) + '0000'
            c = mAplicaciones.objects.filter(CvAplicaciones=CvAplicaciones2).count()
            
            if c == 0:
                Mennsaje = 'La accion en el módulo anterior no ha sido registrado'
            else:
                return render(request, "RegistroAplicaciones.html", {"form":aplicacionr, "aplicaciones":aplicaciones, "Cv":Cvaplicacion, "M":M})
            
        
        return render(request, "RegistroAplicaciones.html", {"form": aplicacionr, "aplicaciones": aplicaciones, "error":Mennsaje, "Cv":Cvaplicacion, "M":M})
            
        
    else:
        d = mAplicaciones.objects.filter(CvAplicaciones=Cvaplicacion).first()
        return render(request, "RegistroAplicaciones.html", {"form":aplicacionr, "aplicaciones":aplicaciones, "error2": 'La Clave ya esta registrada', "d":d, "Cv":Cvaplicacion, "M":M})
    
def registrar_aplicaciones(request):
    aplicacionr = FormularioRegistrarAplicaciones()
    
    aplicaciones = mAplicaciones.objects.all().order_by('CvAplicaciones')
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=410000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=420000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=430000).count()
    
    if request.method == 'GET':
        global MensajeAplicaciones
        MensajeAplicaciones = ''
        return render(request, "RegistroAplicaciones.html", {"form":aplicacionr, "aplicaciones":aplicaciones,  "M":M})
    else:
        
        c1 = mAplicaciones.objects.filter(CvAplicaciones=request.POST['CvAplicaciones']).count()
        
        if c1 == 0:
            c2 = mAplicaciones.objects.filter(DsAplicacion=request.POST['DsAplicacion']).count()
            if c2 == 0:
                
                cantidad_de_ceros = request.POST['CvAplicaciones'].count('0')
                N = 0
                
                if cantidad_de_ceros == 5:
                    N = 1
                    cadena = request.POST['CvAplicaciones']

                    primer_caracter = cadena[0]
                    
                    patron = re.compile('[A-Fa-f]')
                    coincidencias = patron.search(primer_caracter)
                    
                    if coincidencias is not None:
                        if primer_caracter == 'A':
                            CvAplicaciones2 ='900000'
                        else:
                            primer_caracter = primer_caracter.upper()
    
                            # Verificar si la letra está dentro del rango A-F
                            if primer_caracter in 'ABCDEF':
                                # Retorna la letra anterior en el alfabeto
                                primer_caracter_l = chr(ord(primer_caracter) - 1)
                                CvAplicaciones2 = str(primer_caracter_l) + '00000'
                            
                    else:
                        primer_caracter_int = int(primer_caracter)
                        primer_caracter_resta = primer_caracter_int - 1

                        CvAplicaciones2 = str(primer_caracter_resta) + '00000'
                    
                    c = mAplicaciones.objects.filter(CvAplicaciones=CvAplicaciones2).count()
                    
                    if CvAplicaciones2 == '000000':
                        aplicacionr = FormularioRegistrarAplicaciones(request.POST)
                        if aplicacionr.is_valid():
                            aplicacionr.instance.CvAplicaciones = request.POST['CvAplicaciones']    
                            aplicacionr.instance.Nivel = N
                            aplicacionr.save()
                            MensajeAplicaciones = 'Registrado exitosamente!'
                            return redirect('listarAplicaciones')
                        
                    else:
                        
                        if c == 0:
                            #Mennsaje = 'El modulo anterior no ha sido registrado'
                            aplicacionr = FormularioRegistrarAplicaciones(request.POST)
                            if aplicacionr.is_valid():
                                aplicacionr.instance.CvAplicaciones = request.POST['CvAplicaciones']
                                aplicacionr.instance.Nivel = N
                                aplicacionr.save()
                                MensajeAplicaciones = 'Registrado exitosamente!'
                                return redirect('listarAplicaciones')
                        else:
                            
                            aplicacionr = FormularioRegistrarAplicaciones(request.POST)
                            if aplicacionr.is_valid():
                                aplicacionr.instance.CvAplicaciones = request.POST['CvAplicaciones']
                                aplicacionr.instance.Nivel = N
                                aplicacionr.save()
                                MensajeAplicaciones = 'Registrado exitosamente!'
                                return redirect('listarAplicaciones')
                    
                else:
                    N = 2
                    
                    cadena = request.POST['CvAplicaciones']
                    
                    primer_caracter = cadena[0]
                    
                    patron = re.compile('[A-Fa-f]')
                    coincidencias = patron.search(primer_caracter)
                    
                    if coincidencias is not None:
                        segundo_caracteres = cadena[1]  # Obtiene los primeros dos caracteres
                        segundo_caracteres_int = int(segundo_caracteres)
                        segundo_caracteres_resta = segundo_caracteres_int - 1

                        CvAplicaciones2 = primer_caracter + str(segundo_caracteres_resta) + '0000'
                           
                    else:
                        primeros_dos_caracteres = cadena[:2]  # Obtiene los primeros dos caracteres
                        primeros_dos_caracteres_int = int(primeros_dos_caracteres)
                        primeros_dos_caracteres_resta = primeros_dos_caracteres_int - 1

                        CvAplicaciones2 = str(primeros_dos_caracteres_resta) + '0000'

                    c = mAplicaciones.objects.filter(CvAplicaciones=CvAplicaciones2).count()

                    
                    if c == 0:
                        Mennsaje = 'La accion en el módulo anterior no ha sido registrado'
                    else:
                        aplicacionr = FormularioRegistrarAplicaciones(request.POST)
                        if aplicacionr.is_valid():
                            aplicacionr.instance.CvAplicaciones = request.POST['CvAplicaciones']
                            aplicacionr.instance.Nivel = N
                            aplicacionr.save()
                            MensajeAplicaciones = 'Registrado exitosamente!'
                            return redirect('listarAplicaciones')
                    
                aplicacionr.initial = request.POST
                return render(request, "RegistroAplicaciones.html", {"form": aplicacionr, "aplicaciones": aplicaciones, "error":Mennsaje, "Cv":request.POST['CvAplicaciones'],  "M":M})
                
            else:
                d = mAplicaciones.objects.filter(DsAplicacion=request.POST['DsAplicacion']).first()
                aplicacionr.initial = request.POST
                return render(request, "RegistroAplicaciones.html", {"form":aplicacionr, "aplicaciones":aplicaciones, "error2": 'La Descripcion ya esta registrada', "d":d, "Cv":request.POST['CvAplicaciones'],  "M":M})
        else:
            d = mAplicaciones.objects.filter(CvAplicaciones=request.POST['CvAplicaciones']).first()
            aplicacionr.initial = request.POST
            return render(request, "RegistroAplicaciones.html", {"form":aplicacionr, "aplicaciones":aplicaciones, "error2": 'La Clave ya esta registrada', "d":d, "Cv":request.POST['CvAplicaciones'],  "M":M})
            
def editar_aplicaciones(request, id_aplicacion):
    aplicacion = mAplicaciones.objects.filter(id=id_aplicacion).first()
    aplicacionr = FormularioModificarAplicaciones(instance=aplicacion)
    
    aplicaciones = mAplicaciones.objects.all().order_by('CvAplicaciones')
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=410000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=420000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=430000).count()
    
    return render(request, "EditarAplicaciones.html", {"form":aplicacionr, "aplicaciones":aplicaciones, "aplicacion":aplicacion, "M":M})

def aplicar_editar_aplicaciones(request, id_aplicacion):
    aplicacion = mAplicaciones.objects.filter(id=id_aplicacion).first()
    aplicacionr = FormularioModificarAplicaciones(instance=aplicacion)
    
    aplicaciones = mAplicaciones.objects.all().order_by('CvAplicaciones')
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=410000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=420000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=430000).count()
    
    if request.method == 'GET':
        global MensajeAplicaciones
        MensajeAplicaciones = ''
        return render(request, "EditarAplicaciones.html", {"form":aplicacionr, "aplicaciones":aplicaciones, "M":M})
    else:
        
            c2 = mAplicaciones.objects.filter(DsAplicacion=request.POST['DsAplicacion']).count()
            if c2 == 0:
                
                aplicacion = mAplicaciones.objects.get(pk=id_aplicacion)
                aplicacionr = FormularioModificarAplicaciones(request.POST, instance=aplicacion)
                if aplicacionr.is_valid():
                    aplicacionr.save()
                    MensajeAplicaciones = 'Modificado exitosamente!'
                    return redirect('listarAplicaciones')
            
                
            else:
                d = mAplicaciones.objects.filter(DsAplicacion=request.POST['DsAplicacion']).first()
                aplicacionr.initial = request.POST
                return render(request, "EditarAplicaciones.html", {"form":aplicacionr, "aplicaciones":aplicaciones, "error2": 'La Descripcion ya esta registrada', "aplicacion":aplicacion, "d":d, "M":M})

def validar_eliminar_aplicaciones(request, id_aplicacion):
    aplicaciones = mAplicaciones.objects.all().order_by('CvAplicaciones')
    n = mAplicaciones.objects.get(CvAplicaciones=id_aplicacion)
    
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()    
    
    M.btn_Agregar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=410000).count()
    M.btn_Eliminar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=420000).count()
    M.btn_Modificar = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones=430000).count()
    
    if n.Nivel == 2:
        c = mAccesos.objects.filter(DsAplicaciones=id_aplicacion).count()
        if c == 0:
            d = mAplicaciones.objects.get(CvAplicaciones=id_aplicacion)
            error2 = f"Esta seguro de eliminar a  {d.DsAplicacion}?"
            return render(request, "ListaAplicaciones.html", {"aplicaciones":aplicaciones, "error2":error2, "d":d, "M":M})
        else:
            return render(request, "ListaAplicaciones.html", {"aplicaciones":aplicaciones, "mensaje2":'La aplicacion esta asignada a usuarios', "M":M})
    else:
        cadena = n.CvAplicaciones
        primer_caracter = cadena[0]
        cantidad_registros = mAplicaciones.objects.filter(CvAplicaciones__startswith=primer_caracter).count()
        
        if cantidad_registros == 1:
            d = mAplicaciones.objects.get(CvAplicaciones=id_aplicacion)
            error2 = f"Esta seguro de eliminar a  {d.DsAplicacion}?"
            return render(request, "ListaAplicaciones.html", {"aplicaciones":aplicaciones, "error2":error2, "d":d, "M":M})
        else:
            return render(request, "ListaAplicaciones.html", {"aplicaciones":aplicaciones, "mensaje2":'Existen acciones dentro del modulo', "M":M})
    
def eliminar_aplicaciones(request, id_aplicacion):
    aplicacion = mAplicaciones.objects.get(pk=id_aplicacion)
    aplicacion.delete()
    global MensajeAplicaciones
    MensajeAplicaciones = 'Aplicacion eliminada exitosamente!'
    return redirect('listarAplicaciones')

def listar_accesos(request):
    aplicaciones = mAplicaciones.objects.all().order_by('CvAplicaciones')
    
    usuarios = mUsuario.objects.all()
        
    for u in usuarios:
        u.busqueda = mDtPerson.objects.filter(id=u.CvPerson).first()
        u.n = cNombre.objects.filter(id=u.busqueda.CvNombre).first()
        u.aP = cApellido.objects.filter(id=u.busqueda.ApePat).first()
        u.aM = cApellido.objects.filter(id=u.busqueda.ApeMat).first()
        u.tp = cTpPerson.objects.filter(id=u.busqueda.CvTpPerson).first()
        
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()
        
    return render(request, "Accesos.html", {"usuarios":usuarios, "aplicaciones":aplicaciones, "M":M})




def listar_accesos2(request, id_usuario):
    Accesos =  mAccesos.objects.filter(CvUsuario=id_usuario)
    
    aplicaciones_accedidas = mAccesos.objects.filter(CvUsuario=id_usuario).values_list('DsAplicaciones', flat=True)
    aplicaciones_no_accedidas = mAplicaciones.objects.exclude(CvAplicaciones__in=aplicaciones_accedidas).values_list('DsAplicacion', flat=True)
    
    aplicaciones = mAplicaciones.objects.all().order_by('CvAplicaciones')
    
    usuarios = mUsuario.objects.all()
    
    Persona =  mUsuario.objects.get(pk=id_usuario)
    registro = mDtPerson.objects.get(id=Persona.CvPerson)
    Persona.n = cNombre.objects.filter(id=registro.CvNombre).first()
    Persona.aP = cApellido.objects.filter(id=registro.ApePat).first()
    Persona.aM = cApellido.objects.filter(id=registro.ApeMat).first()
    Persona.tp = cTpPerson.objects.filter(id=registro.CvTpPerson).first()
    Persona.Datos = f"{ Persona.n.Ds } { Persona.aP.Ds } { Persona.aM.Ds }  ({ Persona.tp.Ds })"
        
    for u in usuarios:
        u.busqueda = mDtPerson.objects.filter(id=u.CvPerson).first()
        u.n = cNombre.objects.filter(id=u.busqueda.CvNombre).first()
        u.aP = cApellido.objects.filter(id=u.busqueda.ApePat).first()
        u.aM = cApellido.objects.filter(id=u.busqueda.ApeMat).first()
        u.tp = cTpPerson.objects.filter(id=u.busqueda.CvTpPerson).first()
        
    for a in Accesos:
        a.Nombre = mAplicaciones.objects.filter(CvAplicaciones=a.DsAplicaciones).first()
    
        
    r = mRegistro.objects.latest('id')
    M =  mAccesos.objects.all()
    
    M.Catalago = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=1).count()
    M.Personas = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=2).count()
    M.Usuarios = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=3).count()
    M.Aplicaciones = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=4).count()
    M.Accesos = mAccesos.objects.filter(CvUsuario=r.CvUsuario, DsAplicaciones__startswith=5).count()
    
    global MensajeAccesos
    Mensaje = MensajeAccesos
    MensajeAccesos = ""
        
    return render(request, "Accesos.html", {"usuarios":usuarios, "aplicaciones":aplicaciones, "M":M, "Accesos":Accesos, "aplicaciones_accedidas":aplicaciones_accedidas, "aplicaciones_no_accedidas":aplicaciones_no_accedidas, "Persona":Persona, "Mensaje":Mensaje})

def registrar_accesos(request, id_usuario, lista):
    
    
    lista_ids = lista.split(',')
    
    mAccesos.objects.filter(CvUsuario=id_usuario).delete()
    
    for lista_id in lista_ids:
        aplicacion = mAplicaciones.objects.get(DsAplicacion=lista_id)
        nuevo_registro = mAccesos(CvUsuario=id_usuario, CvAplicacion=0, DsAplicaciones=aplicacion.CvAplicaciones)
        nuevo_registro.save()
        
    
    global MensajeAccesos
    MensajeAccesos = "Cambios Aplicados"
    
    return redirect('listaraccesos2', id_usuario=id_usuario)
    