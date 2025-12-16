# Guía del Estudiante - Sistema de Eventos Deportivos

## Índice

1. [Introducción](#introducción)
2. [¿Cómo Funciona el Proyecto?](#cómo-funciona-el-proyecto)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Flujo de una Petición](#flujo-de-una-petición)
5. [Cómo Agregar un Nuevo Componente](#cómo-agregar-un-nuevo-componente)
6. [Ejemplo Práctico: Agregar "Equipo"](#ejemplo-práctico-agregar-equipo)
7. [Despliegue en Docker](#despliegue-en-docker)
8. [Comandos Útiles](#comandos-útiles)
9. [Solución de Problemas](#solución-de-problemas)

---

## Introducción

Esta guía te ayudará a entender cómo funciona el Sistema de Eventos Deportivos y cómo puedes extenderlo agregando nuevos componentes siguiendo la arquitectura en 3 capas.

### Requisitos Previos

- Conocimientos básicos de Python
- Conocimientos básicos de Django
- Conocimientos básicos de HTML/CSS
- Conocimientos básicos de Docker (opcional, pero recomendado)

---

## ¿Cómo Funciona el Proyecto?

### Arquitectura en 3 Capas

El proyecto sigue una arquitectura en 3 capas que separa las responsabilidades:

```
┌─────────────────────────────────────┐
│   CAPA DE PRESENTACIÓN              │
│   - Recibe peticiones HTTP          │
│   - Muestra información al usuario  │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   CAPA DE LÓGICA DE NEGOCIO         │
│   - Aplica reglas de negocio        │
│   - Valida operaciones               │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   CAPA DE ACCESO A DATOS            │
│   - Guarda y recupera datos         │
│   - Interactúa con la base de datos │
└─────────────────────────────────────┘
```

### Componentes Principales

1. **Models** (`models.py`): Define la estructura de datos
2. **Repositories** (`repositories.py`): Accede a la base de datos
3. **Services** (`services.py`): Contiene la lógica de negocio
4. **Views** (`views.py`): Maneja las peticiones HTTP
5. **Forms** (`forms.py`): Valida datos de entrada
6. **Templates** (`templates/`): Muestra la interfaz al usuario

---

## Estructura del Proyecto

```
arquitecturaCapas/
├── manage.py                    # Script de administración de Django
├── requirements.txt             # Dependencias del proyecto
├── README.md                    # Documentación principal
├── Arquitectura.md              # Documentación de arquitectura
├── GuiaEstudiante.md           # Esta guía
├── Dockerfile                   # Configuración de Docker
├── docker-compose.yml           # Orquestación de contenedores
├── eventos_deportivos/          # Configuración del proyecto Django
│   ├── settings.py              # Configuración del proyecto
│   ├── urls.py                  # URLs principales
│   └── wsgi.py                  # Configuración WSGI
├── eventos/                     # Aplicación principal
│   ├── models.py                # Capa de Datos - Modelos
│   ├── repositories.py           # Capa de Datos - Repositorios
│   ├── services.py              # Capa de Negocio - Servicios
│   ├── views.py                 # Capa de Presentación - Controladores
│   ├── forms.py                 # Capa de Presentación - Formularios
│   ├── urls.py                  # URLs de la aplicación
│   ├── admin.py                 # Configuración del admin
│   └── templates/               # Capa de Presentación - Vistas HTML
│       └── eventos/
│           ├── base.html
│           ├── home.html
│           └── ...
└── static/                      # Archivos estáticos (CSS, JS, imágenes)
    └── css/
        └── style.css
```

---

## Flujo de una Petición

Cuando un usuario realiza una acción (por ejemplo, crear un evento), esto es lo que sucede:

### Ejemplo: Crear un Evento

```
1. Usuario hace clic en "Crear Evento"
   ↓
2. Navegador envía petición HTTP POST a /eventos/crear/
   ↓
3. Django URL Router encuentra la ruta en urls.py
   ↓
4. EventoCreateView (Controller) recibe la petición
   ↓
5. EventoForm valida el formato de los datos
   ↓
6. EventoService.crear() aplica reglas de negocio:
   - Valida que la fecha no sea en el pasado
   - Valida que el deporte exista
   ↓
7. EventoRepository.create() guarda en la base de datos
   ↓
8. Model.save() ejecuta INSERT en SQLite
   ↓
9. Controller muestra mensaje de éxito
   ↓
10. Template renderiza la lista de eventos actualizada
    ↓
11. Usuario ve el nuevo evento en la lista
```

### Código del Flujo

**1. URL Routing** (`eventos/urls.py`):
```python
path('eventos/crear/', views.EventoCreateView.as_view(), name='crear_evento'),
```

**2. Controller** (`eventos/views.py`):
```python
class EventoCreateView(CreateView):
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
            
            # Llama al servicio (Capa de Negocio)
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
```

**3. Service** (`eventos/services.py`):
```python
@staticmethod
def crear(nombre: str, deporte_id: int, fecha, lugar: str, descripcion: str = None) -> Evento:
    # Validaciones de negocio
    if not nombre or not nombre.strip():
        raise ValidationError("El nombre del evento es obligatorio")
    
    # Validar que el deporte exista
    deporte = DeporteRepository.get_by_id(deporte_id)
    if not deporte:
        raise ValidationError(f"No se encontró el deporte con ID {deporte_id}")
    
    # Validar que la fecha no sea en el pasado
    if fecha and fecha < timezone.now():
        raise ValidationError("No se pueden crear eventos en el pasado")
    
    # Llama al repositorio (Capa de Datos)
    return EventoRepository.create(
        nombre=nombre.strip(),
        deporte_id=deporte_id,
        fecha=fecha,
        lugar=lugar.strip(),
        descripcion=descripcion
    )
```

**4. Repository** (`eventos/repositories.py`):
```python
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
```

**5. Model** (`eventos/models.py`):
```python
class Evento(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    fecha = models.DateTimeField(verbose_name="Fecha del Evento")
    lugar = models.CharField(max_length=200, verbose_name="Lugar")
    descripcion = models.TextField(blank=True, null=True)
    # ...
```

---

## Cómo Agregar un Nuevo Componente

Para agregar un nuevo componente (por ejemplo, "Equipo"), debes seguir estos pasos en orden:

### Paso 1: Crear el Model (Capa de Datos)

**Archivo**: `eventos/models.py`

```python
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
```

**Después de crear el modelo, ejecuta**:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Paso 2: Crear el Repository (Capa de Datos)

**Archivo**: `eventos/repositories.py`

```python
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
```

**No olvides importar el modelo al inicio del archivo**:
```python
from .models import Deporte, Evento, Participante, Equipo
```

### Paso 3: Crear el Service (Capa de Negocio)

**Archivo**: `eventos/services.py`

```python
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
```

**No olvides importar al inicio del archivo**:
```python
from .repositories import DeporteRepository, EventoRepository, ParticipanteRepository, EquipoRepository
```

### Paso 4: Crear el Form (Capa de Presentación)

**Archivo**: `eventos/forms.py`

```python
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
```

**No olvides importar el modelo**:
```python
from .models import Deporte, Evento, Participante, Equipo
```

### Paso 5: Crear las Views (Capa de Presentación)

**Archivo**: `eventos/views.py`

```python
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
```

**No olvides importar el modelo**:
```python
from .models import Deporte, Evento, Participante, Equipo
```

### Paso 6: Crear las URLs

**Archivo**: `eventos/urls.py`

```python
# Agregar estas rutas al urlpatterns

path('equipos/', views.EquipoListView.as_view(), name='lista_equipos'),
path('equipos/crear/', views.EquipoCreateView.as_view(), name='crear_equipo'),
path('equipos/<int:pk>/', views.EquipoDetailView.as_view(), name='detalle_equipo'),
path('equipos/<int:pk>/editar/', views.EquipoUpdateView.as_view(), name='editar_equipo'),
path('equipos/<int:pk>/eliminar/', views.EquipoDeleteView.as_view(), name='eliminar_equipo'),
```

### Paso 7: Crear los Templates

**Archivo**: `eventos/templates/eventos/lista_equipos.html`

```html
{% extends 'eventos/base.html' %}

{% block title %}Equipos - Sistema de Eventos Deportivos{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1>Lista de Equipos</h1>
    <a href="{% url 'eventos:crear_equipo' %}" class="btn btn-primary">Crear Equipo</a>
</div>

{% if equipos %}
<div class="table-responsive">
    <table class="table table-striped table-hover">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Deporte</th>
                <th>Ciudad</th>
                <th>Fecha de Fundación</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            {% for equipo in equipos %}
            <tr>
                <td>{{ equipo.id }}</td>
                <td><strong>{{ equipo.nombre }}</strong></td>
                <td>{{ equipo.deporte.nombre }}</td>
                <td>{{ equipo.ciudad }}</td>
                <td>{{ equipo.fecha_fundacion|date:"d/m/Y"|default:"-" }}</td>
                <td>
                    <a href="{% url 'eventos:detalle_equipo' equipo.pk %}" class="btn btn-sm btn-info">Ver</a>
                    <a href="{% url 'eventos:editar_equipo' equipo.pk %}" class="btn btn-sm btn-warning">Editar</a>
                    <a href="{% url 'eventos:eliminar_equipo' equipo.pk %}" class="btn btn-sm btn-danger">Eliminar</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% else %}
<div class="alert alert-info">
    No hay equipos registrados. <a href="{% url 'eventos:crear_equipo' %}">Crear el primero</a>
</div>
{% endif %}
{% endblock %}
```

**Archivo**: `eventos/templates/eventos/crear_equipo.html`

```html
{% extends 'eventos/base.html' %}

{% block title %}{% if object %}Editar{% else %}Crear{% endif %} Equipo - Sistema de Eventos Deportivos{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8 mx-auto">
        <h1>{% if object %}Editar Equipo{% else %}Crear Nuevo Equipo{% endif %}</h1>
        <form method="post" class="mt-4">
            {% csrf_token %}
            <div class="mb-3">
                <label for="{{ form.nombre.id_for_label }}" class="form-label">{{ form.nombre.label }}</label>
                {{ form.nombre }}
                {% if form.nombre.errors %}
                    <div class="text-danger">{{ form.nombre.errors }}</div>
                {% endif %}
            </div>
            <div class="mb-3">
                <label for="{{ form.deporte.id_for_label }}" class="form-label">{{ form.deporte.label }}</label>
                {{ form.deporte }}
                {% if form.deporte.errors %}
                    <div class="text-danger">{{ form.deporte.errors }}</div>
                {% endif %}
            </div>
            <div class="mb-3">
                <label for="{{ form.ciudad.id_for_label }}" class="form-label">{{ form.ciudad.label }}</label>
                {{ form.ciudad }}
                {% if form.ciudad.errors %}
                    <div class="text-danger">{{ form.ciudad.errors }}</div>
                {% endif %}
            </div>
            <div class="mb-3">
                <label for="{{ form.fecha_fundacion.id_for_label }}" class="form-label">{{ form.fecha_fundacion.label }}</label>
                {{ form.fecha_fundacion }}
                {% if form.fecha_fundacion.errors %}
                    <div class="text-danger">{{ form.fecha_fundacion.errors }}</div>
                {% endif %}
            </div>
            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                <a href="{% url 'eventos:lista_equipos' %}" class="btn btn-secondary">Cancelar</a>
                <button type="submit" class="btn btn-primary">{% if object %}Actualizar{% else %}Crear{% endif %}</button>
            </div>
        </form>
    </div>
</div>
{% endblock %}
```

**Archivo**: `eventos/templates/eventos/detalle_equipo.html`

```html
{% extends 'eventos/base.html' %}

{% block title %}Detalle de Equipo - Sistema de Eventos Deportivos{% endblock %}

{% block content %}
{% if equipo %}
<div class="row">
    <div class="col-md-8">
        <h1>{{ equipo.nombre }}</h1>
        <div class="card mt-4">
            <div class="card-body">
                <h5 class="card-title">Información del Equipo</h5>
                <p><strong>Deporte:</strong> {{ equipo.deporte.nombre }}</p>
                <p><strong>Ciudad:</strong> {{ equipo.ciudad }}</p>
                <p><strong>Fecha de Fundación:</strong> {{ equipo.fecha_fundacion|date:"d/m/Y"|default:"No registrada" }}</p>
                <p><strong>Fecha de Creación:</strong> {{ equipo.fecha_creacion|date:"d/m/Y H:i" }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Acciones</h5>
                <a href="{% url 'eventos:editar_equipo' equipo.pk %}" class="btn btn-warning w-100 mb-2">Editar</a>
                <a href="{% url 'eventos:eliminar_equipo' equipo.pk %}" class="btn btn-danger w-100 mb-2">Eliminar</a>
                <a href="{% url 'eventos:lista_equipos' %}" class="btn btn-secondary w-100">Volver a Lista</a>
            </div>
        </div>
    </div>
</div>
{% else %}
<div class="alert alert-warning">
    Equipo no encontrado.
</div>
{% endif %}
{% endblock %}
```

**Archivo**: `eventos/templates/eventos/eliminar_equipo.html`

```html
{% extends 'eventos/base.html' %}

{% block title %}Eliminar Equipo - Sistema de Eventos Deportivos{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-6 mx-auto">
        <div class="card">
            <div class="card-body">
                <h2 class="card-title">¿Está seguro de eliminar este equipo?</h2>
                <p class="card-text">
                    <strong>Nombre:</strong> {{ object.nombre }}<br>
                    <strong>Deporte:</strong> {{ object.deporte.nombre }}<br>
                    <strong>Ciudad:</strong> {{ object.ciudad }}
                </p>
                <form method="post">
                    {% csrf_token %}
                    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                        <a href="{% url 'eventos:lista_equipos' %}" class="btn btn-secondary">Cancelar</a>
                        <button type="submit" class="btn btn-danger">Eliminar</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Paso 8: Registrar en el Admin

**Archivo**: `eventos/admin.py`

```python
from .models import Deporte, Evento, Participante, Equipo

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'deporte', 'ciudad', 'fecha_fundacion', 'fecha_creacion')
    list_filter = ('deporte', 'ciudad', 'fecha_creacion')
    search_fields = ('nombre', 'ciudad')
    ordering = ('nombre',)
```

### Paso 9: Actualizar la Navegación

**Archivo**: `eventos/templates/eventos/base.html`

Agregar en el menú de navegación:

```html
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" id="equiposDropdown" role="button" data-bs-toggle="dropdown">
        Equipos
    </a>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="{% url 'eventos:lista_equipos' %}">Listar</a></li>
        <li><a class="dropdown-item" href="{% url 'eventos:crear_equipo' %}">Crear</a></li>
    </ul>
</li>
```

### Resumen del Proceso

1. ✅ Crear Model → `makemigrations` → `migrate`
2. ✅ Crear Repository
3. ✅ Crear Service
4. ✅ Crear Form
5. ✅ Crear Views
6. ✅ Crear URLs
7. ✅ Crear Templates
8. ✅ Registrar en Admin
9. ✅ Actualizar Navegación

---

## Despliegue en Docker

Docker permite ejecutar la aplicación en un contenedor aislado, facilitando el despliegue en cualquier entorno.

### Requisitos

- Docker instalado
- Docker Compose instalado (opcional, pero recomendado)

### Paso 1: Crear el Dockerfile

**Archivo**: `Dockerfile`

```dockerfile
# Usar imagen base de Python
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Paso 2: Crear docker-compose.yml

**Archivo**: `docker-compose.yml`

```yaml
version: '3.8'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    environment:
      - DEBUG=1
      - SECRET_KEY=django-insecure-change-in-production
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=eventos_db
      - POSTGRES_USER=eventos_user
      - POSTGRES_PASSWORD=eventos_pass
    ports:
      - "5432:5432"

volumes:
  postgres_data:
  static_volume:
```

### Paso 3: Actualizar settings.py para PostgreSQL

Si quieres usar PostgreSQL en Docker, actualiza `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'eventos_db'),
        'USER': os.environ.get('DB_USER', 'eventos_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'eventos_pass'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

O mantén SQLite para desarrollo:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Paso 4: Crear .dockerignore

**Archivo**: `.dockerignore`

```
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist/
build/
.git
.gitignore
.env
db.sqlite3
*.log
.DS_Store
```

### Paso 5: Construir y Ejecutar

**Opción A: Usando Docker Compose (Recomendado)**

```bash
# Construir las imágenes
docker-compose build

# Ejecutar los contenedores
docker-compose up

# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener los contenedores
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

**Opción B: Usando Docker directamente**

```bash
# Construir la imagen
docker build -t eventos-deportivos .

# Ejecutar el contenedor
docker run -p 8000:8000 eventos-deportivos

# Ejecutar con volúmenes (para desarrollo)
docker run -p 8000:8000 -v $(pwd):/app eventos-deportivos
```

### Paso 6: Ejecutar Migraciones en Docker

```bash
# Con docker-compose
docker-compose exec web python manage.py migrate

# Con docker
docker exec -it <container_id> python manage.py migrate
```

### Paso 7: Crear Superusuario en Docker

```bash
# Con docker-compose
docker-compose exec web python manage.py createsuperuser

# Con docker
docker exec -it <container_id> python manage.py createsuperuser
```

### Acceder a la Aplicación

Una vez que los contenedores estén corriendo:

- **Aplicación web**: http://localhost:8000
- **Admin**: http://localhost:8000/admin

---

## Comandos Útiles

### Desarrollo Local

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ejecutar servidor de desarrollo
python manage.py runserver

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic

# Verificar configuración
python manage.py check
```

### Docker

```bash
# Ver contenedores corriendo
docker ps

# Ver todos los contenedores
docker ps -a

# Ver logs
docker logs <container_id>

# Entrar al contenedor
docker exec -it <container_id> /bin/bash

# Limpiar imágenes no usadas
docker system prune -a
```

### Git

```bash
# Ver estado
git status

# Agregar archivos
git add .

# Commit
git commit -m "Descripción del cambio"

# Push
git push origin main
```

---

## Solución de Problemas

### Error: "No module named 'eventos'"

**Solución**: Asegúrate de estar en el directorio raíz del proyecto y que el entorno virtual esté activado.

### Error: "Table doesn't exist"

**Solución**: Ejecuta las migraciones:
```bash
python manage.py migrate
```

### Error: "Port 8000 already in use"

**Solución**: Usa otro puerto:
```bash
python manage.py runserver 8001
```

### Error en Docker: "Cannot connect to database"

**Solución**: Verifica que el contenedor de base de datos esté corriendo:
```bash
docker-compose ps
docker-compose up db
```

### Error: "Static files not found"

**Solución**: Recolecta archivos estáticos:
```bash
python manage.py collectstatic
```

### Error: "TemplateDoesNotExist"

**Solución**: Verifica que el template esté en la ruta correcta:
```
eventos/templates/eventos/nombre_template.html
```

---

## Recursos Adicionales

- [Documentación de Django](https://docs.djangoproject.com/)
- [Documentación de Docker](https://docs.docker.com/)
- [Documentación de Docker Compose](https://docs.docker.com/compose/)
- [Arquitectura.md](./Arquitectura.md) - Documentación detallada de la arquitectura

---

## Conclusión

Esta guía te ha mostrado:

1. ✅ Cómo funciona el proyecto y su arquitectura
2. ✅ Cómo agregar nuevos componentes siguiendo las 3 capas
3. ✅ Ejemplo completo de agregar "Equipo"
4. ✅ Cómo desplegar en Docker

Recuerda siempre seguir el orden de las capas:
1. **Model** → 2. **Repository** → 3. **Service** → 4. **Form** → 5. **View** → 6. **URLs** → 7. **Templates**

¡Buena suerte con tu desarrollo! 🚀

---

**Creado por**: @xavicrip  
**Fecha**: 2024  
**Versión**: 1.0

