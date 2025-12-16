from django.urls import path
from . import views

app_name = 'eventos'

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Deportes
    path('deportes/', views.DeporteListView.as_view(), name='lista_deportes'),
    path('deportes/crear/', views.DeporteCreateView.as_view(), name='crear_deporte'),
    path('deportes/<int:pk>/', views.DeporteDetailView.as_view(), name='detalle_deporte'),
    path('deportes/<int:pk>/editar/', views.DeporteUpdateView.as_view(), name='editar_deporte'),
    path('deportes/<int:pk>/eliminar/', views.DeporteDeleteView.as_view(), name='eliminar_deporte'),

    # Participantes
    path('participantes/', views.ParticipanteListView.as_view(), name='lista_participantes'),
    path('participantes/crear/', views.ParticipanteCreateView.as_view(), name='crear_participante'),
    path('participantes/<int:pk>/', views.ParticipanteDetailView.as_view(), name='detalle_participante'),
    path('participantes/<int:pk>/editar/', views.ParticipanteUpdateView.as_view(), name='editar_participante'),
    path('participantes/<int:pk>/eliminar/', views.ParticipanteDeleteView.as_view(), name='eliminar_participante'),

    # Eventos
    path('eventos/', views.EventoListView.as_view(), name='lista_eventos'),
    path('eventos/crear/', views.EventoCreateView.as_view(), name='crear_evento'),
    path('eventos/<int:pk>/', views.EventoDetailView.as_view(), name='detalle_evento'),
    path('eventos/<int:pk>/editar/', views.EventoUpdateView.as_view(), name='editar_evento'),
    path('eventos/<int:pk>/eliminar/', views.EventoDeleteView.as_view(), name='eliminar_evento'),

    # Equipos
    path('equipos/', views.EquipoListView.as_view(), name='lista_equipos'),
    path('equipos/crear/', views.EquipoCreateView.as_view(), name='crear_equipo'),
    path('equipos/<int:pk>/', views.EquipoDetailView.as_view(), name='detalle_equipo'),
    path('equipos/<int:pk>/editar/', views.EquipoUpdateView.as_view(), name='editar_equipo'),
    path('equipos/<int:pk>/eliminar/', views.EquipoDeleteView.as_view(), name='eliminar_equipo'),
]

