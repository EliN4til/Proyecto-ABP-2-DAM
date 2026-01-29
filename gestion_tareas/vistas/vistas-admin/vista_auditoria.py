import flet as ft

def VistaAuditoria(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_SOMBRA_TARJETAS = "#30000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    
    #colores para tipos de acción
    COLOR_CREAR = "#4CAF50"
    COLOR_EDITAR = "#2196F3"
    COLOR_ELIMINAR = "#E53935"
    COLOR_LOGIN = "#9C27B0"
    COLOR_CONFIG = "#FF9800"

    #opciones de filtro
    FILTROS_TIPO = ["Todos", "Crear", "Editar", "Eliminar", "Login", "Configuración"]
    FILTROS_MODULO = ["Todos", "Usuarios", "Tareas", "Equipos", "Departamentos", "Roles", "Sistema"]
    FILTROS_PERIODO = ["Hoy", "Últimos 7 días", "Últimos 30 días", "Este mes", "Todos"]

    filtro_tipo_actual = ["Todos"]
    filtro_modulo_actual = ["Todos"]
    filtro_periodo_actual = ["Últimos 7 días"]

    #datos demo de registros de auditoría
    REGISTROS = [
        {
            "accion": "Crear",
            "modulo": "Usuarios",
            "descripcion": "Nuevo usuario creado: Juan Fernández (EMP006)",
            "usuario": "Ana García",
            "fecha": "29/01/26",
            "hora": "14:32",
            "ip": "192.168.1.45",
        },
        {
            "accion": "Editar",
            "modulo": "Tareas",
            "descripcion": "Tarea actualizada: Arreglar bug UpdateDate.py",
            "usuario": "Carlos López",
            "fecha": "29/01/26",
            "hora": "12:15",
            "ip": "192.168.1.78",
        },
        {
            "accion": "Login",
            "modulo": "Sistema",
            "descripcion": "Inicio de sesión exitoso",
            "usuario": "María Rodríguez",
            "fecha": "29/01/26",
            "hora": "09:00",
            "ip": "192.168.1.102",
        },
        {
            "accion": "Eliminar",
            "modulo": "Tareas",
            "descripcion": "Tarea eliminada: Revisar documentación antigua",
            "usuario": "Pedro Martínez",
            "fecha": "28/01/26",
            "hora": "17:45",
            "ip": "192.168.1.33",
        },
        {
            "accion": "Configuración",
            "modulo": "Sistema",
            "descripcion": "Configuración actualizada: Tiempo de sesión cambiado a 2 horas",
            "usuario": "Ana García",
            "fecha": "28/01/26",
            "hora": "11:20",
            "ip": "192.168.1.45",
        },
        {
            "accion": "Crear",
            "modulo": "Equipos",
            "descripcion": "Nuevo equipo creado: Data Analytics Team",
            "usuario": "Ana García",
            "fecha": "27/01/26",
            "hora": "16:00",
            "ip": "192.168.1.45",
        },
        {
            "accion": "Editar",
            "modulo": "Usuarios",
            "descripcion": "Usuario actualizado: Pedro Martínez - Estado cambiado a INACTIVO",
            "usuario": "Ana García",
            "fecha": "27/01/26",
            "hora": "10:30",
            "ip": "192.168.1.45",
        },
        {
            "accion": "Login",
            "modulo": "Sistema",
            "descripcion": "Intento de login fallido (3 intentos)",
            "usuario": "usuario_desconocido",
            "fecha": "26/01/26",
            "hora": "23:15",
            "ip": "203.45.67.89",
        },
        {
            "accion": "Crear",
            "modulo": "Departamentos",
            "descripcion": "Nuevo departamento creado: Innovación",
            "usuario": "Ana García",
            "fecha": "26/01/26",
            "hora": "14:00",
            "ip": "192.168.1.45",
        },
        {
            "accion": "Editar",
            "modulo": "Roles",
            "descripcion": "Rol actualizado: Manager - Añadido permiso de estadísticas",
            "usuario": "Ana García",
            "fecha": "25/01/26",
            "hora": "09:45",
            "ip": "192.168.1.45",
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

    def get_color_accion(accion: str) -> str:
        """Devuelve el color según el tipo de acción"""
        colores = {
            "Crear": COLOR_CREAR,
            "Editar": COLOR_EDITAR,
            "Eliminar": COLOR_ELIMINAR,
            "Login": COLOR_LOGIN,
            "Configuración": COLOR_CONFIG,
        }
        return colores.get(accion, COLOR_LABEL)

    def get_icono_accion(accion: str) -> str:
        """Devuelve el icono según el tipo de acción"""
        iconos = {
            "Crear": "➕",
            "Editar": "✏️",
            "Eliminar": "🗑️",
            "Login": "🔐",
            "Configuración": "⚙️",
        }
        return iconos.get(accion, "📋")

    #dialog detalle registro
    def mostrar_detalle_registro(registro):
        """Muestra el diálogo con el detalle del registro"""
        color_accion = get_color_accion(registro["accion"])
        icono_accion = get_icono_accion(registro["accion"])
        
        dialog_detalle = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Text(icono_accion, size=20),
                    ft.Container(
                        bgcolor=color_accion,
                        border_radius=8,
                        padding=ft.padding.only(left=8, right=8, top=2, bottom=2),
                        content=ft.Text(registro["accion"], size=11, color="white", weight=ft.FontWeight.BOLD),
                    ),
                    ft.Text(registro["modulo"], size=14, color=COLOR_LABEL),
                ],
                spacing=8,
            ),
            bgcolor="white",
            content=ft.Container(
                width=320,
                bgcolor="white",
                content=ft.Column(
                    spacing=12,
                    tight=True,
                    controls=[
                        ft.Column(spacing=2, controls=[
                            ft.Text("Descripción", size=11, color=COLOR_LABEL),
                            ft.Text(registro["descripcion"], size=12, color="black"),
                        ]),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(spacing=2, controls=[
                                    ft.Text("Usuario", size=11, color=COLOR_LABEL),
                                    ft.Text(registro["usuario"], size=12, color="black"),
                                ]),
                                ft.Column(spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END, controls=[
                                    ft.Text("Fecha y hora", size=11, color=COLOR_LABEL),
                                    ft.Text(f"{registro['fecha']} {registro['hora']}", size=12, color="black"),
                                ]),
                            ]
                        ),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Dirección IP", size=11, color=COLOR_LABEL),
                            ft.Text(registro["ip"], size=12, color="black"),
                        ]),
                    ]
                ),
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog(dialog_detalle)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_detalle)
        dialog_detalle.open = True
        page.update()

    def cerrar_dialog(dialog):
        dialog.open = False
        page.update()

    #dialog filtros
    def mostrar_dialog_filtros(e):
        """Muestra el diálogo de filtros"""
        radio_tipo = ft.RadioGroup(
            value=filtro_tipo_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=tipo, label=tipo, label_style=ft.TextStyle(color="black", size=12)) 
                    for tipo in FILTROS_TIPO
                ],
                spacing=2,
            ),
        )

        radio_periodo = ft.RadioGroup(
            value=filtro_periodo_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=periodo, label=periodo, label_style=ft.TextStyle(color="black", size=12)) 
                    for periodo in FILTROS_PERIODO
                ],
                spacing=2,
            ),
        )

        def aplicar_filtros(e):
            filtro_tipo_actual[0] = radio_tipo.value
            filtro_periodo_actual[0] = radio_periodo.value
            dialog_filtros.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"Filtros aplicados"))
            page.snack_bar.open = True
            page.update()

        def limpiar_filtros(e):
            radio_tipo.value = "Todos"
            radio_periodo.value = "Últimos 7 días"
            page.update()

        def abrir_filtro_modulo(e):
            dialog_filtros.open = False
            page.update()
            mostrar_dialog_modulo()

        dialog_filtros = ft.AlertDialog(
            modal=True,
            title=ft.Text("Filtrar registros", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=400,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("Por Tipo de Acción:", size=13, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                        radio_tipo,
                        ft.Divider(height=10, color=COLOR_BORDE),
                        ft.Text("Por Período:", size=13, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                        radio_periodo,
                        ft.Divider(height=10, color=COLOR_BORDE),
                        ft.Container(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Filtrar por Módulo", size=13, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                                    ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=16, color=COLOR_LABEL),
                                ]
                            ),
                            on_click=abrir_filtro_modulo,
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

    #dialog módulo
    def mostrar_dialog_modulo():
        """Diálogo para seleccionar filtro por módulo"""
        radio_modulo = ft.RadioGroup(
            value=filtro_modulo_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=modulo, label=modulo, label_style=ft.TextStyle(color="black", size=12)) 
                    for modulo in FILTROS_MODULO
                ],
                spacing=2,
            ),
        )

        def aplicar_modulo(e):
            filtro_modulo_actual[0] = radio_modulo.value
            dialog_modulo.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"Módulo: {filtro_modulo_actual[0]}"))
            page.snack_bar.open = True
            page.update()

        def volver_filtros(e):
            dialog_modulo.open = False
            page.update()
            mostrar_dialog_filtros(None)

        dialog_modulo = ft.AlertDialog(
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
                    ft.Text("Seleccionar Módulo", size=14, weight=ft.FontWeight.BOLD, color="black"),
                ],
                spacing=10,
            ),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=280,
                bgcolor="white",
                content=ft.ListView(
                    controls=[radio_modulo],
                    spacing=5,
                ),
            ),
            actions=[
                ft.TextButton("Aplicar", on_click=aplicar_modulo),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_modulo)
        dialog_modulo.open = True
        page.update()

    def crear_tarjeta_registro(registro):
        """Crea una tarjeta para cada registro de auditoría"""
        color_accion = get_color_accion(registro["accion"])
        icono_accion = get_icono_accion(registro["accion"])
        
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
            on_click=lambda e, r=registro: mostrar_detalle_registro(r),
            ink=True,
            content=ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    #icono y badge
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=3,
                        controls=[
                            ft.Text(icono_accion, size=18),
                            ft.Container(
                                bgcolor=color_accion,
                                border_radius=6,
                                padding=ft.padding.only(left=5, right=5, top=1, bottom=1),
                                content=ft.Text(registro["accion"][:4], size=8, color="white", weight=ft.FontWeight.BOLD),
                            ),
                        ]
                    ),
                    #contenido principal
                    ft.Column(
                        expand=True,
                        spacing=2,
                        controls=[
                            ft.Text(
                                registro["descripcion"], 
                                size=11, 
                                color="black", 
                                weight=ft.FontWeight.W_500,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(f"👤 {registro['usuario']}", size=9, color="#666666"),
                                    ft.Text(f"{registro['fecha']} {registro['hora']}", size=9, color=COLOR_LABEL),
                                ]
                            ),
                        ]
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
        hint_text="Buscar en registros...",
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

    #contador de registros
    contador_registros = ft.Text(f"{len(REGISTROS)} registros encontrados", size=11, color=COLOR_LABEL)

    #lista de registros
    lista_registros = ft.ListView(
        spacing=0,
        controls=[crear_tarjeta_registro(registro) for registro in REGISTROS],
        expand=True,
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
                    contador_registros,
                    ft.Container(
                        height=450,
                        content=lista_registros,
                    ),
                ]
            )
        )
    )

    #header flotante
    header_flotante = ft.Container(
        width=200,
        height=50,
        bgcolor=COLOR_HEADER_BG,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            "AUDITORÍA",
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
                    left=90,
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
    page.title = "App Tareas - Auditoría"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 400
    page.window.min_height = 700
    page.padding = 0 
    
    vista = VistaAuditoria(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)