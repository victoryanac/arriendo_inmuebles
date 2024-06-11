from django import forms
from .models import Inmueble, Solicitud_Arriendo

class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = [
            'nombre', 'direccion', 'descripcion', 'imagen', 'precio', 'comuna', 'disponible',
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
