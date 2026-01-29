import flet as ft

def VistaGestionarRoles(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_SOMBRA_TARJETAS = "#30000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_EDITAR = "#2196F3"
    COLOR_ELIMINAR = "#E53935"
    COLOR_BTN_CREAR = "#4682B4"

    #datos demo de roles
    ROLES = [
        {
            "nombre": "Administrador",
            "codigo": "ADMIN",
            "descripcion": "Acceso total al sistema",
            "usuarios": 3,
            "color": "#E53935",
            "permisos": {
                "usuarios": ["crear", "editar", "eliminar", "ver"],
                "tareas": ["crear", "editar", "eliminar", "ver", "asignar"],
                "equipos": ["crear", "editar", "eliminar", "ver"],
                "departamentos": ["crear", "editar", "eliminar", "ver"],
                "configuracion": ["editar", "ver"],
                "estadisticas": ["ver"],
                "auditoria": ["ver"],
            }
        },
        {
            "nombre": "Manager",
            "codigo": "MGR",
            "descripcion": "Gestión de equipos y tareas",
            "usuarios": 8,
            "color": "#FF9800",
            "permisos": {
                "usuarios": ["ver"],
                "tareas": ["crear", "editar", "ver", "asignar"],
                "equipos": ["editar", "ver"],
                "departamentos": ["ver"],
                "configuracion": [],
                "estadisticas": ["ver"],
                "auditoria": [],
            }
        },
        {
            "nombre": "Empleado",
            "codigo": "EMP",
            "descripcion": "Acceso básico a tareas propias",
            "usuarios": 35,
            "color": "#4CAF50",
            "permisos": {
                "usuarios": [],
                "tareas": ["crear", "editar", "ver"],
                "equipos": ["ver"],
                "departamentos": ["ver"],
                "configuracion": [],
                "estadisticas": [],
                "auditoria": [],
            }
        },
        {
            "nombre": "Invitado",
            "codigo": "GUEST",
            "descripcion": "Solo lectura",
            "usuarios": 5,
            "color": "#9E9E9E",
            "permisos": {
                "usuarios": [],
                "tareas": ["ver"],
                "equipos": ["ver"],
                "departamentos": ["ver"],
                "configuracion": [],
                "estadisticas": [],
                "auditoria": [],
            }
        },
    ]

    #lista de todos los permisos posibles
    MODULOS = ["usuarios", "tareas", "equipos", "departamentos", "configuracion", "estadisticas", "auditoria"]
    ACCIONES = ["crear", "editar", "eliminar", "ver", "asignar"]

    def btn_volver_click(e):
        """Acción al hacer clic en el botón volver atrás"""
        page.snack_bar = ft.SnackBar(ft.Text("Volver atrás"))
        page.snack_bar.open = True
        page.update()

    #dialog detalle rol con permisos
    def mostrar_detalle_rol(rol):
        """Muestra el diálogo con el detalle del rol y sus permisos"""
        
        def crear_fila_permisos(modulo: str, permisos_activos: list):
            """Crea una fila mostrando los permisos de un módulo"""
            permisos_chips = []
            for accion in ACCIONES:
                if accion in permisos_activos:
                    permisos_chips.append(
                        ft.Container(
                            bgcolor="#E8F5E9",
                            border_radius=8,
                            padding=ft.padding.only(left=6, right=6, top=2, bottom=2),
                            content=ft.Text(accion, size=9, color="#4CAF50"),
                        )
                    )
            
            if not permisos_chips:
                permisos_chips.append(
                    ft.Text("Sin permisos", size=9, color="#999999", italic=True)
                )
            
            return ft.Container(
                padding=ft.padding.only(top=5, bottom=5),
                border=ft.border.only(bottom=ft.BorderSide(1, COLOR_BORDE)),
                content=ft.Column(
                    spacing=3,
                    controls=[
                        ft.Text(modulo.capitalize(), size=11, color="black", weight=ft.FontWeight.W_500),
                        ft.Row(spacing=5, wrap=True, controls=permisos_chips),
                    ]
                )
            )
        
        lista_permisos = [crear_fila_permisos(modulo, rol["permisos"].get(modulo, [])) for modulo in MODULOS]

        dialog_detalle = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Container(
                        width=12,
                        height=12,
                        border_radius=6,
                        bgcolor=rol["color"],
                    ),
                    ft.Text(rol["nombre"], size=16, weight=ft.FontWeight.BOLD, color="black"),
                    ft.Text(f"({rol['codigo']})", size=12, color=COLOR_LABEL),
                ],
                spacing=8,
            ),
            bgcolor="white",
            content=ft.Container(
                width=320,
                height=350,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Text(rol["descripcion"], size=12, color="#666666"),
                        ft.Text(f"👥 {rol['usuarios']} usuarios asignados", size=11, color=COLOR_LABEL),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        ft.Text("Permisos por módulo:", size=12, color="black", weight=ft.FontWeight.BOLD),
                        ft.Container(
                            height=220,
                            content=ft.ListView(controls=lista_permisos, spacing=0),
                        ),
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

    #dialog editar rol
    def mostrar_editar_rol(rol):
        """Muestra el diálogo para editar rol"""
        
        #crear checkboxes para cada permiso
        permisos_checkboxes = {}
        
        def crear_seccion_modulo(modulo: str):
            permisos_activos = rol["permisos"].get(modulo, [])
            checkboxes = []
            for accion in ACCIONES:
                cb = ft.Checkbox(
                    label=accion.capitalize(),
                    value=accion in permisos_activos,
                    label_style=ft.TextStyle(size=11, color="black"),
                )
                checkboxes.append(cb)
                permisos_checkboxes[f"{modulo}_{accion}"] = cb
            
            return ft.Container(
                padding=ft.padding.only(top=5, bottom=5),
                content=ft.Column(
                    spacing=3,
                    controls=[
                        ft.Text(modulo.capitalize(), size=11, color=COLOR_LABEL, weight=ft.FontWeight.BOLD),
                        ft.Row(spacing=5, wrap=True, controls=checkboxes),
                    ]
                )
            )
        
        secciones_modulos = [crear_seccion_modulo(modulo) for modulo in MODULOS]
        
        def guardar_cambios(e):
            dialog_editar.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"Rol '{rol['nombre']}' actualizado"))
            page.snack_bar.open = True
            page.update()

        def cerrar(e):
            dialog_editar.open = False
            page.update()

        dialog_editar = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Editar: {rol['nombre']}", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=340,
                height=400,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.TextField(
                            label="Nombre del rol",
                            value=rol["nombre"],
                            text_style=ft.TextStyle(size=12, color="black"),
                            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
                            border_color=COLOR_BORDE,
                            height=50,
                        ),
                        ft.TextField(
                            label="Descripción",
                            value=rol["descripcion"],
                            text_style=ft.TextStyle(size=12, color="black"),
                            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
                            border_color=COLOR_BORDE,
                            height=50,
                        ),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        ft.Text("Permisos:", size=12, color="black", weight=ft.FontWeight.BOLD),
                        *secciones_modulos,
                    ]
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar),
                ft.TextButton("Guardar", on_click=guardar_cambios),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_editar)
        dialog_editar.open = True
        page.update()

    #dialog confirmar eliminación
    def mostrar_confirmar_eliminar(rol):
        """Muestra el diálogo de confirmación para eliminar rol"""
        def confirmar_eliminar(e):
            dialog_confirmar.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"Rol '{rol['nombre']}' eliminado"))
            page.snack_bar.open = True
            page.update()

        def cancelar_eliminar(e):
            dialog_confirmar.open = False
            page.update()

        dialog_confirmar = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar rol", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=280,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    tight=True,
                    controls=[
                        ft.Text("¿Estás seguro de que deseas eliminar este rol?", size=12, color="black"),
                        ft.Container(
                            bgcolor="#FFF3F3",
                            border_radius=8,
                            padding=10,
                            content=ft.Row(
                                controls=[
                                    ft.Container(width=10, height=10, border_radius=5, bgcolor=rol["color"]),
                                    ft.Text(rol["nombre"], size=12, color="black", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"({rol['usuarios']} usuarios)", size=11, color="#666666"),
                                ],
                                spacing=8,
                            ),
                        ),
                        ft.Text("Los usuarios con este rol perderán sus permisos.", size=11, color=COLOR_ELIMINAR, italic=True),
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

    #dialog crear nuevo rol
    def mostrar_crear_rol(e):
        """Muestra el diálogo para crear un nuevo rol"""
        
        permisos_checkboxes = {}
        
        def crear_seccion_modulo(modulo: str):
            checkboxes = []
            for accion in ACCIONES:
                cb = ft.Checkbox(
                    label=accion.capitalize(),
                    value=False,
                    label_style=ft.TextStyle(size=11, color="black"),
                )
                checkboxes.append(cb)
                permisos_checkboxes[f"{modulo}_{accion}"] = cb
            
            return ft.Container(
                padding=ft.padding.only(top=5, bottom=5),
                content=ft.Column(
                    spacing=3,
                    controls=[
                        ft.Text(modulo.capitalize(), size=11, color=COLOR_LABEL, weight=ft.FontWeight.BOLD),
                        ft.Row(spacing=5, wrap=True, controls=checkboxes),
                    ]
                )
            )
        
        secciones_modulos = [crear_seccion_modulo(modulo) for modulo in MODULOS]
        
        input_nombre = ft.TextField(
            label="Nombre del rol",
            hint_text="Ej: Supervisor",
            text_style=ft.TextStyle(size=12, color="black"),
            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
            border_color=COLOR_BORDE,
            height=50,
        )
        
        input_codigo = ft.TextField(
            label="Código",
            hint_text="Ej: SUP",
            text_style=ft.TextStyle(size=12, color="black"),
            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
            border_color=COLOR_BORDE,
            height=50,
        )
        
        input_descripcion = ft.TextField(
            label="Descripción",
            hint_text="Descripción del rol...",
            text_style=ft.TextStyle(size=12, color="black"),
            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
            border_color=COLOR_BORDE,
            height=50,
        )
        
        def crear_rol(e):
            if not input_nombre.value:
                page.snack_bar = ft.SnackBar(ft.Text("Por favor, introduce un nombre"))
                page.snack_bar.open = True
                page.update()
                return
            dialog_crear.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"Rol '{input_nombre.value}' creado"))
            page.snack_bar.open = True
            page.update()

        def cerrar(e):
            dialog_crear.open = False
            page.update()

        dialog_crear = ft.AlertDialog(
            modal=True,
            title=ft.Text("Crear Nuevo Rol", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=340,
                height=420,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        input_nombre,
                        input_codigo,
                        input_descripcion,
                        ft.Divider(height=1, color=COLOR_BORDE),
                        ft.Text("Permisos:", size=12, color="black", weight=ft.FontWeight.BOLD),
                        *secciones_modulos,
                    ]
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar),
                ft.TextButton("Crear", on_click=crear_rol),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_crear)
        dialog_crear.open = True
        page.update()

    def cerrar_dialog(dialog):
        dialog.open = False
        page.update()

    def crear_tarjeta_rol(rol):
        """Crea una tarjeta para cada rol"""
        return ft.Container(
            bgcolor="white",
            border_radius=10,
            padding=ft.padding.all(12),
            margin=ft.margin.only(bottom=10),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=COLOR_SOMBRA_TARJETAS,
                offset=ft.Offset(0, 2),
            ),
            content=ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    #indicador de color
                    ft.Container(
                        width=8,
                        height=50,
                        border_radius=4,
                        bgcolor=rol["color"],
                    ),
                    #contenido principal (clickeable)
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            spacing=3,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(rol["nombre"], size=13, color="black", weight=ft.FontWeight.BOLD),
                                        ft.Container(
                                            bgcolor=COLOR_LABEL,
                                            border_radius=8,
                                            padding=ft.padding.only(left=8, right=8, top=2, bottom=2),
                                            content=ft.Text(rol["codigo"], size=9, color="white"),
                                        ),
                                    ]
                                ),
                                ft.Text(rol["descripcion"], size=10, color="#666666", max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(f"👥 {rol['usuarios']} usuarios", size=10, color=COLOR_LABEL),
                            ]
                        ),
                        on_click=lambda e, r=rol: mostrar_detalle_rol(r),
                        ink=True,
                    ),
                    #botones de acción
                    ft.Container(
                        content=ft.Icon(ft.Icons.EDIT, size=18, color=COLOR_EDITAR),
                        on_click=lambda e, r=rol: mostrar_editar_rol(r),
                        ink=True,
                        padding=ft.padding.all(5),
                        border_radius=5,
                    ),
                    ft.Container(
                        content=ft.Icon(ft.Icons.DELETE, size=18, color=COLOR_ELIMINAR),
                        on_click=lambda e, r=rol: mostrar_confirmar_eliminar(r),
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

    #contador de roles
    contador_roles = ft.Text(f"{len(ROLES)} roles configurados", size=11, color=COLOR_LABEL)

    #lista de roles
    lista_roles = ft.ListView(
        spacing=0,
        controls=[crear_tarjeta_rol(rol) for rol in ROLES],
        expand=True,
    )

    #botón crear nuevo rol
    btn_crear = ft.Container(
        width=160,
        height=44,
        bgcolor=COLOR_BTN_CREAR,
        border_radius=22,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=mostrar_crear_rol,
        content=ft.Text("Crear Rol", color="white", weight=ft.FontWeight.BOLD, size=14),
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
                spacing=12,
                controls=[
                    contador_roles,
                    ft.Container(
                        height=420,
                        content=lista_roles,
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
        width=240,
        height=50,
        bgcolor=COLOR_HEADER_BG,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            "GESTIONAR ROLES",
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
                    left=70,
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
    page.title = "App Tareas - Gestionar Roles"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 400
    page.window.min_height = 700
    page.padding = 0 
    
    vista = VistaGestionarRoles(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)