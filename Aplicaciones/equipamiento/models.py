from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# CHOICES
class EstadoEquipamiento(models.TextChoices):
    ASIGNADO = 'AS', _('Asignado')
    EN_REPARACION = 'ER', _('En Reparación')
    DISPONIBLE = 'DI', _('Disponible')
    REEMPLAZO = 'RE', _('Reemplazo')
    DADO_DE_BAJA = 'DB', _('Dado de Baja')

class TipoEquipamiento(models.TextChoices):
    CHROMEBOOK = 'CB', _('Chromebook')
    NOTEBOOK = 'NB', _('Notebook')
    JABRA = 'JB', _('Jabra')
    WACOM = 'WC', _('Wacom')

class EstadoGeneral(models.TextChoices):
    ACTIVO = 'AC', _('Activo')
    INACTIVO = 'IN', _('Inactivo')
    LICENCIA = 'LI', _('Con Licencia')
    RETIRADO = 'RE', _('Retirado')

class Rol(models.TextChoices):
    PROFESOR = 'PR', _('Profesor')
    PRINCIPAL = 'PL', _('Principal')
    ASISTENTE = 'AS', _('Asistente')
    ENFERMERO = 'EN', _('Enfermero')
    PORTERO = 'PO', _('Portero')

# Modelo Curso
class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    seccion = models.CharField(max_length=20)
    nivel = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} - {self.seccion} - {self.nivel}"

# Modelo Sede
class Sede(models.Model):
    codigo = models.CharField(max_length=2, unique=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

class Ubicacion(models.Model):
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='ubicaciones')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} en {self.sede.nombre}"

# Modelo Persona
class Persona(models.Model):
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    estado = models.CharField(max_length=20, choices=EstadoGeneral.choices)


class Alumno(Persona):
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True)

class Funcionario(Persona):
    rol = models.CharField(max_length=20, choices=Rol.choices)

# Modelo Equipamiento
class Equipamiento(models.Model):
    tipo = models.CharField(max_length=20, choices=TipoEquipamiento.choices)
    modelo = models.CharField(max_length=100)
    serie = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=20, choices=EstadoEquipamiento.choices)
    anio_adquisicion = models.IntegerField()
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True, related_name='equipamientos')
    
    # Ajustes para la relación polimórfica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    asignado_a = GenericForeignKey('content_type', 'object_id')

# Modelo RegistroActividad
class RegistroActividad(models.Model):
    equipamiento = models.ForeignKey(Equipamiento, on_delete=models.CASCADE, related_name='actividades')
    tipo_actividad = models.CharField(max_length=20, choices=EstadoEquipamiento.choices)
    fecha_hora = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.get_tipo_actividad_display()} - {self.equipamiento} el {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"
