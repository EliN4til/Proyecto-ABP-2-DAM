import flet as ft

def VistaTareasAtrasadas(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_SOMBRA_TARJETAS = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_ATRASADO = "#E53935"

    # Opciones de filtro
    FILTROS_TAGS = ["Todos", "Desarrollo", "Bug Fix", "Testing", "Diseño", "Documentación", "DevOps", "Base de Datos", "API", "Frontend", "Backend"]
    FILTROS_ORDEN = [
        "Más atrasado primero", 
        "Menos atrasado primero", 
        "Fecha ascendente (antigua → reciente)",
        "Fecha descendente (reciente → antigua)",
        "Alfabético A-Z", 
        "Alfabético Z-A",
        "Por prioridad alta",
        "Por prioridad baja",
    ]

    filtro_tag_actual = ["Todos"]
    filtro_orden_actual = ["Más atrasado primero"]

    # Datos demo de tareas atrasadas (todas tienen atrasado=True)
    TAREAS_ATRASADAS = [
        {
            "titulo": "Arreglar bug linea 287 fichero UpdateDate.py",
            "tag": "Desarrollo",
            "emoji": "👨‍💻",
            "fecha": "25/12/25",
            "dias_atrasado": 5,
            "requerimientos": [
                "Identificar el error en la línea 287 del fichero UpdateDate.py",
                "El bucle debe iterar correctamente sobre la lista de fechas",
                "Validar que no se produzcan excepciones de tipo IndexError",
                "Añadir logs para seguimiento del proceso",
                "Realizar pruebas con datos de producción simulados",
            ]
        },
        {
            "titulo": "Diseñar mockups para dashboard",
            "tag": "Diseño",
            "emoji": "🎨",
            "fecha": "20/12/25",
            "dias_atrasado": 10,
            "requerimientos": [
                "Crear diseño responsive para desktop y móvil",
                "Incluir gráficos de rendimiento y métricas KPI",
                "Usar la paleta de colores corporativa",
                "Diseñar estados vacíos y de error",
                "Exportar en formato Figma y PNG",
            ]
        },
        {
            "titulo": "Corregir validación formulario registro",
            "tag": "Bug Fix",
            "emoji": "🐛",
            "fecha": "22/12/25",
            "dias_atrasado": 8,
            "requerimientos": [
                "El campo email no valida correctamente dominios .co",
                "El password debe aceptar caracteres especiales",
                "Mostrar mensajes de error específicos por campo",
                "Validar que las contraseñas coincidan",
                "Añadir validación de teléfono internacional",
            ]
        },
        {
            "titulo": "Implementar endpoint de notificaciones",
            "tag": "API",
            "emoji": "🔌",
            "fecha": "18/12/25",
            "dias_atrasado": 12,
            "requerimientos": [
                "Crear endpoint POST /api/notifications",
                "Soportar notificaciones push y email",
                "Implementar cola de mensajes para envíos masivos",
                "Añadir rate limiting para evitar spam",
                "Documentar en Swagger con ejemplos",
            ]
        },
        {
            "titulo": "Migrar base de datos a PostgreSQL 15",
            "tag": "Base de Datos",
            "emoji": "🗄️",
            "fecha": "15/12/25",
            "dias_atrasado": 15,
            "requerimientos": [
                "Realizar backup completo antes de migración",
                "Actualizar queries incompatibles con PG15",
                "Migrar procedimientos almacenados",
                "Verificar índices y performance",
                "Ejecutar tests de integración post-migración",
            ]
        },
        {
            "titulo": "Actualizar dependencias de seguridad",
            "tag": "DevOps",
            "emoji": "⚙️",
            "fecha": "23/12/25",
            "dias_atrasado": 7,
            "requerimientos": [
                "Actualizar todas las dependencias con vulnerabilidades críticas",
                "Ejecutar npm audit y pip audit",
                "Verificar compatibilidad con versiones actuales",
                "Actualizar lockfiles",
                "Ejecutar suite de tests completa",
            ]
        },
    ]

    def btn_volver_click(e):
        page.snack_bar = ft.SnackBar(ft.Text("Volver atrás"))
        page.snack_bar.open = True
        page.update()

    def btn_buscar_click(e):
        texto_busqueda = input_busqueda.value
        page.snack_bar = ft.SnackBar(ft.Text(f"Buscando: {texto_busqueda}"))
        page.snack_bar.open = True
        page.update()

    # ============ DIALOG DETALLE TAREA ============
    def mostrar_detalle_tarea(tarea):
        requerimientos_list = ft.Column(
            spacing=8,
            controls=[
                ft.Text(f"• {req}", size=12, color="black")
                for req in tarea["requerimientos"]
            ]
        )

        dialog_detalle = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Text(tarea["emoji"], size=28),
                    ft.Text(tarea["titulo"], size=14, weight=ft.FontWeight.BOLD, color="black", expand=True),
                ],
                spacing=10,
            ),
            bgcolor="white",
            content=ft.Container(
                width=320,
                bgcolor="white",
                content=ft.Column(
                    spacing=15,
                    tight=True,
                    controls=[
                        # Info de la tarea
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(
                                    spacing=3,
                                    controls=[
                                        ft.Text("TAG:", size=11, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                        ft.Text(tarea["tag"], size=11, color="black", weight=ft.FontWeight.W_500),
                                    ]
                                ),
                                ft.Row(
                                    spacing=3,
                                    controls=[
                                        ft.Text(
                                            "Atrasado:",
                                            size=11,
                                            color=COLOR_ATRASADO,
                                            weight=ft.FontWeight.W_500,
                                        ),
                                        ft.Text(
                                            f"{tarea['dias_atrasado']} días",
                                            size=11,
                                            color=COLOR_ATRASADO,
                                            weight=ft.FontWeight.W_500,
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text("Fecha límite:", size=11, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                ft.Text(tarea["fecha"], size=11, color="black", weight=ft.FontWeight.W_500),
                            ],
                            spacing=5,
                        ),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        # Requerimientos
                        ft.Text("Requerimientos:", size=13, color="black", weight=ft.FontWeight.BOLD),
                        ft.Container(
                            height=180,
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

    # ============ DIALOG FILTROS ============
    def mostrar_dialog_filtros(e):
        # Radio buttons para orden por fecha
        radio_fecha = ft.RadioGroup(
            value=filtro_orden_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=orden, label=orden, label_style=ft.TextStyle(color="black", size=12)) 
                    for orden in FILTROS_ORDEN
                ],
                spacing=2,
            ),
        )

        def aplicar_filtros(e):
            filtro_orden_actual[0] = radio_fecha.value
            dialog_filtros.open = False
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Filtro aplicado: {filtro_orden_actual[0]}")
            )
            page.snack_bar.open = True
            page.update()

        def limpiar_filtros(e):
            radio_fecha.value = "Más atrasado primero"
            page.update()

        def abrir_filtro_tags(e):
            dialog_filtros.open = False
            page.update()
            mostrar_dialog_tags()

        dialog_filtros = ft.AlertDialog(
            modal=True,
            title=ft.Text("Filtrar tareas", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=350,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        # Ordenar por fecha
                        ft.Text("Ordenar por fecha:", size=13, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                        radio_fecha,
                        ft.Divider(height=10, color=COLOR_BORDE),
                        # Botón para abrir filtro de tags
                        ft.Container(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Filtrar por Tags", size=13, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                                    ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=16, color=COLOR_LABEL),
                                ]
                            ),
                            on_click=abrir_filtro_tags,
                            ink=True,
                            padding=ft.padding.all(10),
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

    # ============ DIALOG TAGS ============
    def mostrar_dialog_tags():
        radio_tags = ft.RadioGroup(
            value=filtro_tag_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=tag, label=tag, label_style=ft.TextStyle(color="black", size=12)) 
                    for tag in FILTROS_TAGS
                ],
                spacing=2,
            ),
        )

        def aplicar_tag(e):
            filtro_tag_actual[0] = radio_tags.value
            dialog_tags.open = False
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Tag seleccionado: {filtro_tag_actual[0]}")
            )
            page.snack_bar.open = True
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
                        content=ft.Text("←", size=20, color="black", weight="bold"),
                        on_click=volver_filtros,
                        ink=True,
                        border_radius=50,
                        padding=5,
                    ),
                    ft.Text("Seleccionar Tag", size=16, weight=ft.FontWeight.BOLD, color="black"),
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

    def crear_tarjeta_tarea(tarea):
        """Crea una tarjeta para cada tarea atrasada"""
        return ft.Container(
            bgcolor="white",
            border_radius=12,
            padding=ft.padding.all(10),
            margin=ft.margin.only(bottom=8),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color=COLOR_SOMBRA_TARJETAS,
                offset=ft.Offset(0, 2),
            ),
            content=ft.Column(
                spacing=4,
                controls=[
                    # Fila 1: Emoji + Título
                    ft.Row(
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(tarea["emoji"], size=24),
                            ft.Text(
                                tarea["titulo"],
                                size=12,
                                color="black",
                                weight=ft.FontWeight.BOLD,
                                expand=True,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ]
                    ),
                    # Fila 2: Tag + Fecha atrasado
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=3,
                                controls=[
                                    ft.Text("TAG:", size=10, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                    ft.Text(tarea["tag"], size=10, color="black", weight=ft.FontWeight.W_500),
                                ]
                            ),
                            ft.Row(
                                spacing=3,
                                controls=[
                                    ft.Text(
                                        "Atrasado desde:",
                                        size=10,
                                        color=COLOR_ATRASADO,
                                        weight=ft.FontWeight.W_500,
                                    ),
                                    ft.Text(
                                        tarea["fecha"],
                                        size=10,
                                        color=COLOR_ATRASADO,
                                        weight=ft.FontWeight.W_500,
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            on_click=lambda e, t=tarea: mostrar_detalle_tarea(t),
            ink=True,
        )

    # Campo de búsqueda
    input_busqueda = ft.TextField(
        hint_text="Buscar por palabras clave...",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=38,
        expand=True,
        content_padding=ft.padding.only(left=10, right=10, top=8, bottom=8),
    )

    # Botón filtrar
    btn_filtrar = ft.Container(
        content=ft.Text("Filtrar por", size=11, color="black"),
        bgcolor="white",
        border=ft.border.all(1, COLOR_BORDE),
        border_radius=5,
        padding=ft.padding.only(left=12, right=12, top=8, bottom=8),
        on_click=mostrar_dialog_filtros,
        ink=True,
    )

    # Botón buscar (icono lupa)
    btn_buscar = ft.Container(
        content=ft.Icon(ft.Icons.SEARCH, size=20, color="white"),
        bgcolor=COLOR_LABEL,
        border_radius=5,
        padding=ft.padding.all(8),
        on_click=btn_buscar_click,
        ink=True,
    )

    # Fila de búsqueda y filtros
    fila_busqueda = ft.Row(
        spacing=8,
        controls=[
            input_busqueda,
            btn_filtrar,
            btn_buscar,
        ]
    )

    # Lista de tareas
    lista_tareas = ft.ListView(
        spacing=0,
        controls=[crear_tarjeta_tarea(tarea) for tarea in TAREAS_ATRASADAS],
        expand=True,
    )

    # Tarjeta blanca principal
    tarjeta_blanca = ft.Container(
        width=400,
        height=720,
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=COLOR_SOMBRA),
        content=ft.Column(
            spacing=0,
            controls=[
                # Flecha de retroceso - bloque compacto
                ft.Container(
                    padding=ft.padding.only(left=15, top=10, bottom=5),
                    alignment=ft.Alignment(-1, 0),
                    content=ft.Container(
                        content=ft.Text("←", size=26, color="black", weight="bold"),
                        on_click=btn_volver_click,
                        ink=True,
                        border_radius=50,
                        padding=3,
                    ),
                ),

                # Header azul
                ft.Container(
                    height=55,
                    width=400,
                    bgcolor=COLOR_HEADER_BG,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("TAREAS ATRASADAS", size=18, weight=ft.FontWeight.BOLD, color="white")
                ),
                
                # Contenido
                ft.Container(
                    padding=ft.padding.only(left=18, right=18, top=15, bottom=15),
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