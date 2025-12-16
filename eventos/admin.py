from django.contrib import admin
from .models import Deporte, Evento, Participante, EventoParticipante


@admin.register(Deporte)
class DeporteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)


@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'email', 'telefono', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('nombre', 'apellido', 'email')
    ordering = ('apellido', 'nombre')


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'deporte', 'fecha', 'lugar', 'fecha_creacion')
    list_filter = ('deporte', 'fecha', 'fecha_creacion')
    search_fields = ('nombre', 'lugar', 'descripcion')
    ordering = ('-fecha',)
    filter_horizontal = ('participantes',)
    date_hierarchy = 'fecha'


@admin.register(EventoParticipante)
class EventoParticipanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'evento', 'participante', 'fecha_inscripcion', 'numero_inscripcion')
    list_filter = ('fecha_inscripcion', 'evento')
    search_fields = ('evento__nombre', 'participante__nombre', 'participante__apellido', 'numero_inscripcion')
    ordering = ('-fecha_inscripcion',)




from .models import Deporte, Evento, Participante, Equipo

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'deporte', 'ciudad', 'fecha_fundacion', 'fecha_creacion')
    list_filter = ('deporte', 'ciudad', 'fecha_creacion')
    search_fields = ('nombre', 'ciudad')
    ordering = ('nombre',)    
