import flet as ft

def VistaMisProyectos(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_SOMBRA_TARJETAS = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_BADGE_DEP = "#E3F2FD"
    COLOR_TEXT_DEP = "#1565C0"
    
    # Colores para estados de tareas
    COLOR_PENDIENTE = "#FF9800"
    COLOR_REALIZADA = "#4CAF50"
    COLOR_ATRASADA = "#E53935"

    #opciones de filtro
    FILTROS_ESTADO = ["Todos", "En Progreso", "Pausado", "Finalizado"]
    FILTROS_ORDEN = ["Nombre A-Z", "Nombre Z-A"]

    filtro_estado_actual = ["Todos"]
    filtro_orden_actual = ["Nombre A-Z"]

    #datos demo de proyectos asignados al usuario (Ahora con lista de tareas demo)
    PROYECTOS_USER = [
        {
            "nombre": "App Móvil v2.0",
            "descripcion": "Rediseño completo de la aplicación móvil para iOS y Android con Flutter.",
            "mis_departamentos": ["Desarrollo", "Mobile"],
            "rol": "Lead Developer",
            "estado": "En Progreso",
            "tareas_pendientes": 3,
            "equipo": ["Ana García", "Laura Sánchez", "Pedro Martínez"],
            "fecha_inicio": "01/11/25",
            "fecha_fin": "01/03/26",
            "emoji": "📱",
            "lista_tareas": [
                {"titulo": "Configurar entorno Flutter", "estado": "Realizada", "prioridad": "Alta"},
                {"titulo": "Diseñar pantalla Login", "estado": "Realizada", "prioridad": "Media"},
                {"titulo": "Integrar API de usuarios", "estado": "Pendiente", "prioridad": "Alta"},
                {"titulo": "Corregir bug de navegación", "estado": "Atrasada", "prioridad": "Alta"},
                {"titulo": "Tests unitarios módulo Home", "estado": "Pendiente", "prioridad": "Media"},
            ]
        },
        {
            "nombre": "Portal Web Cliente",
            "descripcion": "Portal de autogestión para clientes corporativos.",
            "mis_departamentos": ["Backend", "API"],
            "rol": "Backend Dev",
            "estado": "En Progreso",
            "tareas_pendientes": 5,
            "equipo": ["Carlos López", "Sofia Ruiz", "Diego Torres"],
            "fecha_inicio": "15/12/25",
            "fecha_fin": "30/04/26",
            "emoji": "💻",
            "lista_tareas": [
                {"titulo": "Crear endpoints de facturación", "estado": "Pendiente", "prioridad": "Alta"},
                {"titulo": "Documentar API en Swagger", "estado": "Pendiente", "prioridad": "Baja"},
            ]
        },
        {
            "nombre": "Migración Cloud",
            "descripcion": "Migración de infraestructura on-premise a AWS.",
            "mis_departamentos": ["DevOps"],
            "rol": "Consultor",
            "estado": "Pausado",
            "tareas_pendientes": 1,
            "equipo": ["Pedro Martínez", "Juan Fernández"],
            "fecha_inicio": "01/01/26",
            "fecha_fin": "01/06/26",
            "emoji": "☁️",
            "lista_tareas": [
                {"titulo": "Configurar VPC", "estado": "Realizada", "prioridad": "Alta"},
                {"titulo": "Migrar base de datos", "estado": "Pendiente", "prioridad": "Alta"},
            ]
        },
        {
            "nombre": "Sistema de Pagos",
            "descripcion": "Integración con pasarela de pagos Stripe y PayPal.",
            "mis_departamentos": ["Desarrollo", "Seguridad"],
            "rol": "Developer",
            "estado": "En Progreso",
            "tareas_pendientes": 0,
            "equipo": ["Ana García", "María Rodríguez"],
            "fecha_inicio": "10/10/25",
            "fecha_fin": "15/01/26",
            "emoji": "💳",
            "lista_tareas": [
                {"titulo": "Investigación API Stripe", "estado": "Realizada", "prioridad": "Media"},
                {"titulo": "Implementar Webhooks", "estado": "Realizada", "prioridad": "Alta"},
            ]
        },
    ]

    def btn_volver_click(e):
        page.snack_bar = ft.SnackBar(ft.Text("Volver atrás"))
        page.snack_bar.open = True
        page.update()

    def btn_buscar_click(e):
        texto_busqueda = input_busqueda.value
        page.snack_bar = ft.SnackBar(ft.Text(f"Buscando proyecto: {texto_busqueda}"))
        page.snack_bar.open = True
        page.update()

    # Nuevo: Dialog para ver las tareas específicas del proyecto
    def mostrar_tareas_del_proyecto(proyecto):
        
        def get_icon_color(estado):
            if estado == "Realizada": return COLOR_REALIZADA
            if estado == "Atrasada": return COLOR_ATRASADA
            return COLOR_PENDIENTE

        def get_icon(estado):
            if estado == "Realizada": return ft.Icons.CHECK_CIRCLE
            if estado == "Atrasada": return ft.Icons.WARNING_AMBER
            return ft.Icons.ACCESS_TIME_FILLED

        items_tareas = []
        if not proyecto["lista_tareas"]:
            items_tareas.append(ft.Text("No tienes tareas asignadas en este proyecto.", size=12, color="grey"))
        else:
            for tarea in proyecto["lista_tareas"]:
                item = ft.Container(
                    padding=10,
                    border=ft.border.only(bottom=ft.border.BorderSide(1, "#F0F0F0")),
                    content=ft.Row(
                        controls=[
                            ft.Icon(get_icon(tarea["estado"]), size=18, color=get_icon_color(tarea["estado"])),
                            ft.Column(
                                spacing=2,
                                expand=True,
                                controls=[
                                    ft.Text(tarea["titulo"], size=12, weight=ft.FontWeight.W_500, color="black"),
                                    ft.Text(f"Estado: {tarea['estado']} • Prioridad: {tarea['prioridad']}", size=10, color="grey"),
                                ]
                            )
                        ]
                    )
                )
                items_tareas.append(item)

        dialog_tareas = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Tareas en {proyecto['nombre']}", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=350,
                height=400,
                bgcolor="white",
                content=ft.ListView(
                    controls=items_tareas,
                    spacing=0,
                )
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog_tareas(dialog_tareas)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        def cerrar_dialog_tareas(dlg):
            dlg.open = False
            page.update()

        page.overlay.append(dialog_tareas)
        dialog_tareas.open = True
        page.update()

    # Dialog detalle proyecto (Modificado: Sin progreso y botón arreglado)
    def mostrar_detalle_proyecto(proyecto):
        
        #crear avatares (circulitos) para el equipo
        avatares_equipo = ft.Row(
            spacing=-10, 
            controls=[
                ft.Container(
                    width=30, height=30, bgcolor="#BBDEFB", border_radius=15,
                    border=ft.border.all(2, "white"),
                    alignment=ft.Alignment(0,0),
                    content=ft.Text(miembro[0], size=12, color="black", weight="bold"),
                    tooltip=miembro
                ) for miembro in proyecto["equipo"]
            ]
        )

        mis_deptos_chips = ft.Row(
            wrap=True,
            spacing=5,
            run_spacing=5,
            controls=[
                ft.Container(
                    bgcolor=COLOR_BADGE_DEP,
                    border_radius=15,
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                    content=ft.Text(dep, size=10, color=COLOR_TEXT_DEP, weight=ft.FontWeight.W_500),
                ) for dep in proyecto["mis_departamentos"]
            ]
        )

        def abrir_tareas_desde_detalle(e):
            # Cerramos el detalle actual para abrir el de tareas, o podríamos superponerlo
            # Aquí lo superponemos
            mostrar_tareas_del_proyecto(proyecto)

        def cerrar_dialog(dialog):
            dialog.open = False
            page.update()

        dialog_detalle = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Text(proyecto["emoji"], size=28),
                    ft.Text(proyecto["nombre"], size=16, weight=ft.FontWeight.BOLD, color="black", expand=True),
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
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        #estado y fechas
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Container(
                                    bgcolor="#E8F5E9" if proyecto["estado"] == "En Progreso" else "#FFF3E0",
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                    border_radius=8,
                                    content=ft.Text(proyecto["estado"], size=10, color="black", weight="bold")
                                ),
                                ft.Text(f"{proyecto['fecha_inicio']} - {proyecto['fecha_fin']}", size=10, color="#666666")
                            ]
                        ),
                        #descripcion
                        ft.Text(proyecto["descripcion"], size=12, color="black"),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        
                        #seccion mi rol
                        ft.Text("Mi participación:", size=11, color=COLOR_LABEL, weight="bold"),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(spacing=2, controls=[
                                    ft.Text("Rol", size=10, color="#666666"),
                                    ft.Text(proyecto["rol"], size=11, color="black", weight="bold"),
                                ]),
                                ft.Column(spacing=2, controls=[
                                    ft.Text("Departamentos", size=10, color="#666666"),
                                    mis_deptos_chips,
                                ]),
                            ]
                        ),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        
                        #seccion equipo
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Equipo:", size=11, color=COLOR_LABEL, weight="bold"),
                                avatares_equipo
                            ]
                        ),
                    ]
                ),
            ),
            actions=[
                ft.TextButton("Ver Tareas", on_click=abrir_tareas_desde_detalle),
                ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog(dialog_detalle)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_detalle)
        dialog_detalle.open = True
        page.update()

    #dialog filtros
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

        radio_estado = ft.RadioGroup(
            value=filtro_estado_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=est, label=est, label_style=ft.TextStyle(size=11, color="black")) 
                    for est in FILTROS_ESTADO
                ],
                spacing=2,
            ),
        )

        def aplicar_filtros(e):
            filtro_orden_actual[0] = radio_orden.value
            filtro_estado_actual[0] = radio_estado.value
            dialog_filtros.open = False
            page.snack_bar = ft.SnackBar(ft.Text("Filtros aplicados"))
            page.snack_bar.open = True
            page.update()

        def limpiar_filtros(e):
            radio_orden.value = "Nombre A-Z"
            radio_estado.value = "Todos"
            page.update()

        dialog_filtros = ft.AlertDialog(
            modal=True,
            title=ft.Text("Filtrar proyectos", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=350,
                bgcolor="white",
                content=ft.Column(
                    spacing=8,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("Por Estado:", size=12, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                        radio_estado,
                        ft.Divider(height=8, color=COLOR_BORDE),
                        ft.Text("Ordenar por:", size=12, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                        radio_orden,
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

    def crear_tarjeta_proyecto(proyecto):
        """Crea una tarjeta visual para cada proyecto (Sin barra de progreso)"""
        
        #chips para los departamentos donde trabaja el usuario
        chips_deptos = ft.Row(
            wrap=True,
            spacing=4,
            run_spacing=4,
            controls=[
                ft.Container(
                    bgcolor=COLOR_BADGE_DEP,
                    border_radius=10,
                    padding=ft.padding.symmetric(horizontal=6, vertical=2),
                    content=ft.Text(dep, size=9, color=COLOR_TEXT_DEP, weight=ft.FontWeight.BOLD),
                ) for dep in proyecto["mis_departamentos"]
            ]
        )

        return ft.Container(
            bgcolor="white",
            border_radius=12,
            padding=ft.padding.all(12),
            margin=ft.margin.only(bottom=10),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color=COLOR_SOMBRA_TARJETAS,
                offset=ft.Offset(0, 2),
            ),
            content=ft.Column(
                spacing=6,
                controls=[
                    #fila 1: Emoji + Titulo + Estado (punto)
                    ft.Row(
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=40, height=40, bgcolor="#F5F5F5", border_radius=8,
                                alignment=ft.Alignment(0,0),
                                content=ft.Text(proyecto["emoji"], size=20)
                            ),
                            ft.Column(
                                spacing=0,
                                expand=True,
                                controls=[
                                    ft.Text(proyecto["nombre"], size=13, weight=ft.FontWeight.BOLD, color="black"),
                                    ft.Text(proyecto["rol"], size=10, color="#666666"),
                                ]
                            ),
                            #indicador visual de estado
                            ft.Container(
                                width=10, height=10, border_radius=5,
                                bgcolor="#4CAF50" if proyecto["estado"] == "En Progreso" else "#FFC107",
                                tooltip=proyecto["estado"]
                            )
                        ]
                    ),
                    ft.Divider(height=1, color="#F0F0F0"),
                    
                    #fila 2: Departamentos (Label + Chips)
                    ft.Column(
                        spacing=3,
                        controls=[
                            ft.Text("Mis Departamentos:", size=9, color=COLOR_LABEL, weight="bold"),
                            chips_deptos
                        ]
                    ),
                    
                    ft.Container(height=2), #espaciador
                    
                    #fila 3: Solo tareas pendientes
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.Container(
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                bgcolor="#F5F5F5",
                                border_radius=12,
                                content=ft.Row(
                                    spacing=3,
                                    controls=[
                                        ft.Icon(ft.Icons.LIST_ALT, size=12, color=COLOR_LABEL),
                                        ft.Text(f"{proyecto['tareas_pendientes']} tareas", size=10, color=COLOR_LABEL, weight="bold"),
                                    ]
                                )
                            )
                        ]
                    )
                ]
            ),
            on_click=lambda e, p=proyecto: mostrar_detalle_proyecto(p),
            ink=True,
        )

    #campo de búsqueda
    input_busqueda = ft.TextField(
        hint_text="Buscar proyectos...",
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
        content=ft.Text("Filtrar", size=11, color="black"),
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

    #lista de proyectos
    lista_proyectos = ft.ListView(
        spacing=0,
        controls=[crear_tarjeta_proyecto(p) for p in PROYECTOS_USER],
        expand=True,
        padding=ft.padding.only(bottom=20)
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
                #flecha de retroceso
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
                    content=ft.Text("MIS PROYECTOS", size=18, weight=ft.FontWeight.BOLD, color="white")
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
                            lista_proyectos,
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

def main(page: ft.Page):
    page.title = "App Tareas - Mis Proyectos"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 380
    page.window.min_height = 780
    page.padding = 0 
    
    vista = VistaMisProyectos(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)