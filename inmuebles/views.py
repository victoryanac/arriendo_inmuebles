from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Inmueble
from .forms import InmuebleForm, SolicitudArriendoForm, UserRegisterForm, UserUpdateForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Obtener el modelo de usuario personalizado
Usuario = get_user_model()


def index(request):
    tipo_inmueble = request.GET.get('tipo', None)
    if tipo_inmueble:
        inmuebles = Inmueble.objects.filter(tipo_de_inmueble=tipo_inmueble)
    else:
        inmuebles = Inmueble.objects.all()
    return render(request, 'index.html', {'inmuebles': inmuebles, 'tipo_inmueble': tipo_inmueble})




# Vista para listar todos los inmuebles
def inmueble_list(request):
    inmuebles = Inmueble.objects.all()
    return render(request, 'inmueble_list.html', {'inmuebles': inmuebles})

# Vista para mostrar los detalles de un inmueble específico
def inmueble_detail(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk)
    return render(request, 'inmueble_detail.html', {'inmueble': inmueble})

# Vista para crear un nuevo inmueble
def inmueble_create(request):
    if request.method == 'POST':
        form = InmuebleForm(request.POST)
        if form.is_valid():
            new_inmueble = form.save(commit=False)
            # Asumiendo que necesitas asignar algún atributo adicional como el propietario
            new_inmueble.propietario = request.user
            new_inmueble.save()
            return redirect('inmueble_list')
    else:
        form = InmuebleForm()
    return render(request, 'inmueble_form.html', {'form': form})

# Vista para editar un inmueble existente
def inmueble_edit(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk)
    if request.method == 'POST':
        form = InmuebleForm(request.POST, request.FILES, instance=inmueble)
        if form.is_valid():
            form.save()
            return redirect('inmueble_list')
    else:
        form = InmuebleForm(instance=inmueble)
    return render(request, 'inmueble_form.html', {'form': form})

# Vista para crear una nueva solicitud de arriendo
def solicitud_arriendo_create(request):
    if request.method == 'POST':
        form = SolicitudArriendoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inmueble_list')
    else:
        form = SolicitudArriendoForm()
    return render(request, 'solicitud_arriendo_form.html', {'form': form})



#registro de usuarios
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado exitosamente!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})




@login_required
def user_profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})


