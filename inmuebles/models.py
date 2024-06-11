from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Modelos
class Region(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=50)
    region = models.ForeignKey(Region, related_name='comunas', on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class UsuarioManager(BaseUserManager):
    def create_user(self, correo_electronico, password=None, **extra_fields):
        if not correo_electronico:
            raise ValueError('Los usuarios deben tener una dirección de correo electrónico')
        user = self.model(correo_electronico=self.normalize_email(correo_electronico), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_electronico, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(correo_electronico, password, **extra_fields)

class Usuario(AbstractBaseUser):
    TIPO_USUARIO_CHOICES = [
        ('arrendatario', 'Arrendatario'),
        ('arrendador', 'Arrendador'),
    ]
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    rut = models.CharField(max_length=10, unique=True)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=13)
    tipo_usuario = models.CharField(max_length=12, choices=TIPO_USUARIO_CHOICES)
    correo_electronico = models.EmailField(unique=True, default='correo@correo.cl')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Necesario para acceder al admin de Django

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombres', 'apellidos']  # Correo electrónico ya es requerido por ser USERNAME_FIELD

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'

    def has_perm(self, perm, obj=None):
        "¿El usuario tiene un permiso específico?"
        return True

    def has_module_perms(self, app_label):
        "¿El usuario tiene permisos para ver la app `app_label`?"
        return True

class Inmueble(models.Model):
    TIPO_INMUEBLE_CHOICES = [
        ('departamento', 'Departamento'),
        ('casa', 'Casa'),
        ('oficina', 'Oficina'),
        ('parcela', 'Parcela'),
    ]
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=500)
    imagen = models.ImageField(upload_to='inmuebles/', null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    comuna = models.ForeignKey(Comuna, related_name='inmuebles', on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)
    m2_construidos = models.DecimalField(max_digits=10, decimal_places=2)
    m2_terreno = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_estacionamiento = models.PositiveIntegerField()
    cantidad_banos = models.PositiveIntegerField()
    tipo_de_inmueble = models.CharField(max_length=12, choices=TIPO_INMUEBLE_CHOICES)
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

class Solicitud_Arriendo(models.Model):
    TIPO_PAGO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    arrendatario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensaje = models.TextField(blank=True)
    estado = models.CharField(max_length=10, choices=TIPO_PAGO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Solicitud de {self.inmueble.nombre} por {self.arrendatario.nombres} {self.arrendatario.apellidos}"
