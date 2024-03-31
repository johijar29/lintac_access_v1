from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction
from .models import Equipamiento
from .forms import EquipamientoForm
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404


# Vista para agregar equipamiento
def agregar_equipamiento(request):
    form = EquipamientoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # Aquí simplemente guardamos el nuevo equipamiento sin asignarlo
        form.save()
        messages.success(request, "Equipamiento agregado con éxito al inventario.")
        return redirect('listar_equipamientos')
    else:
        return render(request, "equipamiento/agregar_equipamiento.html", {'form': form})

# Vista para listar equipamientos con paginación (ejemplo básico)
def listar_equipamientos(request):
    # Recoger el tipo de la URL, si existe
    tipo = request.GET.get('tipo')
    if tipo:
        equipamientos = Equipamiento.objects.filter(tipo=tipo)
    else:
        equipamientos = Equipamiento.objects.all()

    # Configuración de la paginación
    paginator = Paginator(equipamientos, 10)  # Muestra 10 equipamientos por página
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # Si la página no es un entero, entregar primera página.
        page_obj = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango (e.g. 9999), entregar última página de resultados.
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "equipamiento/listar_equipamientos.html", {'page_obj': page_obj})

# Vista para editar equipamiento
def editar_equipamiento(request, id):
    equipamiento = get_object_or_404(Equipamiento, pk=id)
    if request.method == "POST":
        form = EquipamientoForm(request.POST, instance=equipamiento)
        if form.is_valid():
            form.save()
            messages.success(request, f"Equipamiento {equipamiento.modelo} actualizado con éxito.")
            return redirect('listar_equipamientos')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = EquipamientoForm(instance=equipamiento)
    return render(request, "equipamiento/editar_equipamiento.html", {'form': form, 'equipamiento': equipamiento})

# Vista para eliminar equipamiento con manejo de transacciones
@transaction.atomic
def eliminar_equipamiento(request, id):
    equipamiento = get_object_or_404(Equipamiento, pk=id)
    if request.method == "POST":
        equipamiento.delete()
        messages.success(request, f"Equipamiento {equipamiento.modelo} eliminado con éxito.")
        return redirect('listar_equipamientos')
    return render(request, "equipamiento/confirmar_eliminacion.html", {'equipamiento': equipamiento})

# Vista para ver los detalles de un equipamiento específico
def detalle_equipamiento(request, pk):
    equipamiento = get_object_or_404(Equipamiento, pk=pk)
    return render(request, 'equipamiento/detalle_equipamiento.html', {'equipamiento': equipamiento})

# Vista home como punto de entrada a la aplicación
def home(request):
    return render(request, 'equipamiento/home.html')



def asignar_equipamiento(request, equipamiento_id):
    # Esta es solo una estructura de ejemplo; necesitarás un formulario para seleccionar a quién se asignará
    if request.method == "POST":
        equipamiento = Equipamiento.objects.get(id=equipamiento_id)
        tipo_asignacion = request.POST.get('tipo_asignacion')
        id_asignacion = request.POST.get('id_asignacion')

        if tipo_asignacion == 'alumno':
            content_type = ContentType.objects.get_for_model(Alumno)
        elif tipo_asignacion == 'funcionario':
            content_type = ContentType.objects.get_for_model(Funcionario)
        else:
            messages.error(request, "Tipo de asignación no válido.")
            return redirect('ruta_correspondiente')

        equipamiento.content_type = content_type
        equipamiento.object_id = id_asignacion
        equipamiento.save()

        messages.success(request, "Equipamiento asignado correctamente.")
        return redirect('ruta_correspondiente')
    else:
        # Renderizar formulario de asignación
        pass