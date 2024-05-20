from django import forms
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from apps.logeo.models import mUsuario
from apps.logeo.models import mDtPerson
from apps.logeo.models import mDireccion

from apps.logeo.models import cMunicipio
from apps.logeo.models import cCiudad
from apps.logeo.models import cCalle
from apps.logeo.models import cColonia

from apps.logeo.models import cNombre
from apps.logeo.models import cApellido
from apps.logeo.models import cGenero
from apps.logeo.models import cTpPerson
from apps.logeo.models import cTrabajo
from apps.logeo.models import cAficion

from apps.logeo.models import mAplicaciones


class FormularioRegistrarUsuario(forms.ModelForm):
    
    class Meta:
        model = mUsuario
        fields = ['Login', 'Password', 'FecIni', 'FecFin', 'EdoCta']
        exclude = ['CvPerson'] 
        widgets = {
            'FecIni': forms.DateInput(attrs={'type': 'date'}),
            'FecFin': forms.DateInput(attrs={'type': 'date'}),
            'Password': forms.PasswordInput(attrs={'type': 'password'}),
            'EdoCta': forms.CheckboxInput(attrs={'checked': 'checked'}),
            #estado_cuenta = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'checked': 'checked'}))
        }
        labels = {
            'Login': 'Login del Usuario',
            'Password': 'Password del Usuario',
            'FecIni': 'Fecha de Inicio',
            'FecFin': 'Fecha de Termino',
            'EdoCta': 'Estado de la Cuenta',
        }

    def __init__(self, *args, **kwargs):
        super(FormularioRegistrarUsuario, self).__init__(*args, **kwargs)
        
        # Establecer la fecha del servidor como valor predeterminado para FecIni
        self.fields['FecIni'].initial = datetime.now().strftime('%Y-%m-%d')
        
        # Establecer FecFin como 7 días después de FecIni
        fec_ini = datetime.now()
        fec_fin_default = fec_ini + timedelta(days=7)
        self.fields['FecFin'].initial = fec_fin_default.strftime('%Y-%m-%d')

        # Configurar la restricción de fecha mínima para FecIni
        self.fields['FecIni'].widget.attrs['min'] = self.fields['FecIni'].initial

        # Configurar la restricción de fecha mínima para FecFin
        self.fields['FecFin'].widget.attrs['min'] = self.fields['FecIni'].initial
    
    def clean(self):
        cleaned_data = super().clean()
        fec_ini = cleaned_data.get('FecIni')
        fec_fin = cleaned_data.get('FecFin')

        if fec_ini and fec_fin and fec_fin < fec_ini:
            raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")

        return cleaned_data
    
    

class FormularioModificarUsuario(forms.ModelForm):
    class Meta:
        model = mUsuario
        fields = ['CvPerson','Login', 'Password', 'FecIni', 'FecFin', 'EdoCta']
        exclude = ['CvPerson'] 
        widgets = {
            'FecIni': forms.DateInput(attrs={'type': 'date'}),
            'FecFin': forms.DateInput(attrs={'type': 'date'}),
            'EdoCta': forms.CheckboxInput(),
        }
        labels = {
            'Login': 'Login del Usuario',
            'Password': 'Password del Usuario',
            'FecIni': 'Fecha de Inicio',
            'FecFin': 'Fecha de Termino',
            'EdoCta': 'Estado de la Cuenta',
        }

        

class FormularioLogeoUsuario(forms.ModelForm):
    class Meta:
        model = mUsuario
        fields = 'Login','Password'
        widgets = {
        'Password': forms.PasswordInput(attrs={'type': 'password'})
    }
        
        
class CambioPassword(forms.ModelForm):
    class Meta:
        model = mUsuario
        fields = ['Password']
        widgets = {
        'Password': forms.PasswordInput(attrs={'type': 'password'})
    }
    
class FormularioRegistrarPersonas(forms.ModelForm):
    class Meta:
        model = mDtPerson
        fields = ['Telefono', 'E_mail', 'FecNac', 'Notas']
        widgets = {
            'FecNac': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'FecNac': 'Fecha de Nacimiento',
        }
              
class FormularioNombre(forms.ModelForm):
    class Meta:
        model = cNombre
        fields = ['Ds']
        
        labels = {
            'Ds': 'Descripcion',
        }
class FormularioApellido(forms.ModelForm):
    class Meta:
        model = cApellido
        fields = ['Ds']
        
        labels = {
            'Ds': 'Descripcion',
        }
class FormularioGenero(forms.ModelForm):
    class Meta:
        model = cGenero
        fields = ['Ds']
        
        labels = {
            'Ds': 'Descripcion',
        }
class FormularioTpPerson(forms.ModelForm):
    class Meta:
        model = cTpPerson
        fields = ['Ds']
        
        labels = {
            'Ds': 'Descripcion',
        }
        
class FormularioTrabajo(forms.ModelForm):
    class Meta:
        model = cTrabajo
        fields = ['Ds']
        
        labels = {
            'Ds': 'Descripcion',
        }
        
class FormularioAficion(forms.ModelForm):
    class Meta:
        model = cAficion
        fields = ['Ds']
        
        labels = {
            'Ds': 'Descripcion',
        }
        
class FormularioRegistrarDireccion(forms.ModelForm):
    class Meta:
        model = mDireccion
        fields = ['Numero', 'CodPos']
        
        labels = {
            'CodPos': 'Codigo Postal',
        }

class FormularioColonia(forms.ModelForm):
    class Meta:
        model = cColonia
        fields = ['Ds']
        
        labels = {
            'Ds': 'Descripcion',
        }
        
class FormularioCalle(forms.ModelForm):
    class Meta:
        model = cCalle
        fields = ['Ds']
        
        labels = {
            'Ds': 'Descripcion',
        }
        
class FormularioMunicipio(forms.ModelForm):
    class Meta:
        model = cMunicipio
        fields = ['Ds']
        
        labels = {
            'Ds': 'Descripcion',
        }
        
class FormularioCiudad(forms.ModelForm):
    class Meta:
        model = cCiudad
        fields = ['Ds']
        
        labels = {
            'Ds': 'Descripcion',
        }
        
class FormularioRegistrarAplicaciones(forms.ModelForm):
    class Meta:
        model = mAplicaciones
        fields = ['DsAplicacion']
        
        labels = {
            'DsAplicacion': 'Descripcion de la Aplicacion',
        }
        
class FormularioModificarAplicaciones(forms.ModelForm):
    class Meta:
        model = mAplicaciones
        fields = ['DsAplicacion']
        
        labels = {
            'DsAplicacion': 'Descripcion de la Aplicacion',
        }
        
