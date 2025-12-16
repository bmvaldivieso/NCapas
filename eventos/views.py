from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from .models import Deporte, Evento, Participante, Equipo
from .forms import DeporteForm, EventoForm, ParticipanteForm
from .services import DeporteService, EventoService, ParticipanteService


# ==================== VISTAS PARA DEPORTES ====================

class DeporteListView(ListView):
    """Vista para listar todos los deportes"""
    model = Deporte
    template_name = 'eventos/lista_deportes.html'
    context_object_name = 'deportes'

    def get_queryset(self):
        return DeporteService.obtener_todos()


class DeporteCreateView(CreateView):
    """Vista para crear un nuevo deporte"""
    model = Deporte
    form_class = DeporteForm
    template_name = 'eventos/crear_deporte.html'
    success_url = reverse_lazy('eventos:lista_deportes')

    def form_valid(self, form):
        try:
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data.get('descripcion', '')
            DeporteService.crear(nombre=nombre, descripcion=descripcion)
            messages.success(self.request, f'Deporte "{nombre}" creado exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class DeporteDetailView(DetailView):
    """Vista para ver los detalles de un deporte"""
    model = Deporte
    template_name = 'eventos/detalle_deporte.html'
    context_object_name = 'deporte'

    def get_object(self):
        deporte_id = self.kwargs.get('pk')
        deporte = DeporteService.obtener_por_id(deporte_id)
        if not deporte:
            messages.error(self.request, 'Deporte no encontrado.')
            return None
        return deporte

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['eventos'] = EventoService.obtener_por_deporte(self.object.id)
        return context


class DeporteUpdateView(UpdateView):
    """Vista para actualizar un deporte"""
    model = Deporte
    form_class = DeporteForm
    template_name = 'eventos/crear_deporte.html'
    success_url = reverse_lazy('eventos:lista_deportes')

    def form_valid(self, form):
        try:
            deporte_id = self.kwargs.get('pk')
            nombre = form.cleaned_data.get('nombre')
            descripcion = form.cleaned_data.get('descripcion')
            DeporteService.actualizar(deporte_id, nombre=nombre, descripcion=descripcion)
            messages.success(self.request, 'Deporte actualizado exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class DeporteDeleteView(DeleteView):
    """Vista para eliminar un deporte"""
    model = Deporte
    template_name = 'eventos/eliminar_deporte.html'
    success_url = reverse_lazy('eventos:lista_deportes')

    def delete(self, request, *args, **kwargs):
        try:
            deporte_id = self.kwargs.get('pk')
            DeporteService.eliminar(deporte_id)
            messages.success(self.request, 'Deporte eliminado exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return redirect(self.success_url)


# ==================== VISTAS PARA PARTICIPANTES ====================

class ParticipanteListView(ListView):
    """Vista para listar todos los participantes"""
    model = Participante
    template_name = 'eventos/lista_participantes.html'
    context_object_name = 'participantes'

    def get_queryset(self):
        return ParticipanteService.obtener_todos()


class ParticipanteCreateView(CreateView):
    """Vista para crear un nuevo participante"""
    model = Participante
    form_class = ParticipanteForm
    template_name = 'eventos/crear_participante.html'
    success_url = reverse_lazy('eventos:lista_participantes')

    def form_valid(self, form):
        try:
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            email = form.cleaned_data['email']
            telefono = form.cleaned_data.get('telefono', '')
            ParticipanteService.crear(
                nombre=nombre,
                apellido=apellido,
                email=email,
                telefono=telefono
            )
            messages.success(self.request, f'Participante "{nombre} {apellido}" creado exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class ParticipanteDetailView(DetailView):
    """Vista para ver los detalles de un participante"""
    model = Participante
    template_name = 'eventos/detalle_participante.html'
    context_object_name = 'participante'

    def get_object(self):
        participante_id = self.kwargs.get('pk')
        participante = ParticipanteService.obtener_por_id(participante_id)
        if not participante:
            messages.error(self.request, 'Participante no encontrado.')
            return None
        return participante

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['eventos'] = self.object.eventos.all()
        return context


class ParticipanteUpdateView(UpdateView):
    """Vista para actualizar un participante"""
    model = Participante
    form_class = ParticipanteForm
    template_name = 'eventos/crear_participante.html'
    success_url = reverse_lazy('eventos:lista_participantes')

    def form_valid(self, form):
        try:
            participante_id = self.kwargs.get('pk')
            nombre = form.cleaned_data.get('nombre')
            apellido = form.cleaned_data.get('apellido')
            email = form.cleaned_data.get('email')
            telefono = form.cleaned_data.get('telefono')
            ParticipanteService.actualizar(
                participante_id,
                nombre=nombre,
                apellido=apellido,
                email=email,
                telefono=telefono
            )
            messages.success(self.request, 'Participante actualizado exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class ParticipanteDeleteView(DeleteView):
    """Vista para eliminar un participante"""
    model = Participante
    template_name = 'eventos/eliminar_participante.html'
    success_url = reverse_lazy('eventos:lista_participantes')

    def delete(self, request, *args, **kwargs):
        try:
            participante_id = self.kwargs.get('pk')
            ParticipanteService.eliminar(participante_id)
            messages.success(self.request, 'Participante eliminado exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return redirect(self.success_url)


# ==================== VISTAS PARA EVENTOS ====================

class EventoListView(ListView):
    """Vista para listar todos los eventos"""
    model = Evento
    template_name = 'eventos/lista_eventos.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        return EventoService.obtener_todos()


class EventoCreateView(CreateView):
    """Vista para crear un nuevo evento"""
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/crear_evento.html'
    success_url = reverse_lazy('eventos:lista_eventos')

    def form_valid(self, form):
        try:
            nombre = form.cleaned_data['nombre']
            deporte_id = form.cleaned_data['deporte'].id
            fecha = form.cleaned_data['fecha']
            lugar = form.cleaned_data['lugar']
            descripcion = form.cleaned_data.get('descripcion', '')
            EventoService.crear(
                nombre=nombre,
                deporte_id=deporte_id,
                fecha=fecha,
                lugar=lugar,
                descripcion=descripcion
            )
            messages.success(self.request, f'Evento "{nombre}" creado exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class EventoDetailView(DetailView):
    """Vista para ver los detalles de un evento"""
    model = Evento
    template_name = 'eventos/detalle_evento.html'
    context_object_name = 'evento'

    def get_object(self):
        evento_id = self.kwargs.get('pk')
        evento = EventoService.obtener_por_id(evento_id)
        if not evento:
            messages.error(self.request, 'Evento no encontrado.')
            return None
        return evento

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['participantes'] = self.object.participantes.all()
            context['todos_participantes'] = ParticipanteService.obtener_todos()
        return context


class EventoUpdateView(UpdateView):
    """Vista para actualizar un evento"""
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/crear_evento.html'
    success_url = reverse_lazy('eventos:lista_eventos')

    def form_valid(self, form):
        try:
            evento_id = self.kwargs.get('pk')
            nombre = form.cleaned_data.get('nombre')
            deporte_id = form.cleaned_data.get('deporte').id if form.cleaned_data.get('deporte') else None
            fecha = form.cleaned_data.get('fecha')
            lugar = form.cleaned_data.get('lugar')
            descripcion = form.cleaned_data.get('descripcion')
            EventoService.actualizar(
                evento_id,
                nombre=nombre,
                deporte_id=deporte_id,
                fecha=fecha,
                lugar=lugar,
                descripcion=descripcion
            )
            messages.success(self.request, 'Evento actualizado exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class EventoDeleteView(DeleteView):
    """Vista para eliminar un evento"""
    model = Evento
    template_name = 'eventos/eliminar_evento.html'
    success_url = reverse_lazy('eventos:lista_eventos')

    def delete(self, request, *args, **kwargs):
        try:
            evento_id = self.kwargs.get('pk')
            EventoService.eliminar(evento_id)
            messages.success(self.request, 'Evento eliminado exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return redirect(self.success_url)


# ==================== VISTA PRINCIPAL ====================

def home(request):
    """Vista principal del sistema"""
    context = {
        'total_deportes': DeporteService.obtener_todos().count(),
        'total_eventos': EventoService.obtener_todos().count(),
        'total_participantes': ParticipanteService.obtener_todos().count(),
        'eventos_futuros': EventoService.obtener_futuros()[:5],
    }
    return render(request, 'eventos/home.html', context)








from .services import DeporteService, EventoService, ParticipanteService, EquipoService
from .forms import DeporteForm, EventoForm, ParticipanteForm, EquipoForm

# Agregar al final del archivo

class EquipoListView(ListView):
    """Vista para listar todos los equipos"""
    model = Equipo
    template_name = 'eventos/lista_equipos.html'
    context_object_name = 'equipos'

    def get_queryset(self):
        return EquipoService.obtener_todos()


class EquipoCreateView(CreateView):
    """Vista para crear un nuevo equipo"""
    model = Equipo
    form_class = EquipoForm
    template_name = 'eventos/crear_equipo.html'
    success_url = reverse_lazy('eventos:lista_equipos')

    def form_valid(self, form):
        try:
            nombre = form.cleaned_data['nombre']
            deporte_id = form.cleaned_data['deporte'].id
            ciudad = form.cleaned_data['ciudad']
            fecha_fundacion = form.cleaned_data.get('fecha_fundacion')
            
            EquipoService.crear(
                nombre=nombre,
                deporte_id=deporte_id,
                ciudad=ciudad,
                fecha_fundacion=fecha_fundacion
            )
            messages.success(self.request, f'Equipo "{nombre}" creado exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class EquipoDetailView(DetailView):
    """Vista para ver los detalles de un equipo"""
    model = Equipo
    template_name = 'eventos/detalle_equipo.html'
    context_object_name = 'equipo'

    def get_object(self):
        equipo_id = self.kwargs.get('pk')
        equipo = EquipoService.obtener_por_id(equipo_id)
        if not equipo:
            messages.error(self.request, 'Equipo no encontrado.')
            return None
        return equipo


class EquipoUpdateView(UpdateView):
    """Vista para actualizar un equipo"""
    model = Equipo
    form_class = EquipoForm
    template_name = 'eventos/crear_equipo.html'
    success_url = reverse_lazy('eventos:lista_equipos')

    def form_valid(self, form):
        try:
            equipo_id = self.kwargs.get('pk')
            nombre = form.cleaned_data.get('nombre')
            deporte_id = form.cleaned_data.get('deporte').id if form.cleaned_data.get('deporte') else None
            ciudad = form.cleaned_data.get('ciudad')
            fecha_fundacion = form.cleaned_data.get('fecha_fundacion')
            
            EquipoService.actualizar(
                equipo_id,
                nombre=nombre,
                deporte_id=deporte_id,
                ciudad=ciudad,
                fecha_fundacion=fecha_fundacion
            )
            messages.success(self.request, 'Equipo actualizado exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class EquipoDeleteView(DeleteView):
    """Vista para eliminar un equipo"""
    model = Equipo
    template_name = 'eventos/eliminar_equipo.html'
    success_url = reverse_lazy('eventos:lista_equipos')

    def delete(self, request, *args, **kwargs):
        try:
            equipo_id = self.kwargs.get('pk')
            EquipoService.eliminar(equipo_id)
            messages.success(self.request, 'Equipo eliminado exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return redirect(self.success_url)