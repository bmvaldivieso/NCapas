from typing import Optional, List
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Deporte, Evento, Participante
from .repositories import DeporteRepository, EventoRepository, ParticipanteRepository, EquipoRepository


class DeporteService:
    """Servicio con lógica de negocio para Deporte"""

    @staticmethod
    def obtener_todos():
        """Obtener todos los deportes"""
        return DeporteRepository.get_all()

    @staticmethod
    def obtener_por_id(deporte_id: int) -> Optional[Deporte]:
        """Obtener un deporte por su ID"""
        return DeporteRepository.get_by_id(deporte_id)

    @staticmethod
    def crear(nombre: str, descripcion: str = None) -> Deporte:
        """Crear un nuevo deporte con validaciones de negocio"""
        # Validar que el nombre no esté vacío
        if not nombre or not nombre.strip():
            raise ValidationError("El nombre del deporte es obligatorio")

        # Validar que no exista un deporte con el mismo nombre
        nombre_limpio = nombre.strip()
        deporte_existente = DeporteRepository.get_by_nombre(nombre_limpio)
        if deporte_existente:
            raise ValidationError(f"Ya existe un deporte con el nombre '{nombre_limpio}'")

        return DeporteRepository.create(nombre=nombre_limpio, descripcion=descripcion)

    @staticmethod
    def actualizar(deporte_id: int, nombre: str = None, descripcion: str = None) -> Deporte:
        """Actualizar un deporte existente con validaciones"""
        deporte = DeporteRepository.get_by_id(deporte_id)
        if not deporte:
            raise ValidationError(f"No se encontró el deporte con ID {deporte_id}")

        # Validar nombre si se proporciona
        if nombre:
            nombre_limpio = nombre.strip()
            if not nombre_limpio:
                raise ValidationError("El nombre del deporte no puede estar vacío")

            # Validar que no exista otro deporte con el mismo nombre
            deporte_existente = DeporteRepository.get_by_nombre(nombre_limpio)
            if deporte_existente and deporte_existente.id != deporte_id:
                raise ValidationError(f"Ya existe otro deporte con el nombre '{nombre_limpio}'")
            nombre = nombre_limpio

        return DeporteRepository.update(deporte, nombre=nombre, descripcion=descripcion)

    @staticmethod
    def eliminar(deporte_id: int) -> bool:
        """Eliminar un deporte con validaciones de negocio"""
        deporte = DeporteRepository.get_by_id(deporte_id)
        if not deporte:
            raise ValidationError(f"No se encontró el deporte con ID {deporte_id}")

        # Validar que no tenga eventos asociados
        eventos = EventoRepository.get_by_deporte(deporte_id)
        if eventos.exists():
            raise ValidationError(
                f"No se puede eliminar el deporte '{deporte.nombre}' porque tiene eventos asociados"
            )

        return DeporteRepository.delete(deporte_id)


class ParticipanteService:
    """Servicio con lógica de negocio para Participante"""

    @staticmethod
    def obtener_todos():
        """Obtener todos los participantes"""
        return ParticipanteRepository.get_all()

    @staticmethod
    def obtener_por_id(participante_id: int) -> Optional[Participante]:
        """Obtener un participante por su ID"""
        return ParticipanteRepository.get_by_id(participante_id)

    @staticmethod
    def crear(nombre: str, apellido: str, email: str, telefono: str = None) -> Participante:
        """Crear un nuevo participante con validaciones de negocio"""
        # Validar campos obligatorios
        if not nombre or not nombre.strip():
            raise ValidationError("El nombre es obligatorio")
        if not apellido or not apellido.strip():
            raise ValidationError("El apellido es obligatorio")
        if not email or not email.strip():
            raise ValidationError("El email es obligatorio")

        # Validar formato de email
        email_limpio = email.strip().lower()
        if '@' not in email_limpio:
            raise ValidationError("El email no tiene un formato válido")

        # Validar que el email sea único
        participante_existente = ParticipanteRepository.get_by_email(email_limpio)
        if participante_existente:
            raise ValidationError(f"Ya existe un participante con el email '{email_limpio}'")

        return ParticipanteRepository.create(
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            email=email_limpio,
            telefono=telefono.strip() if telefono else None
        )

    @staticmethod
    def actualizar(participante_id: int, nombre: str = None, apellido: str = None,
                   email: str = None, telefono: str = None) -> Participante:
        """Actualizar un participante existente con validaciones"""
        participante = ParticipanteRepository.get_by_id(participante_id)
        if not participante:
            raise ValidationError(f"No se encontró el participante con ID {participante_id}")

        # Validar nombre si se proporciona
        if nombre:
            nombre_limpio = nombre.strip()
            if not nombre_limpio:
                raise ValidationError("El nombre no puede estar vacío")
            nombre = nombre_limpio

        # Validar apellido si se proporciona
        if apellido:
            apellido_limpio = apellido.strip()
            if not apellido_limpio:
                raise ValidationError("El apellido no puede estar vacío")
            apellido = apellido_limpio

        # Validar email si se proporciona
        if email:
            email_limpio = email.strip().lower()
            if not email_limpio:
                raise ValidationError("El email no puede estar vacío")
            if '@' not in email_limpio:
                raise ValidationError("El email no tiene un formato válido")

            # Validar que el email sea único
            participante_existente = ParticipanteRepository.get_by_email(email_limpio)
            if participante_existente and participante_existente.id != participante_id:
                raise ValidationError(f"Ya existe otro participante con el email '{email_limpio}'")
            email = email_limpio

        return ParticipanteRepository.update(
            participante,
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono.strip() if telefono else None
        )

    @staticmethod
    def eliminar(participante_id: int) -> bool:
        """Eliminar un participante con validaciones de negocio"""
        participante = ParticipanteRepository.get_by_id(participante_id)
        if not participante:
            raise ValidationError(f"No se encontró el participante con ID {participante_id}")

        return ParticipanteRepository.delete(participante_id)


class EventoService:
    """Servicio con lógica de negocio para Evento"""

    @staticmethod
    def obtener_todos():
        """Obtener todos los eventos"""
        return EventoRepository.get_all()

    @staticmethod
    def obtener_por_id(evento_id: int) -> Optional[Evento]:
        """Obtener un evento por su ID"""
        return EventoRepository.get_by_id(evento_id)

    @staticmethod
    def obtener_futuros():
        """Obtener eventos futuros"""
        return EventoRepository.get_futuros()

    @staticmethod
    def obtener_pasados():
        """Obtener eventos pasados"""
        return EventoRepository.get_pasados()

    @staticmethod
    def obtener_por_deporte(deporte_id: int):
        """Obtener eventos filtrados por deporte"""
        return EventoRepository.get_by_deporte(deporte_id)

    @staticmethod
    def crear(nombre: str, deporte_id: int, fecha, lugar: str, descripcion: str = None) -> Evento:
        """Crear un nuevo evento con validaciones de negocio"""
        # Validar campos obligatorios
        if not nombre or not nombre.strip():
            raise ValidationError("El nombre del evento es obligatorio")
        if not lugar or not lugar.strip():
            raise ValidationError("El lugar del evento es obligatorio")

        # Validar que el deporte exista
        deporte = DeporteRepository.get_by_id(deporte_id)
        if not deporte:
            raise ValidationError(f"No se encontró el deporte con ID {deporte_id}")

        # Validar que la fecha no sea en el pasado (regla de negocio)
        if fecha and fecha < timezone.now():
            raise ValidationError("No se pueden crear eventos en el pasado")

        return EventoRepository.create(
            nombre=nombre.strip(),
            deporte_id=deporte_id,
            fecha=fecha,
            lugar=lugar.strip(),
            descripcion=descripcion
        )

    @staticmethod
    def actualizar(evento_id: int, nombre: str = None, deporte_id: int = None,
                   fecha=None, lugar: str = None, descripcion: str = None) -> Evento:
        """Actualizar un evento existente con validaciones"""
        evento = EventoRepository.get_by_id(evento_id)
        if not evento:
            raise ValidationError(f"No se encontró el evento con ID {evento_id}")

        # Validar nombre si se proporciona
        if nombre:
            nombre_limpio = nombre.strip()
            if not nombre_limpio:
                raise ValidationError("El nombre del evento no puede estar vacío")
            nombre = nombre_limpio

        # Validar lugar si se proporciona
        if lugar:
            lugar_limpio = lugar.strip()
            if not lugar_limpio:
                raise ValidationError("El lugar del evento no puede estar vacío")
            lugar = lugar_limpio

        # Validar deporte si se proporciona
        if deporte_id:
            deporte = DeporteRepository.get_by_id(deporte_id)
            if not deporte:
                raise ValidationError(f"No se encontró el deporte con ID {deporte_id}")

        # Validar fecha si se proporciona
        if fecha and fecha < timezone.now():
            raise ValidationError("No se puede cambiar la fecha del evento al pasado")

        return EventoRepository.update(
            evento,
            nombre=nombre,
            deporte_id=deporte_id,
            fecha=fecha,
            lugar=lugar,
            descripcion=descripcion
        )

    @staticmethod
    def eliminar(evento_id: int) -> bool:
        """Eliminar un evento con validaciones de negocio"""
        evento = EventoRepository.get_by_id(evento_id)
        if not evento:
            raise ValidationError(f"No se encontró el evento con ID {evento_id}")

        return EventoRepository.delete(evento_id)

    @staticmethod
    def inscribir_participante(evento_id: int, participante_id: int, numero_inscripcion: str = None) -> bool:
        """Inscribir un participante a un evento con validaciones"""
        evento = EventoRepository.get_by_id(evento_id)
        if not evento:
            raise ValidationError(f"No se encontró el evento con ID {evento_id}")

        participante = ParticipanteRepository.get_by_id(participante_id)
        if not participante:
            raise ValidationError(f"No se encontró el participante con ID {participante_id}")

        # Validar que el participante no esté ya inscrito
        if evento.participantes.filter(pk=participante_id).exists():
            raise ValidationError(
                f"El participante '{participante.nombre_completo}' ya está inscrito en este evento"
            )

        # Validar que el evento no haya pasado
        if evento.fecha < timezone.now():
            raise ValidationError("No se pueden inscribir participantes a eventos pasados")

        EventoRepository.agregar_participante(evento_id, participante_id, numero_inscripcion)
        return True

    @staticmethod
    def desinscribir_participante(evento_id: int, participante_id: int) -> bool:
        """Desinscribir un participante de un evento"""
        evento = EventoRepository.get_by_id(evento_id)
        if not evento:
            raise ValidationError(f"No se encontró el evento con ID {evento_id}")

        participante = ParticipanteRepository.get_by_id(participante_id)
        if not participante:
            raise ValidationError(f"No se encontró el participante con ID {participante_id}")

        return EventoRepository.remover_participante(evento_id, participante_id)



class EquipoService:
    """Servicio con lógica de negocio para Equipo"""

    @staticmethod
    def obtener_todos():
        """Obtener todos los equipos"""
        return EquipoRepository.get_all()

    @staticmethod
    def obtener_por_id(equipo_id: int):
        """Obtener un equipo por su ID"""
        return EquipoRepository.get_by_id(equipo_id)

    @staticmethod
    def obtener_por_deporte(deporte_id: int):
        """Obtener equipos filtrados por deporte"""
        return EquipoRepository.get_by_deporte(deporte_id)

    @staticmethod
    def crear(nombre: str, deporte_id: int, ciudad: str, fecha_fundacion=None):
        """Crear un nuevo equipo con validaciones de negocio"""
        # Validar campos obligatorios
        if not nombre or not nombre.strip():
            raise ValidationError("El nombre del equipo es obligatorio")
        if not ciudad or not ciudad.strip():
            raise ValidationError("La ciudad del equipo es obligatoria")

        # Validar que el deporte exista
        deporte = DeporteRepository.get_by_id(deporte_id)
        if not deporte:
            raise ValidationError(f"No se encontró el deporte con ID {deporte_id}")

        # Validar que no exista un equipo con el mismo nombre
        equipos = EquipoRepository.get_all()
        if equipos.filter(nombre=nombre.strip()).exists():
            raise ValidationError(f"Ya existe un equipo con el nombre '{nombre.strip()}'")

        return EquipoRepository.create(
            nombre=nombre.strip(),
            deporte_id=deporte_id,
            ciudad=ciudad.strip(),
            fecha_fundacion=fecha_fundacion
        )

    @staticmethod
    def actualizar(equipo_id: int, nombre: str = None, deporte_id: int = None,
                   ciudad: str = None, fecha_fundacion=None):
        """Actualizar un equipo existente con validaciones"""
        equipo = EquipoRepository.get_by_id(equipo_id)
        if not equipo:
            raise ValidationError(f"No se encontró el equipo con ID {equipo_id}")

        # Validar nombre si se proporciona
        if nombre:
            nombre_limpio = nombre.strip()
            if not nombre_limpio:
                raise ValidationError("El nombre del equipo no puede estar vacío")
            nombre = nombre_limpio

        # Validar ciudad si se proporciona
        if ciudad:
            ciudad_limpio = ciudad.strip()
            if not ciudad_limpio:
                raise ValidationError("La ciudad del equipo no puede estar vacía")
            ciudad = ciudad_limpio

        # Validar deporte si se proporciona
        if deporte_id:
            deporte = DeporteRepository.get_by_id(deporte_id)
            if not deporte:
                raise ValidationError(f"No se encontró el deporte con ID {deporte_id}")

        return EquipoRepository.update(
            equipo,
            nombre=nombre,
            deporte_id=deporte_id,
            ciudad=ciudad,
            fecha_fundacion=fecha_fundacion
        )

    @staticmethod
    def eliminar(equipo_id: int) -> bool:
        """Eliminar un equipo con validaciones de negocio"""
        equipo = EquipoRepository.get_by_id(equipo_id)
        if not equipo:
            raise ValidationError(f"No se encontró el equipo con ID {equipo_id}")

        # Aquí puedes agregar validaciones adicionales
        # Por ejemplo: no permitir eliminar equipos con eventos asociados

        return EquipoRepository.delete(equipo_id)