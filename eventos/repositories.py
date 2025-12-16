from typing import List, Optional
from django.db.models import QuerySet
from .models import Deporte, Evento, Participante, EventoParticipante, Equipo


class DeporteRepository:
    """Repositorio para operaciones de acceso a datos de Deporte"""

    @staticmethod
    def get_all() -> QuerySet[Deporte]:
        """Obtener todos los deportes"""
        return Deporte.objects.all()

    @staticmethod
    def get_by_id(deporte_id: int) -> Optional[Deporte]:
        """Obtener un deporte por su ID"""
        try:
            return Deporte.objects.get(pk=deporte_id)
        except Deporte.DoesNotExist:
            return None

    @staticmethod
    def get_by_nombre(nombre: str) -> Optional[Deporte]:
        """Obtener un deporte por su nombre"""
        try:
            return Deporte.objects.get(nombre=nombre)
        except Deporte.DoesNotExist:
            return None

    @staticmethod
    def create(nombre: str, descripcion: str = None) -> Deporte:
        """Crear un nuevo deporte"""
        return Deporte.objects.create(nombre=nombre, descripcion=descripcion)

    @staticmethod
    def update(deporte: Deporte, nombre: str = None, descripcion: str = None) -> Deporte:
        """Actualizar un deporte existente"""
        if nombre:
            deporte.nombre = nombre
        if descripcion is not None:
            deporte.descripcion = descripcion
        deporte.save()
        return deporte

    @staticmethod
    def delete(deporte_id: int) -> bool:
        """Eliminar un deporte por su ID"""
        try:
            deporte = Deporte.objects.get(pk=deporte_id)
            deporte.delete()
            return True
        except Deporte.DoesNotExist:
            return False


class ParticipanteRepository:
    """Repositorio para operaciones de acceso a datos de Participante"""

    @staticmethod
    def get_all() -> QuerySet[Participante]:
        """Obtener todos los participantes"""
        return Participante.objects.all()

    @staticmethod
    def get_by_id(participante_id: int) -> Optional[Participante]:
        """Obtener un participante por su ID"""
        try:
            return Participante.objects.get(pk=participante_id)
        except Participante.DoesNotExist:
            return None

    @staticmethod
    def get_by_email(email: str) -> Optional[Participante]:
        """Obtener un participante por su email"""
        try:
            return Participante.objects.get(email=email)
        except Participante.DoesNotExist:
            return None

    @staticmethod
    def create(nombre: str, apellido: str, email: str, telefono: str = None) -> Participante:
        """Crear un nuevo participante"""
        return Participante.objects.create(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono
        )

    @staticmethod
    def update(participante: Participante, nombre: str = None, apellido: str = None,
               email: str = None, telefono: str = None) -> Participante:
        """Actualizar un participante existente"""
        if nombre:
            participante.nombre = nombre
        if apellido:
            participante.apellido = apellido
        if email:
            participante.email = email
        if telefono is not None:
            participante.telefono = telefono
        participante.save()
        return participante

    @staticmethod
    def delete(participante_id: int) -> bool:
        """Eliminar un participante por su ID"""
        try:
            participante = Participante.objects.get(pk=participante_id)
            participante.delete()
            return True
        except Participante.DoesNotExist:
            return False


class EventoRepository:
    """Repositorio para operaciones de acceso a datos de Evento"""

    @staticmethod
    def get_all() -> QuerySet[Evento]:
        """Obtener todos los eventos"""
        return Evento.objects.select_related('deporte').prefetch_related('participantes').all()

    @staticmethod
    def get_by_id(evento_id: int) -> Optional[Evento]:
        """Obtener un evento por su ID"""
        try:
            return Evento.objects.select_related('deporte').prefetch_related('participantes').get(pk=evento_id)
        except Evento.DoesNotExist:
            return None

    @staticmethod
    def get_by_deporte(deporte_id: int) -> QuerySet[Evento]:
        """Obtener eventos filtrados por deporte"""
        return Evento.objects.filter(deporte_id=deporte_id).select_related('deporte')

    @staticmethod
    def get_futuros() -> QuerySet[Evento]:
        """Obtener eventos futuros"""
        from django.utils import timezone
        return Evento.objects.filter(fecha__gte=timezone.now()).select_related('deporte')

    @staticmethod
    def get_pasados() -> QuerySet[Evento]:
        """Obtener eventos pasados"""
        from django.utils import timezone
        return Evento.objects.filter(fecha__lt=timezone.now()).select_related('deporte')

    @staticmethod
    def create(nombre: str, deporte_id: int, fecha, lugar: str, descripcion: str = None) -> Evento:
        """Crear un nuevo evento"""
        return Evento.objects.create(
            nombre=nombre,
            deporte_id=deporte_id,
            fecha=fecha,
            lugar=lugar,
            descripcion=descripcion
        )

    @staticmethod
    def update(evento: Evento, nombre: str = None, deporte_id: int = None,
               fecha=None, lugar: str = None, descripcion: str = None) -> Evento:
        """Actualizar un evento existente"""
        if nombre:
            evento.nombre = nombre
        if deporte_id:
            evento.deporte_id = deporte_id
        if fecha:
            evento.fecha = fecha
        if lugar:
            evento.lugar = lugar
        if descripcion is not None:
            evento.descripcion = descripcion
        evento.save()
        return evento

    @staticmethod
    def delete(evento_id: int) -> bool:
        """Eliminar un evento por su ID"""
        try:
            evento = Evento.objects.get(pk=evento_id)
            evento.delete()
            return True
        except Evento.DoesNotExist:
            return False

    @staticmethod
    def agregar_participante(evento_id: int, participante_id: int, numero_inscripcion: str = None) -> EventoParticipante:
        """Agregar un participante a un evento"""
        evento = Evento.objects.get(pk=evento_id)
        participante = Participante.objects.get(pk=participante_id)
        return EventoParticipante.objects.create(
            evento=evento,
            participante=participante,
            numero_inscripcion=numero_inscripcion
        )

    @staticmethod
    def remover_participante(evento_id: int, participante_id: int) -> bool:
        """Remover un participante de un evento"""
        try:
            inscripcion = EventoParticipante.objects.get(evento_id=evento_id, participante_id=participante_id)
            inscripcion.delete()
            return True
        except EventoParticipante.DoesNotExist:
            return False


class EquipoRepository:
    """Repositorio para operaciones de acceso a datos de Equipo"""

    @staticmethod
    def get_all():
        """Obtener todos los equipos"""
        return Equipo.objects.select_related('deporte').all()

    @staticmethod
    def get_by_id(equipo_id: int):
        """Obtener un equipo por su ID"""
        try:
            return Equipo.objects.select_related('deporte').get(pk=equipo_id)
        except Equipo.DoesNotExist:
            return None

    @staticmethod
    def get_by_deporte(deporte_id: int):
        """Obtener equipos filtrados por deporte"""
        return Equipo.objects.filter(deporte_id=deporte_id).select_related('deporte')

    @staticmethod
    def create(nombre: str, deporte_id: int, ciudad: str, fecha_fundacion=None):
        """Crear un nuevo equipo"""
        return Equipo.objects.create(
            nombre=nombre,
            deporte_id=deporte_id,
            ciudad=ciudad,
            fecha_fundacion=fecha_fundacion
        )

    @staticmethod
    def update(equipo, nombre: str = None, deporte_id: int = None,
               ciudad: str = None, fecha_fundacion=None):
        """Actualizar un equipo existente"""
        if nombre:
            equipo.nombre = nombre
        if deporte_id:
            equipo.deporte_id = deporte_id
        if ciudad:
            equipo.ciudad = ciudad
        if fecha_fundacion is not None:
            equipo.fecha_fundacion = fecha_fundacion
        equipo.save()
        return equipo

    @staticmethod
    def delete(equipo_id: int) -> bool:
        """Eliminar un equipo por su ID"""
        try:
            equipo = Equipo.objects.get(pk=equipo_id)
            equipo.delete()
            return True
        except Equipo.DoesNotExist:
            return False