import flet as ft

def VistaGestionarTrabajadores(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_SOMBRA_TARJETAS = "#30000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_ACTIVO = "#4CAF50"
    COLOR_INACTIVO = "#F44336"
    COLOR_PENDIENTE = "#FF9800"
    COLOR_EDITAR = "#2196F3"
    COLOR_ELIMINAR = "#E53935"
    COLOR_BTN_CREAR = "#4682B4"

    #opciones de filtro
    FILTROS_ESTADO = ["Todos", "Activos", "Inactivos", "Pendientes"]
    FILTROS_PROYECTO = ["Todos", "App Móvil v2.0", "Portal Web Cliente", "API REST Services", "Dashboard Analytics", "Sistema de Pagos", "CRM Interno", "Migración Cloud"]
    FILTROS_ORDEN = [
        "Nombre A-Z",
        "Nombre Z-A",
        "Más reciente",
        "Más antiguo",
        "Por proyecto",
    ]

    filtro_estado_actual = ["Todos"]
    filtro_proyecto_actual = ["Todos"]
    filtro_orden_actual = ["Nombre A-Z"]

    #datos demo de trabajadores
    TRABAJADORES = [
        {
            "nombre": "Ana García",
            "id": "EMP001",
            "email": "ana.garcia@techsolutions.com",
            "proyecto": "App Móvil v2.0",
            "cargo": "Senior Developer",
            "estado": "ACTIVO",
            "fecha_alta": "15/03/2021",
        },
        {
            "nombre": "Carlos López",
            "id": "EMP002",
            "email": "carlos.lopez@techsolutions.com",
            "proyecto": "Portal Web Cliente",
            "cargo": "UX Designer",
            "estado": "ACTIVO",
            "fecha_alta": "22/06/2021",
        },
        {
            "nombre": "María Rodríguez",
            "id": "EMP003",
            "email": "maria.rodriguez@techsolutions.com",
            "proyecto": "API REST Services",
            "cargo": "QA Lead",
            "estado": "ACTIVO",
            "fecha_alta": "10/01/2022",
        },
        {
            "nombre": "Pedro Martínez",
            "id": "EMP004",
            "email": "pedro.martinez@techsolutions.com",
            "proyecto": "Migración Cloud",
            "cargo": "DevOps Engineer",
            "estado": "INACTIVO",
            "fecha_alta": "05/09/2020",
        },
        {
            "nombre": "Laura Sánchez",
            "id": "EMP005",
            "email": "laura.sanchez@techsolutions.com",
            "proyecto": "Dashboard Analytics",
            "cargo": "Backend Lead",
            "estado": "ACTIVO",
            "fecha_alta": "18/04/2022",
        },
        {
            "nombre": "Juan Fernández",
            "id": "EMP006",
            "email": "juan.fernandez@techsolutions.com",
            "proyecto": "Portal Web Cliente",
            "cargo": "Frontend Developer",
            "estado": "PENDIENTE",
            "fecha_alta": "01/12/2024",
        },
        {
            "nombre": "Sofia Ruiz",
            "id": "EMP007",
            "email": "sofia.ruiz@techsolutions.com",
            "proyecto": "CRM Interno",
            "cargo": "Technical Writer",
            "estado": "ACTIVO",
            "fecha_alta": "20/07/2023",
        },
        {
            "nombre": "Diego Torres",
            "id": "EMP008",
            "email": "diego.torres@techsolutions.com",
            "proyecto": "Sistema de Pagos",
            "cargo": "DBA",
            "estado": "INACTIVO",
            "fecha_alta": "12/02/2021",
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

    def btn_crear_trabajador_click(e):
        """Acción al hacer clic en el botón crear trabajador"""
        page.snack_bar = ft.SnackBar(ft.Text("Crear nuevo trabajador"))
        page.snack_bar.open = True
        page.update()

    def btn_gestionar_roles_click(e):
        """Acción al hacer clic en el botón gestionar roles"""
        page.snack_bar = ft.SnackBar(ft.Text("Gestionar roles"))
        page.snack_bar.open = True
        page.update()

    #dialog detalle trabajador
    def mostrar_detalle_trabajador(trabajador):
        """Muestra el diálogo con el detalle del trabajador"""
        estado_color = COLOR_ACTIVO if trabajador["estado"] == "ACTIVO" else (COLOR_INACTIVO if trabajador["estado"] == "INACTIVO" else COLOR_PENDIENTE)
        
        dialog_detalle = ft.AlertDialog(
            modal=True,
            title=ft.Text(trabajador["nombre"], size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=300,
                bgcolor="white",
                content=ft.Column(
                    spacing=12,
                    tight=True,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"ID: {trabajador['id']}", size=12, color=COLOR_LABEL),
                                ft.Container(
                                    bgcolor=estado_color,
                                    border_radius=10,
                                    padding=ft.padding.only(left=10, right=10, top=3, bottom=3),
                                    content=ft.Text(trabajador["estado"], size=10, color="white", weight=ft.FontWeight.BOLD),
                                ),
                            ]
                        ),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Email", size=11, color=COLOR_LABEL),
                            ft.Text(trabajador["email"], size=12, color="black"),
                        ]),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Proyecto", size=11, color=COLOR_LABEL),
                            ft.Text(trabajador["proyecto"], size=12, color="black"),
                        ]),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Cargo", size=11, color=COLOR_LABEL),
                            ft.Text(trabajador["cargo"], size=12, color="black"),
                        ]),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Fecha de alta", size=11, color=COLOR_LABEL),
                            ft.Text(trabajador["fecha_alta"], size=12, color="black"),
                        ]),
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

    #dialog editar trabajador
    def mostrar_editar_trabajador(trabajador):
        """Muestra el diálogo para editar trabajador"""
        def guardar_cambios(e):
            dialog_editar.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"Trabajador {trabajador['nombre']} actualizado"))
            page.snack_bar.open = True
            page.update()

        def cerrar_dialog(e):
            dialog_editar.open = False
            page.update()

        dialog_editar = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Editar: {trabajador['nombre']}", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=300,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    tight=True,
                    controls=[
                        ft.TextField(
                            label="Nombre",
                            value=trabajador["nombre"],
                            text_style=ft.TextStyle(size=12, color="black"),
                            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
                            border_color=COLOR_BORDE,
                            height=50,
                        ),
                        ft.TextField(
                            label="Email",
                            value=trabajador["email"],
                            text_style=ft.TextStyle(size=12, color="black"),
                            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
                            border_color=COLOR_BORDE,
                            height=50,
                        ),
                        ft.TextField(
                            label="Cargo",
                            value=trabajador["cargo"],
                            text_style=ft.TextStyle(size=12, color="black"),
                            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
                            border_color=COLOR_BORDE,
                            height=50,
                        ),
                        ft.DropdownM2(
                            label="Estado",
                            value=trabajador["estado"],
                            text_style=ft.TextStyle(size=12, color="black"),
                            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
                            bgcolor="white",
                            fill_color="white",
                            border_color=COLOR_BORDE,
                            height=50,
                            options=[
                                ft.dropdownm2.Option("ACTIVO"),
                                ft.dropdownm2.Option("INACTIVO"),
                                ft.dropdownm2.Option("PENDIENTE"),
                            ],
                        ),
                    ]
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialog),
                ft.TextButton("Guardar", on_click=guardar_cambios),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_editar)
        dialog_editar.open = True
        page.update()

    #dialog confirmar eliminación
    def mostrar_confirmar_eliminar(trabajador):
        """Muestra el diálogo de confirmación para eliminar trabajador"""
        def confirmar_eliminar(e):
            dialog_confirmar.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"Trabajador {trabajador['nombre']} eliminado"))
            page.snack_bar.open = True
            page.update()

        def cancelar_eliminar(e):
            dialog_confirmar.open = False
            page.update()

        dialog_confirmar = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar trabajador", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=280,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    tight=True,
                    controls=[
                        ft.Text("¿Estás seguro de que deseas eliminar este trabajador?", size=12, color="black"),
                        ft.Container(
                            bgcolor="#FFF3F3",
                            border_radius=8,
                            padding=10,
                            content=ft.Column(
                                spacing=3,
                                controls=[
                                    ft.Text(trabajador["nombre"], size=13, color="black", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"{trabajador['id']} - {trabajador['email']}", size=11, color="#666666"),
                                ],
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
        radio_estado = ft.RadioGroup(
            value=filtro_estado_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=estado, label=estado, label_style=ft.TextStyle(color="black", size=12)) 
                    for estado in FILTROS_ESTADO
                ],
                spacing=2,
            ),
        )

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
            filtro_estado_actual[0] = radio_estado.value
            filtro_orden_actual[0] = radio_orden.value
            dialog_filtros.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"Filtros aplicados"))
            page.snack_bar.open = True
            page.update()

        def limpiar_filtros(e):
            radio_estado.value = "Todos"
            radio_orden.value = "Nombre A-Z"
            page.update()

        def abrir_filtro_proyecto(e):
            dialog_filtros.open = False
            page.update()
            mostrar_dialog_proyecto()

        dialog_filtros = ft.AlertDialog(
            modal=True,
            title=ft.Text("Filtrar trabajadores", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=380,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("Por Estado:", size=13, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                        radio_estado,
                        ft.Divider(height=10, color=COLOR_BORDE),
                        ft.Text("Ordenar por:", size=13, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                        radio_orden,
                        ft.Divider(height=10, color=COLOR_BORDE),
                        ft.Container(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Filtrar por Proyecto", size=13, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                                    ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=16, color=COLOR_LABEL),
                                ]
                            ),
                            on_click=abrir_filtro_proyecto,
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

    #dialog proyecto
    def mostrar_dialog_proyecto():
        """Diálogo para seleccionar filtro por proyecto"""
        radio_proyecto = ft.RadioGroup(
            value=filtro_proyecto_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=proy, label=proy, label_style=ft.TextStyle(color="black", size=12)) 
                    for proy in FILTROS_PROYECTO
                ],
                spacing=2,
            ),
        )

        def aplicar_proyecto(e):
            filtro_proyecto_actual[0] = radio_proyecto.value
            dialog_proyecto.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"Proyecto: {filtro_proyecto_actual[0]}"))
            page.snack_bar.open = True
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
                        content=ft.Text("←", size=20, color="black", weight="bold"),
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

    def crear_tarjeta_trabajador(trabajador):
        """Crea una tarjeta para cada trabajador"""
        estado_color = COLOR_ACTIVO if trabajador["estado"] == "ACTIVO" else (COLOR_INACTIVO if trabajador["estado"] == "INACTIVO" else COLOR_PENDIENTE)
        
        return ft.Container(
            bgcolor="white",
            border_radius=10,
            padding=ft.padding.all(10),
            margin=ft.margin.only(bottom=8),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
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
                            spacing=3,
                            controls=[
                                #fila 1: Nombre + Estado
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(
                                            trabajador["nombre"],
                                            size=12,
                                            color="black",
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Container(
                                            width=10,
                                            height=10,
                                            border_radius=5,
                                            bgcolor=estado_color,
                                        ),
                                    ]
                                ),
                                #fila 2: ID + Proyecto
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(trabajador["id"], size=10, color=COLOR_LABEL),
                                        ft.Text(trabajador["proyecto"], size=10, color="#666666"),
                                    ]
                                ),
                            ]
                        ),
                        on_click=lambda e, t=trabajador: mostrar_detalle_trabajador(t),
                        ink=True,
                    ),
                    #botones de acción
                    ft.Container(
                        content=ft.Icon(ft.Icons.EDIT, size=18, color=COLOR_EDITAR),
                        on_click=lambda e, t=trabajador: mostrar_editar_trabajador(t),
                        ink=True,
                        padding=ft.padding.all(5),
                        border_radius=5,
                    ),
                    ft.Container(
                        content=ft.Icon(ft.Icons.DELETE, size=18, color=COLOR_ELIMINAR),
                        on_click=lambda e, t=trabajador: mostrar_confirmar_eliminar(t),
                        ink=True,
                        padding=ft.padding.all(5),
                        border_radius=5,
                    ),
                ]
            ),
        )

    #botón volver
    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight=ft.FontWeight.BOLD),
        on_click=btn_volver_click,
        ink=True,
        padding=10,
    )

    #campo de búsqueda
    input_busqueda = ft.TextField(
        hint_text="Buscar por nombre...",
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

    #botón buscar
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

    #contador de trabajadores
    contador_trabajadores = ft.Text(f"{len(TRABAJADORES)} trabajadores", size=11, color=COLOR_LABEL)

    #lista de trabajadores
    lista_trabajadores = ft.ListView(
        spacing=0,
        controls=[crear_tarjeta_trabajador(trabajador) for trabajador in TRABAJADORES],
        expand=True,
    )

    #botón crear trabajador
    btn_crear = ft.Container(
        width=160,
        height=40,
        bgcolor=COLOR_BTN_CREAR,
        border_radius=20,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_crear_trabajador_click,
        content=ft.Text("Crear Trabajador", color="white", weight=ft.FontWeight.BOLD, size=12),
    )

    #botón gestionar roles
    btn_roles = ft.Container(
        width=140,
        height=40,
        bgcolor="#6A5ACD",
        border_radius=20,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_gestionar_roles_click,
        content=ft.Text("Gestionar Roles", color="white", weight=ft.FontWeight.BOLD, size=12),
    )

    #tarjeta blanca principal
    tarjeta_blanca = ft.Container(
        width=380,
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color=COLOR_SOMBRA,
            offset=ft.Offset(0, 5),
        ),
        content=ft.Container(
            padding=ft.padding.only(left=18, right=18, top=55, bottom=20),
            content=ft.Column(
                spacing=10,
                controls=[
                    fila_busqueda,
                    contador_trabajadores,
                    ft.Container(
                        height=380,
                        content=lista_trabajadores,
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                        controls=[btn_crear, btn_roles],
                    ),
                ]
            )
        )
    )

    #header flotante
    header_flotante = ft.Container(
        width=300,
        height=50,
        bgcolor=COLOR_HEADER_BG,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            "GESTIONAR TRABAJADORES",
            size=18,
            weight=ft.FontWeight.BOLD,
            color="white"
        )
    )

    #contenido superpuesto (tarjeta + header)
    contenido_superpuesto = ft.Container(
        width=380,
        height=620,
        content=ft.Stack(
            controls=[
                ft.Container(
                    content=tarjeta_blanca,
                    top=30,
                ),
                ft.Container(
                    content=header_flotante,
                    top=0,
                    left=40,
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
        content=ft.Stack(
            expand=True,
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment(0, 0),
                    content=contenido_superpuesto
                ),
                ft.Container(
                    content=btn_volver,
                    top=10,
                    left=10,
                )
            ]
        )
    )


#para probar directamente
def main(page: ft.Page):
    page.title = "App Tareas - Gestionar Trabajadores"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 400
    page.window.min_height = 700
    page.padding = 0 
    
    vista = VistaGestionarTrabajadores(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)