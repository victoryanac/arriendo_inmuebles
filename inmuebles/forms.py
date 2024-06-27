from django import forms
from .models import Inmueble, Solicitud_Arriendo, Usuario
from django.contrib.auth.forms import UserCreationForm

class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = [
            'nombre', 'direccion', 'descripcion', 'imagen_url', 'precio', 'comuna', 'disponible',
            'm2_construidos', 'm2_terreno', 'cantidad_estacionamiento', 'cantidad_banos', 'tipo_de_inmueble', 'propietario'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Ingrese la dirección completa'})
        }

class SolicitudArriendoForm(forms.ModelForm):
    class Meta:
        model = Solicitud_Arriendo
        fields = ['inmueble', 'arrendatario', 'mensaje', 'estado']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escriba su mensaje aquí'}),
        }
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['correo_electronico', 'nombres', 'apellidos', 'rut', 'password1', 'password2']

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if Usuario.objects.filter(rut=rut).exists():
            raise forms.ValidationError('Este RUT ya está registrado.')
        return rut


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'telefono']