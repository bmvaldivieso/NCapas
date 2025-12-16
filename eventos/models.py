from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone


class Deporte(models.Model):
    """Modelo para representar un deporte"""
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Deporte"
        verbose_name_plural = "Deportes"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Participante(models.Model):
    """Modelo para representar un participante"""
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    email = models.EmailField(unique=True, validators=[EmailValidator()], verbose_name="Email")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"


class Evento(models.Model):
    """Modelo para representar un evento deportivo"""
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    deporte = models.ForeignKey(
        Deporte,
        on_delete=models.CASCADE,
        related_name='eventos',
        verbose_name="Deporte"
    )
    fecha = models.DateTimeField(verbose_name="Fecha del Evento")
    lugar = models.CharField(max_length=200, verbose_name="Lugar")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    participantes = models.ManyToManyField(
        Participante,
        through='EventoParticipante',
        related_name='eventos',
        verbose_name="Participantes"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.nombre} - {self.deporte.nombre}"


class EventoParticipante(models.Model):
    """Modelo intermedio para la relación Many-to-Many entre Evento y Participante"""
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, verbose_name="Evento")
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, verbose_name="Participante")
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Inscripción")
    numero_inscripcion = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número de Inscripción")

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        unique_together = ['evento', 'participante']
        ordering = ['-fecha_inscripcion']

    def __str__(self):
        return f"{self.participante.nombre_completo} - {self.evento.nombre}"

class Equipo(models.Model):
    """Modelo para representar un equipo deportivo"""
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    deporte = models.ForeignKey(
        Deporte,
        on_delete=models.CASCADE,
        related_name='equipos',
        verbose_name="Deporte"
    )
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")
    fecha_fundacion = models.DateField(blank=True, null=True, verbose_name="Fecha de Fundación")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.deporte.nombre})"        
