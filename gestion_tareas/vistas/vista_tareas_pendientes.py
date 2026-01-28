import flet as ft

def VistaTareasPendientes(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_SOMBRA_TARJETAS = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_ELIMINAR = "#E53935"
    COLOR_BTN_ANADIR = "#4682B4"

    #opciones de filtro
    FILTROS_TAGS = ["Todos", "Desarrollo", "Bug Fix", "Testing", "Diseño", "Documentación", "DevOps", "Base de Datos", "API", "Frontend", "Backend"]
    FILTROS_ORDEN = [
        "Más reciente primero", 
        "Más antiguo primero", 
        "Fecha ascendente (antigua → reciente)",
        "Fecha descendente (reciente → antigua)",
        "Alfabético A-Z", 
        "Alfabético Z-A",
        "Por prioridad alta",
        "Por prioridad baja",
    ]

    filtro_tag_actual = ["Todos"]
    filtro_orden_actual = ["Más reciente primero"]

    #datos demo de tareas pendientes (con requerimientos y rango de fechas)
    TAREAS_PENDIENTES = [
        {
            "titulo": "Arreglar bug linea 287 fichero UpdateDate.py",
            "tag": "Desarrollo",
            "emoji": "👨‍💻",
            "fecha_inicio": "25/12/25",
            "fecha_fin": "31/12/25",
            "requerimientos": [
                "Identificar el error en la línea 287 del fichero UpdateDate.py",
                "El bucle debe iterar correctamente sobre la lista de fechas",
                "Validar que no se produzcan excepciones de tipo IndexError",
                "Añadir logs para seguimiento del proceso",
                "Realizar pruebas con datos de producción simulados",
            ]
        },
        {
            "titulo": "Implementar autenticación OAuth2",
            "tag": "Backend",
            "emoji": "🔧",
            "fecha_inicio": "26/12/25",
            "fecha_fin": "05/01/26",
            "requerimientos": [
                "Configurar cliente OAuth2 con Google y GitHub",
                "Implementar flujo de autorización",
                "Guardar tokens de acceso de forma segura",
                "Manejar refresh de tokens automático",
                "Añadir tests de integración",
            ]
        },
        {
            "titulo": "Diseñar mockups para dashboard",
            "tag": "Diseño",
            "emoji": "🎨",
            "fecha_inicio": "27/12/25",
            "fecha_fin": "03/01/26",
            "requerimientos": [
                "Crear diseño responsive para desktop y móvil",
                "Incluir gráficos de rendimiento y métricas KPI",
                "Usar la paleta de colores corporativa",
                "Diseñar estados vacíos y de error",
                "Exportar en formato Figma y PNG",
            ]
        },
        {
            "titulo": "Escribir tests unitarios módulo Auth",
            "tag": "Testing",
            "emoji": "🧪",
            "fecha_inicio": "28/12/25",
            "fecha_fin": "08/01/26",
            "requerimientos": [
                "Cobertura mínima del 80% en el módulo de autenticación",
                "Testear login, logout y refresh de tokens",
                "Incluir tests para casos de error y edge cases",
                "Mockear las llamadas a servicios externos",
                "Documentar los tests con descripciones claras",
            ]
        },
        {
            "titulo": "Configurar pipeline CI/CD",
            "tag": "DevOps",
            "emoji": "⚙️",
            "fecha_inicio": "29/12/25",
            "fecha_fin": "10/01/26",
            "requerimientos": [
                "Configurar GitHub Actions para build automático",
                "Añadir etapa de tests automatizados",
                "Configurar deploy automático a staging",
                "Implementar notificaciones en Slack",
                "Documentar el proceso de deployment",
            ]
        },
        {
            "titulo": "Documentar API endpoints v2",
            "tag": "Documentación",
            "emoji": "📝",
            "fecha_inicio": "30/12/25",
            "fecha_fin": "15/01/26",
            "requerimientos": [
                "Documentar todos los endpoints del API v2 en Swagger",
                "Incluir ejemplos de request y response",
                "Describir códigos de error y sus significados",
                "Añadir sección de autenticación y autorización",
                "Revisar y actualizar la documentación existente",
            ]
        },
    ]

    def btn_volver_click(e):
        """Acción al hacer clic en el botón volver atrás"""
        page.snack_bar = ft.SnackBar(ft.Text("Volver atrás"))
        page.snack_bar.open = True
        page.update()

    def btn_buscar_click(e):
        """Acción al hacer clic en el botón buscar"""
        texto_busqueda = input_busqueda.value
        page.snack_bar = ft.SnackBar(ft.Text(f"Buscando: {texto_busqueda}"))
        page.snack_bar.open = True
        page.update()

    def btn_anadir_click(e):
        """Acción al hacer clic en el botón añadir tarea"""
        page.snack_bar = ft.SnackBar(ft.Text("Añadir nueva tarea"))
        page.snack_bar.open = True
        page.update()

    #dialog detalle tarea
    def mostrar_detalle_tarea(tarea):
        """Muestra el diálogo con el detalle de la tarea"""
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
                        #info de la tarea
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
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(
                                    spacing=3,
                                    controls=[
                                        ft.Text("Inicio:", size=11, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                        ft.Text(tarea["fecha_inicio"], size=11, color="black", weight=ft.FontWeight.W_500),
                                    ]
                                ),
                                ft.Row(
                                    spacing=3,
                                    controls=[
                                        ft.Text("Fin:", size=11, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                        ft.Text(tarea["fecha_fin"], size=11, color="black", weight=ft.FontWeight.W_500),
                                    ]
                                ),
                            ]
                        ),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        #requerimientos
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

    #dialog confirmar eliminación
    def mostrar_confirmar_eliminar(tarea):
        """Muestra el diálogo de confirmación para eliminar tarea"""
        def confirmar_eliminar(e):
            dialog_confirmar.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"Tarea eliminada: {tarea['titulo'][:30]}..."))
            page.snack_bar.open = True
            page.update()

        def cancelar_eliminar(e):
            dialog_confirmar.open = False
            page.update()

        dialog_confirmar = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar tarea", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=280,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    tight=True,
                    controls=[
                        ft.Text("¿Estás seguro de que deseas eliminar esta tarea?", size=13, color="black"),
                        ft.Container(
                            bgcolor="#FFF3F3",
                            border_radius=8,
                            padding=10,
                            content=ft.Row(
                                controls=[
                                    ft.Text(tarea["emoji"], size=20),
                                    ft.Text(tarea["titulo"], size=12, color="black", expand=True, max_lines=2),
                                ],
                                spacing=8,
                            ),
                        ),
                        ft.Text("Esta acción no se puede deshacer.", size=11, color=COLOR_ELIMINAR, italic=True),
                    ]
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_eliminar),
                ft.TextButton("Eliminar", on_click=confirmar_eliminar, style=ft.ButtonStyle(color=COLOR_ELIMINAR)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_confirmar)
        dialog_confirmar.open = True
        page.update()

    #dialog filtros
    def mostrar_dialog_filtros(e):
        """Muestra el diálogo de filtros"""
        #radio buttons para orden por fecha
        radio_orden = ft.RadioGroup(
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
            """Aplicar filtros seleccionados"""
            filtro_orden_actual[0] = radio_orden.value
            dialog_filtros.open = False
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Filtro aplicado: {filtro_orden_actual[0]}")
            )
            page.snack_bar.open = True
            page.update()

        def limpiar_filtros(e):
            """Limpiar filtros a valores por defecto"""
            radio_orden.value = "Más reciente primero"
            page.update()

        def abrir_filtro_tags(e):
            """Abrir diálogo de filtro por tags"""
            dialog_filtros.open = False
            page.update()
            mostrar_dialog_tags()

        dialog_filtros = ft.AlertDialog(
            modal=True,
            title=ft.Text("Filtrar tareas", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=380,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        #ordenar por fecha
                        ft.Text("Ordenar por:", size=13, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                        radio_orden,
                        ft.Divider(height=10, color=COLOR_BORDE),
                        #botón para abrir filtro de tags
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

    #dialog tags
    def mostrar_dialog_tags():
        """Diálogo para seleccionar filtro por tag"""
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
            """Aplicar filtro por tag"""
            filtro_tag_actual[0] = radio_tags.value
            dialog_tags.open = False
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Tag seleccionado: {filtro_tag_actual[0]}")
            )
            page.snack_bar.open = True
            page.update()

        def volver_filtros(e):
            """Volver al diálogo de filtros"""
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
        """Crea una tarjeta para cada tarea pendiente"""
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
            content=ft.Row(
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    #contenido principal (clickeable)
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            spacing=4,
                            controls=[
                                #fila 1: Emoji + Título
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
                                #fila 2: Tag + Fecha rango
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
                                                    "Fecha:",
                                                    size=10,
                                                    color=COLOR_LABEL,
                                                    weight=ft.FontWeight.W_500,
                                                ),
                                                ft.Text(
                                                    f"{tarea['fecha_inicio']} - {tarea['fecha_fin']}",
                                                    size=10,
                                                    color="black",
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
                    ),
                    #botón X para eliminar
                    ft.Container(
                        content=ft.Text("X", size=16, color=COLOR_ELIMINAR, weight=ft.FontWeight.BOLD),
                        on_click=lambda e, t=tarea: mostrar_confirmar_eliminar(t),
                        ink=True,
                        padding=ft.padding.all(8),
                        border_radius=5,
                    ),
                ]
            ),
        )

    #campo de búsqueda
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

    #botón filtrar
    btn_filtrar = ft.Container(
        content=ft.Text("Filtrar por", size=11, color="black"),
        bgcolor="white",
        border=ft.border.all(1, COLOR_BORDE),
        border_radius=5,
        padding=ft.padding.only(left=12, right=12, top=8, bottom=8),
        on_click=mostrar_dialog_filtros,
        ink=True,
    )

    #botón buscar (icono lupa)
    btn_buscar = ft.Container(
        content=ft.Icon(ft.Icons.SEARCH, size=20, color="white"),
        bgcolor=COLOR_LABEL,
        border_radius=5,
        padding=ft.padding.all(8),
        on_click=btn_buscar_click,
        ink=True,
    )

    #fila de búsqueda y filtros
    fila_busqueda = ft.Row(
        spacing=8,
        controls=[
            input_busqueda,
            btn_filtrar,
            btn_buscar,
        ]
    )

    #lista de tareas
    lista_tareas = ft.ListView(
        spacing=0,
        controls=[crear_tarjeta_tarea(tarea) for tarea in TAREAS_PENDIENTES],
        expand=True,
    )

    #botón añadir tarea
    btn_anadir = ft.Container(
        width=160,
        height=44,
        bgcolor=COLOR_BTN_ANADIR,
        border_radius=22,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_anadir_click,
        content=ft.Text("Añadir Tarea", color="white", weight=ft.FontWeight.BOLD, size=14),
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
                #flecha de retroceso - bloque compacto
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

                #header azul
                ft.Container(
                    height=55,
                    width=400,
                    bgcolor=COLOR_HEADER_BG,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("TAREAS PENDIENTES", size=18, weight=ft.FontWeight.BOLD, color="white")
                ),
                
                #contenido
                ft.Container(
                    padding=ft.padding.only(left=18, right=18, top=15, bottom=15),
                    expand=True,
                    content=ft.Column(
                        spacing=12,
                        expand=True,
                        controls=[
                            fila_busqueda,
                            lista_tareas,
                            #botón añadir centrado
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[btn_anadir]
                            ),
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