from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Deporte, Evento, Participante, Equipo


class DeporteForm(forms.ModelForm):
    """Formulario para crear y editar Deportes"""

    class Meta:
        model = Deporte
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del deporte'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ingrese una descripción del deporte (opcional)'
            })
        }
        labels = {
            'nombre': 'Nombre del Deporte',
            'descripcion': 'Descripción'
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip()
            if not nombre:
                raise ValidationError("El nombre no puede estar vacío")
        return nombre


class ParticipanteForm(forms.ModelForm):
    """Formulario para crear y editar Participantes"""

    class Meta:
        model = Participante
        fields = ['nombre', 'apellido', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@correo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el teléfono (opcional)'
            })
        }
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'email': 'Email',
            'telefono': 'Teléfono'
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip()
            if not nombre:
                raise ValidationError("El nombre no puede estar vacío")
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if apellido:
            apellido = apellido.strip()
            if not apellido:
                raise ValidationError("El apellido no puede estar vacío")
        return apellido

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()
        return email


class EventoForm(forms.ModelForm):
    """Formulario para crear y editar Eventos"""

    class Meta:
        model = Evento
        fields = ['nombre', 'deporte', 'fecha', 'lugar', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del evento'
            }),
            'deporte': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fecha': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'lugar': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el lugar del evento'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ingrese una descripción del evento (opcional)'
            })
        }
        labels = {
            'nombre': 'Nombre del Evento',
            'deporte': 'Deporte',
            'fecha': 'Fecha y Hora',
            'lugar': 'Lugar',
            'descripcion': 'Descripción'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['deporte'].queryset = Deporte.objects.all().order_by('nombre')

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip()
            if not nombre:
                raise ValidationError("El nombre no puede estar vacío")
        return nombre

    def clean_lugar(self):
        lugar = self.cleaned_data.get('lugar')
        if lugar:
            lugar = lugar.strip()
            if not lugar:
                raise ValidationError("El lugar no puede estar vacío")
        return lugar

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha:
            # Validar que la fecha no sea en el pasado
            if fecha < timezone.now():
                raise ValidationError("No se pueden crear eventos en el pasado")
        return fecha



class EquipoForm(forms.ModelForm):
    """Formulario para crear y editar Equipos"""

    class Meta:
        model = Equipo
        fields = ['nombre', 'deporte', 'ciudad', 'fecha_fundacion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del equipo'
            }),
            'deporte': forms.Select(attrs={
                'class': 'form-control'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la ciudad'
            }),
            'fecha_fundacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
        labels = {
            'nombre': 'Nombre del Equipo',
            'deporte': 'Deporte',
            'ciudad': 'Ciudad',
            'fecha_fundacion': 'Fecha de Fundación'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['deporte'].queryset = Deporte.objects.all().order_by('nombre')

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip()
            if not nombre:
                raise ValidationError("El nombre no puede estar vacío")
        return nombre

    def clean_ciudad(self):
        ciudad = self.cleaned_data.get('ciudad')
        if ciudad:
            ciudad = ciudad.strip()
            if not ciudad:
                raise ValidationError("La ciudad no puede estar vacía")
        return ciudad