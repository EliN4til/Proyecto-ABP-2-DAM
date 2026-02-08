# Proyecto-ABP-2-DAM
Acceso a datos

# 📋 Sistema de Gestión de Tareas - Documentación Técnica

## 📑 Índice

1. [Descripción General](#descripción-general)
2. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
3. [Estructura de Archivos](#estructura-de-archivos)
4. [Modelos de Datos](#modelos-de-datos)
5. [Operaciones CRUD](#operaciones-crud)
6. [Sistema de Autenticación](#sistema-de-autenticación)
7. [Interfaces de Usuario](#interfaces-de-usuario)
8. [Lógica de Negocio](#lógica-de-negocio)
9. [Sistema de Auditoría](#sistema-de-auditoría)
10. [Instalación y Configuración](#instalación-y-configuración)
11. [Uso de la Aplicación](#uso-de-la-aplicación)

---

## 🎯 Descripción General

**Sistema de Gestión de Tareas** es una aplicación de escritorio desarrollada en Python utilizando el framework **Flet** para la interfaz gráfica y **MongoDB Atlas** como base de datos. La aplicación permite gestionar empleados, departamentos, proyectos y tareas con diferentes niveles de permisos (administrador y usuario estándar).

### Características Principales

- ✅ **Gestión completa de empleados** con validación de DNI/NIE
- ✅ **Gestión de departamentos** y asignación de personal
- ✅ **Gestión de proyectos** con presupuestos y estados
- ✅ **Sistema de tareas** con prioridades, fechas límite y asignaciones
- ✅ **Autenticación y sesiones** con roles diferenciados
- ✅ **Sistema de auditoría** que registra todas las operaciones
- ✅ **Validaciones robustas** con Pydantic
- ✅ **Interfaz moderna** con gradientes y diseño responsive
- ✅ **Persistencia de credenciales** para acceso rápido

---

## 🏗️ Arquitectura del Proyecto

### Patrón Arquitectónico

El proyecto sigue una **arquitectura en capas** (Layered Architecture):

```
┌─────────────────────────────────────┐
│     CAPA DE PRESENTACIÓN (UI)       │  ← Vistas Flet
├─────────────────────────────────────┤
│     CAPA DE LÓGICA DE NEGOCIO       │  ← CRUD + Validaciones
├─────────────────────────────────────┤
│     CAPA DE SERVICIOS                │  ← Gestión de Sesión + DB
├─────────────────────────────────────┤
│     CAPA DE DATOS                    │  ← MongoDB Atlas
└─────────────────────────────────────┘
```

### Stack Tecnológico

| Categoría | Tecnología | Versión |
|-----------|------------|---------|
| **Framework UI** | Flet | ^0.80.5 |
| **Base de Datos** | MongoDB Atlas | 4.x |
| **Driver BD** | PyMongo | ^4.16.0 |
| **Validación** | Pydantic | ^2.12.5 |
| **Testing** | Pytest | ^8.0.0 |
| **Gestión Deps** | Poetry | 2.3.2 |
| **Lenguaje** | Python | 3.14 |

---

## 📂 Estructura de Archivos

```
gestion_tareas/
│
├── main.py                              # Punto de entrada principal
├── pyproject.toml                       # Configuración Poetry
├── poetry.lock                          # Dependencias bloqueadas
├── README.md                            # Documentación
├── .gitignore                           # Archivos excluidos de Git
│
├── modelos/
│   ├── __init__.py
│   ├── init.py                          # Modelos Pydantic + datos prueba
│   └── crud.py                          # Operaciones CRUD completas
│
├── servicios/
│   ├── __init__.py
│   ├── db_manager.py                    # Wrapper conexión BD
│   ├── mongo_service.py                 # Servicio MongoDB
│   └── sesion_service.py                # Gestión de sesión en memoria
│
├── utilidades/
│   ├── __init__.py
│   ├── validaciones.py                  # Validadores email/DNI/teléfono
│   ├── config_db.json                   # Credenciales BD (git-ignored)
│   └── config_login.json                # Email guardado (git-ignored)
│
├── vistas/
│   ├── __init__.py
│   │
│   ├── vistas_admin/
│   │   ├── vista_area_admin.py          # Dashboard administrador
│   │   ├── vista_configuracion.py       # Configuración sistema
│   │   ├── vista_auditoria.py           # Registro de operaciones
│   │   ├── vista_estadisticas.py        # Métricas y gráficos
│   │   ├── vista_gestionar_trabajadores.py
│   │   ├── vista_crear_trabajador.py
│   │   ├── vista_gestionar_departamentos.py
│   │   ├── vista_crear_departamento.py
│   │   ├── vista_gestionar_proyectos.py
│   │   └── vista_crear_proyectos.py
│   │
│   └── vistas_usuario/
│       ├── vista_conexion.py            # Conexión MongoDB
│       ├── vista_login.py               # Inicio de sesión
│       ├── vista_error_404.py           # Página de error
│       ├── vista_area_personal.py       # Dashboard usuario
│       ├── vista_mis_datos.py           # Perfil usuario
│       ├── vista_tareas_pendientes.py
│       ├── vista_tareas_realizadas.py
│       ├── vista_tareas_atrasadas.py
│       ├── vista_nueva_tarea.py
│       ├── vista_compartido_conmigo.py
│       ├── vista_detalle_tarea.py
│       └── vista_mis_proyectos.py
│
└── tests/
    └── test_crud.py                     # Tests unitarios con mocks
```

---

## 📊 Modelos de Datos

### 1. EmpleadoModel

**Colección:** `empleados`

```python
{
    "_id": ObjectId,
    "identificador": str,           # DNI/NIE único
    "nombre": str,
    "apellidos": str,
    "email": EmailStr,              # Validado por Pydantic
    "contrasenya": str,          
    "foto": str | None,
    "estado": "ACTIVO" | "INACTIVO" | "PENDIENTE",
    "empresa": str,
    "equipo": str,
    "proyecto": str | None,
    "departamento": {
        "nombre": str,
        "ubicacion": str
    },
    "cargo": str,
    "id_empleado": str,
    "telefono": str | None,
    "ubicacion": str,
    "fecha_incorporacion": datetime,
    "fecha_alta": datetime | None,
    "es_admin": bool                # Rol de administrador
}
```

**Validaciones:**
- Email único (validado con `email-validator`)
- Identificador único (DNI/NIE validado con algoritmo)
- Estados permitidos: ACTIVO, INACTIVO, PENDIENTE

---

### 2. DepartamentoModel

**Colección:** `departamentos`

```python
{
    "_id": ObjectId,
    "nombre": str,
    "codigo": str,                  # Código único
    "empresa": str,
    "responsable": str,
    "descripcion": str | None,
    "ubicacion": str | None,
    "email": str,
    "telefono": str,
    "presupuesto": float | None,
    "estado": "ACTIVO" | "INACTIVO" | "EN CREACIÓN",
    "miembros": [
        {
            "id_usuario": str,
            "nombre": str,
            "apellidos": str,
            "identificador": str
        }
    ],
    "proyecto_asignado": str | None,
    "fecha_creacion": datetime | None
}
```

**Patrón de diseño:** Embedding de miembros (desnormalización controlada)

---

### 3. ProyectoModel

**Colección:** `proyectos`

```python
{
    "_id": ObjectId,
    "nombre": str,
    "codigo": str,                  # Código único
    "responsable": str,
    "cliente": str,
    "presupuesto": float | None,
    "estado": "ACTIVO" | "PAUSADO" | "INACTIVO",
    "fecha_inicio": datetime,
    "fecha_fin": datetime | None,
    "descripcion": str,
    "fecha_creacion": datetime | None
}
```

---

### 4. TareaModel

**Colección:** `tareas`

```python
{
    "_id": ObjectId,
    "titulo": str,
    "requisitos": str | None,
    "estado": "pendiente" | "en_proceso" | "completado",
    "tags": [str],
    "icono": str,                   # Emoji
    "id_proyecto": str,             # Referencia a proyecto
    "proyecto": str | None,         # Nombre proyecto (desnormalizado)
    "prioridad": "alta" | "media" | "baja",
    "asignados": [
        {
            "id_usuario": str,
            "nombre": str,
            "foto": str | None
        }
    ],
    "compartido_por": str | None,
    "atrasado": bool,
    "fecha_inicio": datetime,
    "fecha_limite": datetime | None,
    "fecha_completado": datetime | None,
    "fecha_modificacion": datetime | None
}
```

**Patrón Subset:** Guarda resumen de usuarios asignados para evitar JOINs.

---

### 5. RolModel

**Colección:** `roles`

```python
{
    "_id": ObjectId,
    "nombre": str,
    "codigo": str,
    "descripcion": str | None,
    "usuarios": int,
    "color": str,                   # Hex color
    "permisos": {}                  # Diccionario flexible
}
```

---

### 6. ConfiguracionModel

**Colección:** `configuracion` (documento único)

```python
{
    "_id": ObjectId,
    "empresa": str,                 # Default: "TechSolutions S.L"
    "sesion": str                   # Default: "1 hora"
}
```

---

### 7. AuditoriaModel

**Colección:** `auditoria`

```python
{
    "_id": ObjectId,
    "accion": str,                  # Crear, Editar, Eliminar, Login, Configuración
    "modulo": str,                  # Usuarios, Tareas, Departamentos, etc.
    "descripcion": str,
    "usuario": str,
    "fecha_completa": datetime,
    "ip": str | None                # Opcional
}
```

---

## 🔧 Operaciones CRUD

### Estructura General de Respuestas

Todas las funciones CRUD siguen el patrón:

```python
(exito: bool, resultado: dict | list | str)
```

**Ejemplo:**
```python
exito, datos = crear_empleado({...})
if exito:
    print(f"ID creado: {datos['_id']}")
else:
    print(f"Errores: {datos}")
```

---

### CRUD de Empleados

#### `crear_empleado(datos: dict) -> tuple`

**Flujo:**
1. Valida datos con `EmpleadoModel` (Pydantic)
2. Comprueba duplicados de email e identificador
3. Inserta en MongoDB
4. Registra en auditoría
5. Retorna `(True, empleado_con_id)` o `(False, lista_errores)`

**Validaciones:**
- Email único y válido
- DNI/NIE único y válido (algoritmo de letra)
- Campos obligatorios según modelo

```python
datos = {
    "identificador": "12345678Z",
    "nombre": "Juan",
    "apellidos": "Pérez",
    "email": "juan@empresa.com",
    "contrasenya": "pass123",
    "empresa": "TechCorp",
    "equipo": "Backend",
    "departamento": {"nombre": "IT", "ubicacion": "Madrid"},
    "cargo": "Desarrollador",
    "id_empleado": "EMP001",
    "ubicacion": "Madrid",
    "fecha_incorporacion": datetime.now()
}

exito, resultado = crear_empleado(datos)
```

#### `obtener_empleado(id_empleado: str) -> tuple`

Retorna un empleado por su `_id`. Convierte ObjectId a string.

#### `obtener_empleado_por_email(email: str) -> tuple`

Busca por email (usado en login).

#### `obtener_todos_empleados() -> tuple`

Retorna lista completa de empleados.

#### `actualizar_empleado(id_empleado: str, datos: dict) -> tuple`

Actualiza campos específicos con `$set`.

#### `eliminar_empleado(id_empleado: str) -> tuple`

Elimina físicamente el documento y registra en auditoría.

---

### CRUD de Departamentos

#### `crear_departamento(datos: dict) -> tuple`

**Validaciones adicionales:**
- Código de departamento único
- Fecha de creación automática si no se proporciona

```python
datos = {
    "nombre": "Recursos Humanos",
    "codigo": "RRHH001",
    "empresa": "TechCorp",
    "responsable": "María López",
    "email": "rrhh@empresa.com",
    "telefono": "+34 912345678",
    "presupuesto": 50000.00
}
```

#### `actualizar_departamento(id_departamento: str, datos: dict) -> tuple`

Permite actualizar campos como presupuesto, estado, miembros, etc.

#### `agregar_miembro_departamento(id_depto: str, miembro: dict) -> tuple`

Usa operador `$push` para agregar al array `miembros`.

```python
miembro = {
    "id_usuario": "507f1f77bcf86cd799439011",
    "nombre": "Ana",
    "apellidos": "García",
    "identificador": "87654321X"
}
```

#### `eliminar_miembro_departamento(id_depto: str, id_usuario: str) -> tuple`

Usa operador `$pull` para remover del array.

---

### CRUD de Proyectos

#### `crear_proyecto(datos: dict) -> tuple`

**Validaciones:**
- Código único
- Fecha de inicio obligatoria
- Estados: ACTIVO, PAUSADO, INACTIVO

```python
datos = {
    "nombre": "App Móvil v2.0",
    "codigo": "PRY001",
    "responsable": "Carlos Ruiz",
    "cliente": "ClienteCorp",
    "presupuesto": 100000.00,
    "fecha_inicio": datetime.now(),
    "fecha_fin": datetime(2026, 12, 31),
    "descripcion": "Desarrollo de nueva versión"
}
```

#### `obtener_proyectos_activos() -> tuple`

Retorna solo proyectos con `estado: "ACTIVO"`.

---

### CRUD de Tareas

#### `crear_tarea(datos: dict) -> tuple`

**Campos clave:**
- `id_proyecto`: Referencia al proyecto
- `asignados`: Lista de usuarios (patrón Subset)
- `prioridad`: alta, media, baja
- `estado`: pendiente, en_proceso, completado

```python
datos = {
    "titulo": "Diseñar base de datos",
    "requisitos": "Modelo ER completo",
    "icono": "📋",
    "id_proyecto": "507f1f77bcf86cd799439011",
    "proyecto": "App Móvil v2.0",
    "prioridad": "alta",
    "asignados": [
        {
            "id_usuario": "507f191e810c19729de860ea",
            "nombre": "Laura",
            "foto": None
        }
    ],
    "fecha_inicio": datetime.now(),
    "fecha_limite": datetime(2026, 3, 15)
}
```

#### `obtener_tareas_usuario(id_usuario: str) -> tuple`

Retorna tareas donde el usuario está en el array `asignados`.

**Query MongoDB:**
```python
{"asignados.id_usuario": id_usuario}
```

#### `obtener_tareas_pendientes_usuario(id_usuario: str) -> tuple`

Filtra por estado pendiente o en_proceso.

#### `obtener_tareas_completadas_usuario(id_usuario: str) -> tuple`

Filtra por estado completado.

#### `completar_tarea(id_tarea: str) -> tuple`

Actualiza estado y registra `fecha_completado`.

---

### Sistema de Filtrado y Ordenamiento

#### `filtrar_tareas(tareas: list, filtros: dict, texto_busqueda: str) -> list`

**Filtros disponibles:**
- `prioridad`: "alta", "media", "baja", "Todas"
- `tag`: Cualquier tag de la lista de tags
- `proyecto`: Nombre del proyecto
- Texto de búsqueda: busca en título y proyecto

**Ejemplo:**
```python
filtros = {
    "prioridad": "alta",
    "tag": "Backend",
    "proyecto": "App Móvil v2.0"
}
resultado = filtrar_tareas(todas_tareas, filtros, "diseño")
```

#### `ordenar_tareas(tareas: list, criterio: str, campo_fecha: str) -> list`

**Criterios disponibles:**
- "Alfabético A-Z"
- "Alfabético Z-A"
- "Por prioridad alta"
- "Por prioridad baja"
- "Por proyecto"
- "Fecha ascendente"
- "Fecha descendente"
- "Más atrasado primero"
- "Menos atrasado primero"

**Implementación de prioridad:**
```python
orden = {"alta": 0, "media": 1, "baja": 2}
sorted(tareas, key=lambda t: orden.get(t.get("prioridad"), 1))
```

---

## 🔐 Sistema de Autenticación

### Flujo de Autenticación

```
┌──────────────┐
│   Conexión   │ → MongoDB Atlas con credenciales
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    Login     │ → Validar email + contraseña
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Sesión     │ → Guardar usuario en memoria
└──────┬───────┘
       │
       ├─→ es_admin = True  → Vista Admin
       │
       └─→ es_admin = False → Vista Personal
```

### Gestión de Sesión (sesion_service.py)

**Variables globales:**
```python
_usuario_activo = None
_contexto_dashboard = "personal"  # "admin" | "personal"
```

**Funciones principales:**

#### `guardar_usuario(datos_usuario: dict)`
Almacena el objeto completo del empleado en memoria.

#### `obtener_usuario() -> dict | None`
Retorna el usuario activo o None.

#### `hay_sesion() -> bool`
Verifica si existe sesión activa.

#### `cerrar_sesion()`
Limpia la variable `_usuario_activo`.

#### `establecer_contexto(contexto: str)`
Guarda si el usuario accedió desde área admin o personal (para navegación inteligente).

#### `obtener_contexto() -> str`
Retorna el contexto actual.

---

### Validación de Credenciales

#### `validar_login(email: str, contrasenya: str) -> tuple`

**Flujo:**
1. Busca empleado por email
2. Compara contraseñas en texto plano ⚠️
3. Registra intento en auditoría
4. Retorna `(True, empleado)` o `(False, mensaje_error)`


---

### Persistencia de Credenciales

#### Conexión BD (`vista_conexion.py`)

Guarda en `utilidades/config_db.json`:
```json
{
    "uri": "gestiontareas1.mgzio0n.mongodb.net",
    "usuario": "admin"
}
```

**No guarda la contraseña** por seguridad.

#### Login (`vista_login.py`)

Guarda en `utilidades/config_login.json`:
```json
{
    "email": "usuario@empresa.com"
}
```

**Flujo de login rápido:**
1. Detecta email guardado
2. Muestra diálogo de confirmación
3. Solicita solo contraseña
4. Ejecuta login completo

---

## 🎨 Interfaces de Usuario

### Paleta de Colores Corporativa

```python
COLOR_FONDO_TOP = "#152060"      # Azul oscuro
COLOR_FONDO_BOT = "#4FC3F7"      # Azul claro
COLOR_HEADER_BG = "#1F2855"      # Azul header
COLOR_BTN_BG = "#4682B4"         # Azul botones
COLOR_LABEL = "#5B9BD5"          # Azul labels
COLOR_BORDE = "#E0E0E0"          # Gris borde

# Estados
COLOR_CREAR = "#4CAF50"          # Verde
COLOR_EDITAR = "#2196F3"         # Azul
COLOR_ELIMINAR = "#E53935"       # Rojo
COLOR_LOGIN = "#9C27B0"          # Púrpura
```

### Componentes Reutilizables

#### Gradiente de Fondo
```python
ft.LinearGradient(
    begin=ft.Alignment(-1, -1),
    end=ft.Alignment(1, 1),
    colors=[COLOR_FONDO_TOP, COLOR_FONDO_BOT]
)
```

#### Tarjeta con Sombra
```python
ft.Container(
    bgcolor="white",
    border_radius=25,
    shadow=ft.BoxShadow(
        spread_radius=0,
        blur_radius=15,
        color="#40000000",
        offset=ft.Offset(0, 5)
    )
)
```

#### Header Flotante
```python
ft.Container(
    width=220,
    height=50,
    bgcolor=COLOR_HEADER_BG,
    border_radius=25,
    alignment=ft.Alignment(0, 0),
    content=ft.Text("TÍTULO", size=18, weight="bold", color="white")
)
```

---

### Vistas Administrativas

#### 1. **vista_area_admin.py** - Dashboard Admin

Menú de 8 opciones en grid 3x3:
- Gestionar Trabajadores
- Gestionar Departamentos
- Gestionar Proyectos
- Ver Estadísticas
- Configuración
- Registro de Auditoría
- Ir al Área Personal
- Cerrar Sesión

**Navegación:**
```python
async def click_gestionar_trabajadores(e):
    await page.push_route("/gestionar_trabajadores")
```

#### 2. **vista_gestionar_trabajadores.py** - Gestión de Empleados

**Componentes principales:**
- Barra de búsqueda con filtrado en tiempo real
- Lista scrollable de tarjetas de empleados
- Botón flotante "+" para crear nuevo
- Diálogo de edición con todos los campos
- Confirmación de eliminación

**Funcionalidades:**
- Buscar por nombre, email, DNI
- Editar datos completos
- Cambiar estado (ACTIVO/INACTIVO)
- Eliminar con confirmación
- Ver detalles completos

**Tarjeta de empleado:**
```python
ft.Container(
    bgcolor="white",
    border_radius=10,
    padding=12,
    content=ft.Row([
        ft.CircleAvatar(radius=25, content=ft.Text(iniciales)),
        ft.Column([
            ft.Text(nombre, weight="bold"),
            ft.Text(cargo, size=11),
            ft.Text(email, size=10, color="grey")
        ]),
        ft.IconButton(icon=ft.Icons.EDIT, on_click=editar),
        ft.IconButton(icon=ft.Icons.DELETE, on_click=eliminar)
    ])
)
```

#### 3. **vista_crear_trabajador.py** - Formulario de Alta

**Campos del formulario:**
- DNI/NIE con validación algoritmo letra
- Nombre y Apellidos
- Email con validación formato
- Contraseña con reveal
- Empresa (read-only desde config)
- Departamento (dropdown dinámico desde BD)
- Cargo
- ID Empleado
- Teléfono con validación formato español
- Ubicación
- Fecha de incorporación (DatePicker)

**Validaciones en tiempo real:**
```python
def validar_dni(dni: str) -> tuple:
    letras_control = "TRWAGMYFPDXBNJZSQVHLCKE"
    numero = int(dni[:8])
    letra_esperada = letras_control[numero % 23]
    return (dni[8] == letra_esperada, letra_esperada)
```

#### 4. **vista_auditoria.py** - Registro de Auditoría

**Filtros disponibles:**
- Tipo de acción (Crear, Editar, Eliminar, Login, Configuración)
- Módulo (Usuarios, Tareas, Departamentos, etc.)
- Período (Hoy, Últimos 7 días, Todos)
- Búsqueda de texto

**Tarjeta de registro:**
```python
ft.Row([
    ft.Column([
        ft.Text(icono_accion, size=18),
        ft.Container(
            bgcolor=color_accion,
            content=ft.Text(accion.upper(), size=8, color="white")
        )
    ]),
    ft.Column([
        ft.Text(descripcion, size=11, weight="w500"),
        ft.Row([
            ft.Text(f"👤 {usuario}", size=9),
            ft.Text(f"{fecha} {hora}", size=9)
        ])
    ])
])
```

#### 5. **vista_estadisticas.py** - Métricas y KPIs

**Métricas principales:**
- Total empleados activos
- Total departamentos
- Total proyectos activos
- Tareas pendientes totales
- Tareas completadas este mes
- Tasa de cumplimiento

**Gráficos:**
- Distribución de empleados por departamento (barras)
- Tareas por estado (circular)
- Evolución de tareas en el tiempo (líneas)

#### 6. **vista_configuracion.py** - Ajustes del Sistema

**Configuraciones disponibles:**
- Nombre de la empresa
- Tiempo de expiración de sesión:
  - 30 minutos
  - 1 hora
  - 4 horas
  - 8 horas

**Persistencia:**
Guarda en colección `configuracion` (documento único con upsert).

---

### Vistas de Usuario

#### 7. **vista_area_personal.py** - Dashboard Usuario

Menú de 7 opciones:
- Mis datos
- Tareas pendientes
- Tareas realizadas
- Crear nueva tarea
- Tareas compartidas conmigo
- Tareas atrasadas
- Mis proyectos

**Condicional para admins:**
```python
if usuario.get("es_admin", False):
    # Agregar botón "Volver al área de admin"
```

#### 8. **vista_tareas_pendientes.py** - Listado de Tareas

**Funcionalidades:**
- Búsqueda por texto (título, proyecto)
- Filtros:
  - Prioridad (Alta, Media, Baja, Todas)
  - Tag (Backend, Frontend, Testing, etc.)
  - Proyecto
- Ordenamiento:
  - Alfabético A-Z / Z-A
  - Por prioridad
  - Por fecha
  - Por proyecto

**Tarjeta de tarea:**
```python
ft.Container(
    bgcolor="white",
    border_radius=12,
    padding=12,
    content=ft.Column([
        ft.Row([
            ft.Text(emoji, size=24),
            ft.Column([
                ft.Text(titulo, weight="bold", size=13),
                ft.Text(proyecto, size=10, color="grey")
            ])
        ]),
        ft.Row([
            ft.Container(  # Badge prioridad
                bgcolor=color_prioridad,
                content=ft.Text(prioridad, color="white")
            ),
            ft.Text(f"📅 {fecha_limite}", size=10)
        ])
    ])
)
```

#### 9. **vista_nueva_tarea.py** - Formulario de Creación

**Campos:**
- Título (obligatorio)
- Emoji/Icono (selector visual)
- Proyecto (dropdown de proyectos activos)
- Prioridad (RadioGroup)
- Tags (multiselect con chips)
- Requisitos (TextField multilínea)
- Fecha inicio y límite (DatePickers)
- Asignados (multiselect de empleados del proyecto)

**Validaciones:**
- Título no vacío
- Proyecto seleccionado
- Fecha límite > Fecha inicio
- Al menos un asignado

#### 10. **vista_mis_datos.py** - Perfil de Usuario

**Información mostrada:**
- Nombre y apellidos
- Estado con indicador visual
- DNI/NIE
- Empresa
- Departamento
- Equipo
- Cargo
- ID Empleado
- Email corporativo
- Teléfono
- Ubicación
- Fecha de incorporación

**Funcionalidad adicional:**
Botón "Cambiar Contraseña" con validación de contraseña actual.

---

## 💼 Lógica de Negocio

### Patrón Subset en MongoDB

**Problema:** JOINs son costosos en MongoDB.

**Solución:** Almacenar subset de datos relacionados.

**Ejemplo en Tareas:**
```python
# En lugar de solo guardar ID:
"asignados": ["507f191e810c19729de860ea"]

# Guardamos subset:
"asignados": [
    {
        "id_usuario": "507f191e810c19729de860ea",
        "nombre": "Laura",
        "foto": "https://..."
    }
]
```

**Ventajas:**
- Carga rápida sin consultas adicionales
- Reduce latencia en interfaces de usuario

**Desventajas:**
- Redundancia de datos
- Requiere actualización sincronizada

---

### Sistema de Estados

#### Estados de Empleado
```python
"ACTIVO"      # Trabajando normalmente
"INACTIVO"    # Baja temporal o permanente
"PENDIENTE"   # Recién creado, pendiente de activación
```

#### Estados de Departamento
```python
"ACTIVO"        # Operativo
"INACTIVO"      # Cerrado o en stand-by
"EN CREACIÓN"   # En proceso de configuración
```

#### Estados de Proyecto
```python
"ACTIVO"   # En desarrollo
"PAUSADO"  # Detenido temporalmente
"INACTIVO" # Finalizado o cancelado
```

#### Estados de Tarea
```python
"pendiente"    # No iniciada
"en_proceso"   # En desarrollo
"completado"   # Terminada
```

---

### Cálculo de Tareas Atrasadas

**Lógica:**
```python
def calcular_atraso(tarea):
    if tarea["estado"] == "completado":
        return False
    
    fecha_limite = tarea.get("fecha_limite")
    if not fecha_limite:
        return False
    
    hoy = datetime.now()
    if hoy > fecha_limite:
        dias_atrasado = (hoy - fecha_limite).days
        return True, dias_atrasado
    
    return False, 0
```

**Implementación en vistas:**
```python
exito, tareas = obtener_tareas_pendientes_usuario(id_usuario)
tareas_atrasadas = [t for t in tareas if t.get("atrasado", False)]
```

---

### Sistema de Auditoría

#### Eventos Registrados

| Acción | Módulo | Descripción |
|--------|--------|-------------|
| Crear | Usuarios | "usuario registrado: {nombre}" |
| Editar | Usuarios | "usuario actualizado id: {id}" |
| Eliminar | Usuarios | "usuario eliminado: {nombre}" |
| Login | Sistema | "sesión iniciada: {email}" |
| Login | Sistema | "fallo de acceso: {razón}" |
| Crear | Tareas | "tarea creada: {título}" |
| Editar | Tareas | "tarea actualizada" |
| Eliminar | Tareas | "tarea borrada" |
| Configuración | Sistema | "configuración actualizada" |

#### Función de Registro

```python
def registrar_log(accion, modulo, descripcion, usuario=None):
    if usuario is None:
        usuario = obtener_nombre_usuario()
        if usuario == "Usuario":
            usuario = "Sistema"
    
    log = {
        "accion": accion,
        "modulo": modulo,
        "descripcion": descripcion,
        "usuario": usuario,
        "fecha_completa": datetime.now()
    }
    get_db().auditoria.insert_one(log)
```

**Uso en CRUD:**
```python
def crear_empleado(datos):
    resultado = get_db().empleados.insert_one(...)
    registrar_log("Crear", "Usuarios", f"usuario registrado: {datos['nombre']}")
    return (True, datos)
```

---

## 🔧 Instalación y Configuración

### Requisitos Previos

- Python 3.10 o superior
- MongoDB Atlas account (gratuito)
- Poetry 2.x (gestor de dependencias)

---

### Instalación Paso a Paso

#### 1. Clonar el Repositorio

```bash
git clone https://github.com/EliN4til/Proyecto-ABP-2-DAM.git
cd gestion_tareas
```

#### 2. Instalar Poetry (si no lo tienes)

**Opción A: Con pip**
```powershell
pip install poetry
```

**Opción B: Instalador oficial**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org/ -UseBasicParsing).Content | python -
```

**Agregar al PATH** (Windows):
```powershell
[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "User") + ";C:\Users\TU_USUARIO\AppData\Roaming\Python\Python314\Scripts",
    "User"
)
```

**Opción C: LE FUNCIONÓ ASI A PABLO**
```powershell
"C:\Users\pablo\AppData\Roaming\Python\Python314\Scripts\poetry.exe" install
>> & "C:\Users\pablo\AppData\Roaming\Python\Python314\Scripts\poetry.exe"
```
Cambiando el usuario por el vuestro y suponiendo que el python no sea de windows store



#### 3. Instalar Dependencias

```bash
# Instalar todas las dependencias del proyecto
poetry install

# Activar el entorno virtual
poetry shell
```

#### 4. Configurar MongoDB Atlas

1. Crear cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Crear un cluster gratuito
3. Configurar acceso de red (permitir tu IP o 0.0.0.0/0 para desarrollo)
4. Crear usuario de base de datos
5. Obtener la connection string:
   ```
   mongodb+srv://USUARIO:CONTRASEÑA@cluster.mongodb.net/?appName=GestionTareas1
   ```

#### 5. Cargar Datos de Prueba (Opcional)

```bash
python -m gestion_tareas.modelos.init
```

Esto crea:
- 1 empleado de prueba (Laura García)
- 1 proyecto de prueba
- 1 tarea de prueba

---

### Ejecución de la Aplicación

#### Método 1: Con Poetry (recomendado)

```bash
poetry run start
```

#### Método 2: Python directo

```bash
python -m gestion_tareas.main
```

#### Método 3: Ejecutable Poetry

```bash
python -m poetry run start
```

---

### Estructura de la Base de Datos

**Nombre de la BD:** `tareas_db`

**Colecciones:**
- `empleados` - Usuarios del sistema
- `departamentos` - Departamentos de la empresa
- `proyectos` - Proyectos activos
- `tareas` - Tareas asignadas
- `roles` - Roles y permisos
- `configuracion` - Configuración global
- `auditoria` - Registro de operaciones

---

## 📱 Uso de la Aplicación

### Primera Ejecución

#### 1. Pantalla de Conexión

- Introduce la **URI del servidor** (ej: `gestiontareas1.mgzio0n.mongodb.net`) (en este caso para esta tarea)
- Introduce el **usuario** de MongoDB
- Introduce la **contraseña**
- Click en "Conectarse"

**Persistencia:** La URI y usuario se guardan en `config_db.json` para futuras conexiones.

#### 2. Pantalla de Login

- Introduce tu **email corporativo**
- Introduce tu **contraseña**
- Click en "Iniciar Sesión"

**Persistencia:** El email se guarda en `config_login.json` para login rápido.

**Login rápido:** Si detecta email guardado, solo pide contraseña.

---

### Flujo de Usuario Normal

```
Login → Área Personal → [Seleccionar opción]
├─ Mis datos
│  └─ Ver perfil + Cambiar contraseña
├─ Tareas pendientes
│  ├─ Buscar/Filtrar/Ordenar
│  └─ Click en tarea → Detalle → Completar/Editar
├─ Tareas realizadas
│  └─ Historial de tareas completadas
├─ Crear nueva tarea
│  └─ Formulario completo → Guardar
├─ Tareas compartidas conmigo
│  └─ Tareas donde estoy asignado
├─ Tareas atrasadas
│  └─ Tareas con fecha límite pasada
└─ Mis proyectos
   └─ Proyectos donde participo
```

---

### Flujo de Administrador

```
Login → [Puede elegir]
├─ Área Admin
│  ├─ Gestionar Trabajadores
│  │  ├─ Buscar
│  │  ├─ Crear nuevo → Formulario
│  │  ├─ Editar → Modificar datos
│  │  └─ Eliminar → Confirmar
│  ├─ Gestionar Departamentos
│  │  └─ CRUD completo + Gestión de miembros
│  ├─ Gestionar Proyectos
│  │  └─ CRUD completo + Estados
│  ├─ Ver Estadísticas
│  │  └─ KPIs + Gráficos
│  ├─ Configuración
│  │  └─ Empresa + Sesión
│  ├─ Registro de Auditoría
│  │  └─ Filtros + Búsqueda
│  └─ Ir al Área Personal
│     └─ Acceso a funciones de usuario
└─ Área Personal
   └─ (Funciones normales de usuario)
```

---

### Casos de Uso Principales

#### Crear un Empleado

1. Admin → Área Admin → Gestionar Trabajadores
2. Click en botón flotante "+"
3. Rellenar formulario:
   - DNI con letra válida
   - Email único
   - Seleccionar departamento existente
   - Fecha de incorporación
4. Click "Crear Trabajador"
5. Sistema valida y guarda
6. Registro en auditoría

#### Asignar Tarea

1. Usuario → Área Personal → Crear nueva tarea
2. Título y emoji
3. Seleccionar proyecto
4. Seleccionar prioridad
5. Agregar tags
6. Escribir requisitos
7. Seleccionar fechas
8. Agregar asignados (empleados del proyecto)
9. Click "Crear Tarea"
10. Sistema crea y registra

#### Completar Tarea

1. Usuario → Tareas pendientes
2. Click en tarjeta de tarea
3. Vista detalle
4. Click "Completar"
5. Sistema actualiza estado y fecha_completado
6. Mueve a tareas realizadas

#### Generar Reporte de Auditoría

1. Admin → Área Admin → Registro de Auditoría
2. Aplicar filtros:
   - Tipo: "Editar"
   - Módulo: "Usuarios"
   - Período: "Últimos 7 días"
3. Buscar texto: "contraseña"
4. Resultados filtrados en tiempo real
5. Click en registro → Ver detalle completo

---

## 🧪 Testing

### Estructura de Tests

**Archivo:** `tests/test_crud.py`

**Framework:** pytest con mocks

**Cobertura:**
- ✅ Creación de tareas
- ✅ Validaciones de Pydantic
- ✅ Obtención de tareas
- ✅ Creación de empleados
- ✅ Validación de duplicados
- ✅ Creación de departamentos
- ✅ Creación de proyectos

### Ejecución de Tests

```bash
# Con Poetry
poetry run pytest

# Con coverage
poetry run pytest --cov=gestion_tareas

# Verbose
poetry run pytest -v

# Test específico
poetry run pytest tests/test_crud.py::TestCRUD::test_crear_tarea_exito
```

### Ejemplo de Test con Mock

```python
def test_crear_tarea_exito(self, mock_db):
    datos_tarea = {
        "titulo": "Tarea de Prueba",
        "estado": "pendiente",
        "prioridad": "alta",
        "id_proyecto": "000000000000000000000123",
        "fecha_inicio": datetime.now()
    }
    
    # Mock del resultado de insert_one
    mock_resultado = MagicMock()
    mock_resultado.inserted_id = "nuevo_id_123"
    mock_db.tareas.insert_one.return_value = mock_resultado

    # Ejecutar
    exito, resultado = crear_tarea(datos_tarea)

    # Assertions
    assert exito is True
    assert resultado["_id"] == "nuevo_id_123"
    mock_db.tareas.insert_one.assert_called_once()
```

---


---