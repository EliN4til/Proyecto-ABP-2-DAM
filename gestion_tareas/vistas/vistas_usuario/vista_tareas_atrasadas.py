import flet as ft
from gestion_tareas.modelos.crud import obtener_tareas_atrasadas, completar_tarea, filtrar_y_ordenar
from datetime import datetime

def VistaTareasAtrasadas(page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_SOMBRA_TARJETAS = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_ATRASADO = "#E53935"
    COLOR_PRIORIDAD_ALTA = "#E53935"
    COLOR_PRIORIDAD_MEDIA = "#FF9800"
    COLOR_PRIORIDAD_BAJA = "#4CAF50"
    COLOR_COMPLETADO = "#4CAF50"

    #opciones de filtro
    FILTROS_TAGS = ["Todos", "Desarrollo", "Bug Fix", "Testing", "Diseño", "Documentación", "DevOps", "Base de Datos", "API", "Frontend", "Backend"]
    FILTROS_PROYECTO = ["Todos", "App Móvil v2.0", "Portal Web Cliente", "API REST Services", "Dashboard Analytics", "Sistema de Pagos", "CRM Interno", "Migración Cloud"]
    FILTROS_PRIORIDAD = ["Todas", "Alta", "Media", "Baja"]
    FILTROS_ORDEN = [
        "Más atrasado primero", 
        "Menos atrasado primero", 
        "Fecha ascendente",
        "Fecha descendente",
        "Alfabético A-Z", 
        "Alfabético Z-A",
        "Por prioridad alta",
        "Por prioridad baja",
        "Por proyecto",
    ]

    filtro_tag_actual = ["Todos"]
    filtro_proyecto_actual = ["Todos"]
    filtro_prioridad_actual = ["Todas"]
    filtro_orden_actual = ["Más atrasado primero"]

    # --- LÓGICA DE BASE DE DATOS ---

    def cargar_tareas_atrasadas():
        """Obtiene las tareas atrasadas de la base de datos"""
        exito, resultado = obtener_tareas_atrasadas()
        if exito:
            tareas = []
            for t in resultado:
                #formateamos la fecha
                fecha = ""
                dias_atrasado = 0
                if t.get("fecha_limite"):
                    fecha_limite = t["fecha_limite"]
                    fecha = fecha_limite.strftime("%d/%m/%y")
                    #calculamos días de atraso
                    diferencia = datetime.now() - fecha_limite
                    dias_atrasado = max(0, diferencia.days)
                
                #obtenemos los nombres de los asignados
                asignados_nombres = []
                for asignado in t.get("asignados", []):
                    if isinstance(asignado, dict):
                        asignados_nombres.append(asignado.get("nombre", "Sin nombre"))
                    else:
                        asignados_nombres.append(str(asignado))
                
                #obtenemos el primer tag o lo dejamos vacío
                tags = t.get("tags", [])
                tag = tags[0] if tags else "General"
                
                #creamos el diccionario de la tarea
                tarea = {
                    "_id": t.get("_id"),
                    "titulo": t.get("titulo", "Sin título"),
                    "tag": tag,
                    "emoji": t.get("icono", "📋"),
                    "proyecto": t.get("proyecto", "Sin proyecto"),
                    "departamento": "General",
                    "prioridad": t.get("prioridad", "Media"),
                    "asignados": asignados_nombres,
                    "fecha": fecha,
                    "dias_atrasado": dias_atrasado,
                    "requerimientos": [t.get("requisitos", "Sin requisitos")]
                }
                tareas.append(tarea)
            return tareas
        else:
            print(f"Error cargando tareas: {resultado}")
            return []
    
    #cargamos las tareas al inicio
    todas_las_tareas = cargar_tareas_atrasadas()
    
    def actualizar_lista_tareas():
        """Actualiza la lista de tareas en pantalla aplicando filtros sobre la memoria"""
        #preparamos los filtros
        filtros = {
            "prioridad": filtro_prioridad_actual[0],
            "tag": filtro_tag_actual[0],
            "proyecto": filtro_proyecto_actual[0]
        }
        
        #obtenemos el texto de búsqueda
        texto = input_busqueda.value if hasattr(input_busqueda, 'value') else ""
        
        #filtramos y ordenamos usando la función importada
        tareas_filtradas = filtrar_y_ordenar(
            todas_las_tareas, 
            filtros, 
            texto, 
            filtro_orden_actual[0],
            "fecha"
        )
        
        #actualizamos la lista
        lista_tareas.controls = []
        if not tareas_filtradas:
            lista_tareas.controls.append(
                ft.Container(
                    padding=20,
                    content=ft.Text("No hay tareas que coincidan con los filtros", color="grey")
                )
            )
        else:
            for tarea in tareas_filtradas:
                tarjeta = crear_tarjeta_tarea(tarea)
                lista_tareas.controls.append(tarjeta)
        page.update()

    def handle_completar_tarea(e, tarea):
        """Marca la tarea como completada en la BD y la elimina de la vista actual"""
        id_tarea = tarea.get("_id")
        if not id_tarea: return

        exito, mensaje = completar_tarea(id_tarea)
        
        if exito:
            mostrar_mensaje_dialog(page, "✅ Completada", f"Tarea '{tarea['titulo']}' marcada como completada", "green")
            # Recargamos de la base de datos y refrescamos la UI
            nonlocal todas_las_tareas
            todas_las_tareas = cargar_tareas_atrasadas()
            actualizar_lista_tareas()
        else:
            mostrar_mensaje_dialog(page, "❌ Error", f"Error: {mensaje}", "red")
        
        page.update()

    # --- DIÁLOGOS Y UI ---

    def get_color_prioridad(prioridad):
        p = prioridad.lower()
        if p == "alta":
            return COLOR_PRIORIDAD_ALTA
        elif p == "media":
            return COLOR_PRIORIDAD_MEDIA
        else:
            return COLOR_PRIORIDAD_BAJA

    async def btn_volver_click(e):
        await page.push_route("/area_personal")

    def mostrar_mensaje_dialog(page, titulo, mensaje, color):
        """Muestra un diálogo de alerta visible compatible con versiones antiguas"""
        dlg = ft.AlertDialog(
            title=ft.Text(titulo, color="black", weight="bold"),
            content=ft.Text(mensaje, color="black", size=14),
            bgcolor="white",
            actions=[
                ft.TextButton("Entendido", on_click=lambda e: setattr(dlg, "open", False) or page.update())
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def btn_buscar_click(e):
        actualizar_lista_tareas()
        mostrar_mensaje_dialog(page, "🔍 Búsqueda", f"Buscando: {input_busqueda.value}", "blue")
        page.update()

    def mostrar_detalle_tarea(tarea):
        requerimientos_list = ft.Column(
            spacing=6,
            controls=[
                ft.Text(f"• {req}", size=11, color="black")
                for req in tarea["requerimientos"]
            ]
        )

        asignados_text = ", ".join(tarea["asignados"]) if tarea["asignados"] else "Sin asignar"

        dialog_detalle = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Text(tarea["emoji"], size=26),
                    ft.Container(
                        expand=True,
                        content=ft.Text(tarea["titulo"], size=13, weight=ft.FontWeight.BOLD, color="black"),
                    ),
                ],
                spacing=8,
            ),
            bgcolor="white",
            content=ft.Container(
                width=320,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    tight=True,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        #info básica
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Container(
                                    bgcolor=get_color_prioridad(tarea["prioridad"]),
                                    border_radius=10,
                                    padding=ft.Padding(left=8, right=8, top=2, bottom=2),
                                    content=ft.Text(tarea["prioridad"], size=10, color="white", weight=ft.FontWeight.BOLD),
                                ),
                                ft.Row(
                                    spacing=3,
                                    controls=[
                                        ft.Text("TAG:", size=10, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                        ft.Text(tarea["tag"], size=10, color="black", weight=ft.FontWeight.W_500),
                                    ]
                                ),
                            ]
                        ),
                        #atrasado
                        ft.Container(
                            bgcolor="#FFF3F3",
                            border_radius=8,
                            padding=8,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("⚠️ Atrasado:", size=11, color=COLOR_ATRASADO, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"{tarea['dias_atrasado']} días (desde {tarea['fecha']})", size=11, color=COLOR_ATRASADO),
                                ]
                            ),
                        ),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        #proyecto y departamento
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(spacing=2, controls=[
                                    ft.Text("Proyecto", size=10, color=COLOR_LABEL),
                                    ft.Text(tarea["proyecto"], size=11, color="black", weight=ft.FontWeight.W_500),
                                ]),
                                ft.Column(spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END, controls=[
                                    ft.Text("Departamento", size=10, color=COLOR_LABEL),
                                    ft.Text(tarea["departamento"], size=11, color="black", weight=ft.FontWeight.W_500),
                                ]),
                            ]
                        ),
                        #asignados
                        ft.Column(spacing=2, controls=[
                            ft.Text("Asignados", size=10, color=COLOR_LABEL),
                            ft.Text(asignados_text, size=11, color="black"),
                        ]),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        #requerimientos
                        ft.Text("Requerimientos:", size=12, color="black", weight=ft.FontWeight.BOLD),
                        ft.Container(
                            height=120,
                            content=ft.ListView(
                                controls=[requerimientos_list],
                                spacing=5,
                            ),
                        ),
                    ]
                ),
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog(dialog_detalle)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        def cerrar_dialog(dialog):
            dialog.open = False
            page.update()

        page.overlay.append(dialog_detalle)
        dialog_detalle.open = True
        page.update()

    # --- DIÁLOGOS DE FILTROS ---

    def mostrar_dialog_filtros(e):
        radio_orden = ft.RadioGroup(
            value=filtro_orden_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=orden, label=orden, label_style=ft.TextStyle(size=11, color="black")) 
                    for orden in FILTROS_ORDEN
                ],
                spacing=2,
            ),
        )

        radio_prioridad = ft.RadioGroup(
            value=filtro_prioridad_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=prio, label=prio, label_style=ft.TextStyle(size=11, color="black")) 
                    for prio in FILTROS_PRIORIDAD
                ],
                spacing=2,
            ),
        )

        def aplicar_filtros(e):
            filtro_orden_actual[0] = radio_orden.value
            filtro_prioridad_actual[0] = radio_prioridad.value
            dialog_filtros.open = False
            actualizar_lista_tareas()
            mostrar_mensaje_dialog(page, "✅ Filtros", "Filtros aplicados", "blue")
            page.update()

        def limpiar_filtros(e):
            radio_orden.value = "Más atrasado primero"
            radio_prioridad.value = "Todas"
            filtro_orden_actual[0] = "Más atrasado primero"
            filtro_prioridad_actual[0] = "Todas"
            filtro_tag_actual[0] = "Todos"
            filtro_proyecto_actual[0] = "Todos"
            input_busqueda.value = ""
            actualizar_lista_tareas()
            page.update()

        def abrir_filtro_tags(e):
            dialog_filtros.open = False
            page.update()
            mostrar_dialog_tags()

        def abrir_filtro_proyecto(e):
            dialog_filtros.open = False
            page.update()
            mostrar_dialog_proyecto()

        dialog_filtros = ft.AlertDialog(
            modal=True,
            title=ft.Text("Filtrar tareas", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=420,
                bgcolor="white",
                content=ft.Column(
                    spacing=8,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("Por Prioridad:", size=12, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                        radio_prioridad,
                        ft.Divider(height=8, color=COLOR_BORDE),
                        ft.Text("Ordenar por:", size=12, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                        radio_orden,
                        ft.Divider(height=8, color=COLOR_BORDE),
                        ft.Container(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Filtrar por Tag", size=12, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                                    ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=14, color=COLOR_LABEL),
                                ]
                            ),
                            on_click=abrir_filtro_tags,
                            ink=True,
                            padding=8,
                            border_radius=5,
                            bgcolor="#F5F5F5",
                        ),
                        ft.Container(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Filtrar por Proyecto", size=12, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                                    ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=14, color=COLOR_LABEL),
                                ]
                            ),
                            on_click=abrir_filtro_proyecto,
                            ink=True,
                            padding=8,
                            border_radius=5,
                            bgcolor="#F5F5F5",
                        ),
                    ],
                ),
            ),
            actions=[
                ft.TextButton("Limpiar", on_click=limpiar_filtros),
                ft.TextButton("Aplicar", on_click=aplicar_filtros),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_filtros)
        dialog_filtros.open = True
        page.update()

    def mostrar_dialog_tags():
        radio_tags = ft.RadioGroup(
            value=filtro_tag_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=tag, label=tag, label_style=ft.TextStyle(size=11, color="black")) 
                    for tag in FILTROS_TAGS
                ],
                spacing=2,
            ),
        )

        def aplicar_tag(e):
            filtro_tag_actual[0] = radio_tags.value
            dialog_tags.open = False
            actualizar_lista_tareas()
            mostrar_mensaje_dialog(page, "✅ Tag Seleccionado", f"Tag: {filtro_tag_actual[0]}", "blue")
            page.update()

        def volver_filtros(e):
            dialog_tags.open = False
            page.update()
            mostrar_dialog_filtros(None)

        dialog_tags = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text("←", size=18, color="black", weight="bold"),
                        on_click=volver_filtros,
                        ink=True,
                        border_radius=50,
                        padding=5,
                    ),
                    ft.Text("Seleccionar Tag", size=14, weight=ft.FontWeight.BOLD, color="black"),
                ],
                spacing=10,
            ),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=350,
                bgcolor="white",
                content=ft.ListView(
                    controls=[radio_tags],
                    spacing=5,
                ),
            ),
            actions=[
                ft.TextButton("Aplicar", on_click=aplicar_tag),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_tags)
        dialog_tags.open = True
        page.update()

    def mostrar_dialog_proyecto():
        radio_proyecto = ft.RadioGroup(
            value=filtro_proyecto_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=proy, label=proy, label_style=ft.TextStyle(size=11, color="black")) 
                    for proy in FILTROS_PROYECTO
                ],
                spacing=2,
            ),
        )

        def aplicar_proyecto(e):
            filtro_proyecto_actual[0] = radio_proyecto.value
            dialog_proyecto.open = False
            actualizar_lista_tareas()
            mostrar_mensaje_dialog(page, "✅ Proyecto Seleccionado", f"Proyecto: {filtro_proyecto_actual[0]}", "blue")
            page.update()

        def volver_filtros(e):
            dialog_proyecto.open = False
            page.update()
            mostrar_dialog_filtros(None)

        dialog_proyecto = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text("←", size=18, color="black", weight="bold"),
                        on_click=volver_filtros,
                        ink=True,
                        border_radius=50,
                        padding=5,
                    ),
                    ft.Text("Seleccionar Proyecto", size=14, weight=ft.FontWeight.BOLD, color="black"),
                ],
                spacing=10,
            ),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=300,
                bgcolor="white",
                content=ft.ListView(
                    controls=[radio_proyecto],
                    spacing=5,
                ),
            ),
            actions=[
                ft.TextButton("Aplicar", on_click=aplicar_proyecto),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_proyecto)
        dialog_proyecto.open = True
        page.update()

    # --- RENDERIZADO DE TARJETAS ---

    def crear_tarjeta_tarea(tarea):
        """Crea una tarjeta para cada tarea atrasada con el botón de completar"""
        return ft.Container(
            bgcolor="white",
            border_radius=10,
            padding=12,
            margin=ft.Margin(bottom=10),
            border=ft.Border(top=ft.BorderSide(1, "#FFCDD2"), bottom=ft.BorderSide(1, "#FFCDD2"), left=ft.BorderSide(1, "#FFCDD2"), right=ft.BorderSide(1, "#FFCDD2")),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=5,
                color=COLOR_SOMBRA_TARJETAS,
                offset=ft.Offset(0, 2),
            ),
            content=ft.Column(
                spacing=8,
                controls=[
                    #fila 1: Emoji + Título + Prioridad
                    ft.Row(
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(tarea["emoji"], size=22),
                            ft.Text(
                                tarea["titulo"],
                                size=12,
                                color="black",
                                weight=ft.FontWeight.BOLD,
                                expand=True,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Container(
                                bgcolor=get_color_prioridad(tarea["prioridad"]),
                                border_radius=8,
                                padding=ft.Padding(left=6, right=6, top=1, bottom=1),
                                content=ft.Text(tarea["prioridad"], size=9, color="white", weight=ft.FontWeight.BOLD),
                            ),
                        ]
                    ),
                    #fila 2: Proyecto + Tag
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(tarea["proyecto"], size=10, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                            ft.Row(
                                spacing=3,
                                controls=[
                                    ft.Text("TAG:", size=9, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                    ft.Text(tarea["tag"], size=9, color="black", weight=ft.FontWeight.W_500),
                                ]
                            ),
                        ]
                    ),
                    #fila 3: Días atrasado + Fecha
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                f"⚠️ {tarea['dias_atrasado']} días atrasado",
                                size=10,
                                color=COLOR_ATRASADO,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                f"Desde: {tarea['fecha']}",
                                size=9,
                                color="#666666",
                            ),
                        ]
                    ),
                    ft.Divider(height=1, color="#F0F0F0"),
                    # Fila 4: Botones de Acción (Detalles y Completar)
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.TextButton(
                                "Ver detalles",
                                icon=ft.Icons.INFO_OUTLINE,
                                on_click=lambda e, t=tarea: mostrar_detalle_tarea(t),
                                style=ft.ButtonStyle(color=COLOR_LABEL)
                            ),
                            ft.FilledButton(
                                "Marcar completado",
                                icon=ft.Icons.CHECK_CIRCLE,
                                bgcolor=COLOR_COMPLETADO,
                                color="white",
                                height=34,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    text_style=ft.TextStyle(size=11, weight="bold")
                                ),
                                on_click=lambda e, t=tarea: handle_completar_tarea(e, t)
                            )
                        ]
                    )
                ]
            ),
        )

    # --- ELEMENTOS DE LA PÁGINA ---

    input_busqueda = ft.TextField(
        hint_text="Buscar por palabras clave...",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=38,
        expand=True,
        content_padding=ft.Padding(left=10, right=10, top=8, bottom=8),
    )

    btn_filtrar = ft.Container(
        content=ft.Text("Filtrar", size=11, color="black"),
        bgcolor="white",
        border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)),
        border_radius=5,
        padding=ft.Padding(left=12, right=12, top=8, bottom=8),
        on_click=mostrar_dialog_filtros,
        ink=True,
    )

    btn_buscar = ft.Container(
        content=ft.Icon(ft.Icons.SEARCH, size=20, color="white"),
        bgcolor=COLOR_LABEL,
        border_radius=5,
        padding=8,
        on_click=btn_buscar_click,
        ink=True,
    )

    fila_busqueda = ft.Row(
        spacing=8,
        controls=[
            input_busqueda,
            btn_filtrar,
            btn_buscar,
        ]
    )

    lista_tareas = ft.ListView(
        spacing=0,
        expand=True,
    )

    #tarjeta blanca principal
    tarjeta_blanca = ft.Container(
        width=400,
        height=720,
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=COLOR_SOMBRA),
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Container(
                    padding=ft.Padding(left=15, top=10, bottom=5),
                    alignment=ft.Alignment(-1, 0),
                    content=ft.Container(
                        content=ft.Text("←", size=26, color="black", weight="bold"),
                        on_click=btn_volver_click,
                        ink=True,
                        border_radius=50,
                        padding=3,
                    ),
                ),
                ft.Container(
                    height=55,
                    width=400,
                    bgcolor=COLOR_HEADER_BG,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("TAREAS ATRASADAS", size=18, weight=ft.FontWeight.BOLD, color="white")
                ),
                ft.Container(
                    padding=ft.Padding(left=18, right=18, top=15, bottom=15),
                    expand=True,
                    content=ft.Column(
                        spacing=12,
                        expand=True,
                        controls=[
                            fila_busqueda,
                            lista_tareas,
                        ]
                    )
                )
            ]
        )
    )

    # Inicialización
    actualizar_lista_tareas()

    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[COLOR_FONDO_TOP, COLOR_FONDO_BOT],
        ),
        alignment=ft.Alignment(0, 0), 
        content=tarjeta_blanca
    )