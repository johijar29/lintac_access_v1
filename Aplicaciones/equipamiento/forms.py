from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import Equipamiento, Alumno, Funcionario


class EquipamientoForm(forms.ModelForm):
    class Meta:
        model = Equipamiento
        fields = ['serie', 'modelo', 'anio_adquisicion']  # Incluir todos los campos del modelo Equipamiento.
        widgets = {
            'anio_adquisicion': forms.NumberInput(attrs={'type': 'number', 'min': 1900, 'max': 2099, 'step': 1}),
            #'ubicacion': forms.Select(),
            'tipo': forms.Select(),
            'estado': forms.Select(),
            # Suponiendo que 'content_type' necesita ser elegido de una lista limitada:
            'content_type': forms.Select(choices=[(ct.id, ct.name) for ct in ContentType.objects.all()]),
        }

    def __init__(self, *args, **kwargs):
        super(EquipamientoForm, self).__init__(*args, **kwargs)
        # Personalización general de campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Específicas
        self.fields['serie'].widget.attrs['placeholder'] = 'Ingrese la serie del equipamiento'
        self.fields['modelo'].widget.attrs['placeholder'] = 'Ingrese el modelo del equipamiento'

        # Filtrar ubicaciones si es necesario, por ejemplo, sólo activas o específicas
        ## self.fields['ubicacion'].queryset = Ubicacion.objects.all()

    # Validaciones personalizadas si son necesarias


class AsignarEquipamientoForm(forms.Form):
    equipamiento_id = forms.ModelChoiceField(
        queryset=Equipamiento.objects.none(),  # Inicialmente vacío, se define en __init__
        label="Equipamiento",
        empty_label="Seleccione un Equipamiento",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tipo_asignacion = forms.ChoiceField(
        choices=[('alumno', 'Alumno'), ('funcionario', 'Funcionario')],
        label="Asignar A",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    id_asignacion = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(AsignarEquipamientoForm, self).__init__(*args, **kwargs)
        # Actualiza el queryset para equipamiento_id con equipamientos no asignados
        self.fields['equipamiento_id'].queryset = Equipamiento.objects.filter(
            content_type__isnull=True, 
            object_id__isnull=True
        )

    def clean(self):
        cleaned_data = super().clean()
        tipo_asignacion = cleaned_data.get("tipo_asignacion")
        id_asignacion = cleaned_data.get("id_asignacion")

        # Valida que el ID proporcionado corresponda a un objeto válido según el tipo de asignación
        if tipo_asignacion == 'alumno':
            if not Alumno.objects.filter(id=id_asignacion).exists():
                self.add_error('id_asignacion', 'El ID de Alumno no es válido.')
        elif tipo_asignacion == 'funcionario':
            if not Funcionario.objects.filter(id=id_asignacion).exists():
                self.add_error('id_asignacion', 'El ID de Funcionario no es válido.')

        return cleaned_data