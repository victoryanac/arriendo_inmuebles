from django.contrib import admin
from .models import Region, Comuna, Usuario, Inmueble, Solicitud_Arriendo

# Register your models here.

admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(Usuario)
admin.site.register(Inmueble)
admin.site.register(Solicitud_Arriendo)
