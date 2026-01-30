import flet as ft

def VistaGestionarProyectos(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_SOMBRA_TARJETAS = "#30000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_ACTIVO = "#4CAF50"
    COLOR_INACTIVO = "#F44336"
    COLOR_EN_CREACION = "#FF9800"
    COLOR_EDITAR = "#2196F3"
    COLOR_ELIMINAR = "#E53935"
    COLOR_BTN_CREAR = "#4682B4"

    #opciones de filtro
    FILTROS_ESTADO = ["Todos", "Activos", "Inactivos", "En creación"]
    FILTROS_CLIENTE = ["Todos", "TechCorp S.A.", "Innovatech Ltd.", "GlobalMedia", "FinanceHub", "StartupXYZ", "Interno"]
    FILTROS_ORDEN = [
        "Nombre A-Z",
        "Nombre Z-A",
        "Más reciente",
        "Más antiguo",
        "Por cliente",
    ]

    filtro_estado_actual = ["Todos"]
    filtro_cliente_actual = ["Todos"]
    filtro_orden_actual = ["Nombre A-Z"]

    #datos demo de proyectos
    PROYECTOS = [
        {
            "nombre": "App Móvil v2.0",
            "codigo": "PRY001",
            "responsable": "Ana García",
            "cliente": "TechCorp S.A.",
            "presupuesto": "45.000 €",
            "estado": "ACTIVO",
            "fecha_inicio": "15/01/2024",
            "fecha_fin": "30/06/2025",
        },
        {
            "nombre": "Portal Web Cliente",
            "codigo": "PRY002",
            "responsable": "Carlos López",
            "cliente": "Innovatech Ltd.",
            "presupuesto": "32.000 €",
            "estado": "ACTIVO",
            "fecha_inicio": "01/03/2024",
            "fecha_fin": "15/09/2025",
        },
        {
            "nombre": "API REST Services",
            "codigo": "PRY003",
            "responsable": "María Rodríguez",
            "cliente": "Interno",
            "presupuesto": "18.500 €",
            "estado": "ACTIVO",
            "fecha_inicio": "10/06/2024",
            "fecha_fin": "20/12/2025",
        },
        {
            "nombre": "Dashboard Analytics",
            "codigo": "PRY004",
            "responsable": "Pedro Martínez",
            "cliente": "GlobalMedia",
            "presupuesto": "28.000 €",
            "estado": "EN CREACIÓN",
            "fecha_inicio": "01/02/2025",
            "fecha_fin": "30/08/2025",
        },
        {
            "nombre": "Sistema de Pagos",
            "codigo": "PRY005",
            "responsable": "Laura Sánchez",
            "cliente": "FinanceHub",
            "presupuesto": "55.000 €",
            "estado": "ACTIVO",
            "fecha_inicio": "20/09/2023",
            "fecha_fin": "15/03/2025",
        },
        {
            "nombre": "CRM Interno",
            "codigo": "PRY006",
            "responsable": "Juan Fernández",
            "cliente": "Interno",
            "presupuesto": "22.000 €",
            "estado": "INACTIVO",
            "fecha_inicio": "05/01/2022",
            "fecha_fin": "30/12/2023",
        },
        {
            "nombre": "Migración Cloud",
            "codigo": "PRY007",
            "responsable": "Sofia Ruiz",
            "cliente": "StartupXYZ",
            "presupuesto": "38.000 €",
            "estado": "ACTIVO",
            "fecha_inicio": "01/11/2024",
            "fecha_fin": "30/04/2025",
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

    def btn_crear_proyecto_click(e):
        """Acción al hacer clic en el botón crear proyecto"""
        page.snack_bar = ft.SnackBar(ft.Text("Crear nuevo proyecto"))
        page.snack_bar.open = True
        page.update()

    #dialog detalle proyecto
    def mostrar_detalle_proyecto(proyecto):
        """Muestra el diálogo con el detalle del proyecto"""
        estado_color = COLOR_ACTIVO if proyecto["estado"] == "ACTIVO" else (COLOR_INACTIVO if proyecto["estado"] == "INACTIVO" else COLOR_EN_CREACION)
        
        dialog_detalle = ft.AlertDialog(
            modal=True,
            title=ft.Text(proyecto["nombre"], size=16, weight=ft.FontWeight.BOLD, color="black"),
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
                                ft.Text(f"Código: {proyecto['codigo']}", size=12, color=COLOR_LABEL),
                                ft.Container(
                                    bgcolor=estado_color,
                                    border_radius=10,
                                    padding=ft.padding.only(left=10, right=10, top=3, bottom=3),
                                    content=ft.Text(proyecto["estado"], size=10, color="white", weight=ft.FontWeight.BOLD),
                                ),
                            ]
                        ),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Responsable", size=11, color=COLOR_LABEL),
                            ft.Text(proyecto["responsable"], size=12, color="black"),
                        ]),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Cliente", size=11, color=COLOR_LABEL),
                            ft.Text(proyecto["cliente"], size=12, color="black"),
                        ]),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Presupuesto", size=11, color=COLOR_LABEL),
                            ft.Text(proyecto["presupuesto"], size=12, color="black"),
                        ]),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(spacing=2, controls=[
                                    ft.Text("Fecha inicio", size=11, color=COLOR_LABEL),
                                    ft.Text(proyecto["fecha_inicio"], size=12, color="black"),
                                ]),
                                ft.Column(spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END, controls=[
                                    ft.Text("Fecha fin", size=11, color=COLOR_LABEL),
                                    ft.Text(proyecto["fecha_fin"], size=12, color="black"),
                                ]),
                            ]
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

    #dialog editar proyecto
    def mostrar_editar_proyecto(proyecto):
        """Muestra el diálogo para editar proyecto"""
        def guardar_cambios(e):
            dialog_editar.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"Proyecto {proyecto['nombre']} actualizado"))
            page.snack_bar.open = True
            page.update()

        def cerrar_dialog(e):
            dialog_editar.open = False
            page.update()

        dialog_editar = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Editar: {proyecto['nombre']}", size=16, weight=ft.FontWeight.BOLD, color="black"),
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
                            value=proyecto["nombre"],
                            text_style=ft.TextStyle(size=12, color="black"),
                            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
                            border_color=COLOR_BORDE,
                            height=50,
                        ),
                        ft.TextField(
                            label="Responsable",
                            value=proyecto["responsable"],
                            text_style=ft.TextStyle(size=12, color="black"),
                            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
                            border_color=COLOR_BORDE,
                            height=50,
                        ),
                        ft.TextField(
                            label="Cliente",
                            value=proyecto["cliente"],
                            text_style=ft.TextStyle(size=12, color="black"),
                            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
                            border_color=COLOR_BORDE,
                            height=50,
                        ),
                        ft.TextField(
                            label="Presupuesto",
                            value=proyecto["presupuesto"],
                            text_style=ft.TextStyle(size=12, color="black"),
                            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
                            border_color=COLOR_BORDE,
                            height=50,
                        ),
                        ft.DropdownM2(
                            label="Estado",
                            value=proyecto["estado"],
                            text_style=ft.TextStyle(size=12, color="black"),
                            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
                            bgcolor="white",
                            fill_color="white",
                            border_color=COLOR_BORDE,
                            height=50,
                            options=[
                                ft.dropdownm2.Option("ACTIVO"),
                                ft.dropdownm2.Option("INACTIVO"),
                                ft.dropdownm2.Option("EN CREACIÓN"),
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
    def mostrar_confirmar_eliminar(proyecto):
        """Muestra el diálogo de confirmación para eliminar proyecto"""
        def confirmar_eliminar(e):
            dialog_confirmar.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"Proyecto {proyecto['nombre']} eliminado"))
            page.snack_bar.open = True
            page.update()

        def cancelar_eliminar(e):
            dialog_confirmar.open = False
            page.update()

        dialog_confirmar = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar proyecto", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=280,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    tight=True,
                    controls=[
                        ft.Text("¿Estás seguro de que deseas eliminar este proyecto?", size=12, color="black"),
                        ft.Container(
                            bgcolor="#FFF3F3",
                            border_radius=8,
                            padding=10,
                            content=ft.Column(
                                spacing=3,
                                controls=[
                                    ft.Text(proyecto["nombre"], size=13, color="black", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"{proyecto['codigo']} - {proyecto['cliente']}", size=11, color="#666666"),
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

        def abrir_filtro_cliente(e):
            dialog_filtros.open = False
            page.update()
            mostrar_dialog_cliente()

        dialog_filtros = ft.AlertDialog(
            modal=True,
            title=ft.Text("Filtrar proyectos", size=16, weight=ft.FontWeight.BOLD, color="black"),
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
                                    ft.Text("Filtrar por Cliente", size=13, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                                    ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=16, color=COLOR_LABEL),
                                ]
                            ),
                            on_click=abrir_filtro_cliente,
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

    #dialog cliente
    def mostrar_dialog_cliente():
        """Diálogo para seleccionar filtro por cliente"""
        radio_cliente = ft.RadioGroup(
            value=filtro_cliente_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=cli, label=cli, label_style=ft.TextStyle(color="black", size=12)) 
                    for cli in FILTROS_CLIENTE
                ],
                spacing=2,
            ),
        )

        def aplicar_cliente(e):
            filtro_cliente_actual[0] = radio_cliente.value
            dialog_cliente.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"Cliente: {filtro_cliente_actual[0]}"))
            page.snack_bar.open = True
            page.update()

        def volver_filtros(e):
            dialog_cliente.open = False
            page.update()
            mostrar_dialog_filtros(None)

        dialog_cliente = ft.AlertDialog(
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
                    ft.Text("Seleccionar Cliente", size=14, weight=ft.FontWeight.BOLD, color="black"),
                ],
                spacing=10,
            ),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=280,
                bgcolor="white",
                content=ft.ListView(
                    controls=[radio_cliente],
                    spacing=5,
                ),
            ),
            actions=[
                ft.TextButton("Aplicar", on_click=aplicar_cliente),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_cliente)
        dialog_cliente.open = True
        page.update()

    def crear_tarjeta_proyecto(proyecto):
        """Crea una tarjeta para cada proyecto"""
        estado_color = COLOR_ACTIVO if proyecto["estado"] == "ACTIVO" else (COLOR_INACTIVO if proyecto["estado"] == "INACTIVO" else COLOR_EN_CREACION)
        
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
                                            proyecto["nombre"],
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
                                #fila 2: Código + Cliente
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(proyecto["codigo"], size=10, color=COLOR_LABEL),
                                        ft.Text(proyecto["cliente"], size=10, color="#666666"),
                                    ]
                                ),
                            ]
                        ),
                        on_click=lambda e, p=proyecto: mostrar_detalle_proyecto(p),
                        ink=True,
                    ),
                    #botones de acción
                    ft.Container(
                        content=ft.Icon(ft.Icons.EDIT, size=18, color=COLOR_EDITAR),
                        on_click=lambda e, p=proyecto: mostrar_editar_proyecto(p),
                        ink=True,
                        padding=ft.padding.all(5),
                        border_radius=5,
                    ),
                    ft.Container(
                        content=ft.Icon(ft.Icons.DELETE, size=18, color=COLOR_ELIMINAR),
                        on_click=lambda e, p=proyecto: mostrar_confirmar_eliminar(p),
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

    #contador de proyectos
    contador_proyectos = ft.Text(f"{len(PROYECTOS)} proyectos", size=11, color=COLOR_LABEL)

    #lista de proyectos
    lista_proyectos = ft.ListView(
        spacing=0,
        controls=[crear_tarjeta_proyecto(proyecto) for proyecto in PROYECTOS],
        expand=True,
    )

    #botón crear proyecto
    btn_crear = ft.Container(
        width=170,
        height=44,
        bgcolor=COLOR_BTN_CREAR,
        border_radius=22,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_crear_proyecto_click,
        content=ft.Text("Crear Proyecto", color="white", weight=ft.FontWeight.BOLD, size=13),
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
                    contador_proyectos,
                    ft.Container(
                        height=390,
                        content=lista_proyectos,
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[btn_crear],
                    ),
                ]
            )
        )
    )

    #header flotante
    header_flotante = ft.Container(
        width=280,
        height=50,
        bgcolor=COLOR_HEADER_BG,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            "GESTIONAR PROYECTOS",
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
                    left=50,
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
    page.title = "App Tareas - Gestionar Proyectos"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 400
    page.window.min_height = 700
    page.padding = 0 
    
    vista = VistaGestionarProyectos(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)