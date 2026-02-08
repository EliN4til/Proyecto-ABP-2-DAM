import flet as ft
from modelos.crud import obtener_todos_roles, crear_rol, actualizar_rol, eliminar_rol

def VistaGestionarRoles(page):
    
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

    # Variable para almacenar los roles cargados de la base de datos
    roles_db = []

    #lista de todos los permisos posibles
    MODULOS = ["usuarios", "tareas", "equipos", "departamentos", "configuracion", "estadisticas", "auditoria"]
    ACCIONES = ["crear", "editar", "eliminar", "ver", "asignar"]

    # --- LÓGICA DE CARGA DE DATOS ---

    def cargar_roles_real():
        """Obtiene los roles desde la base de datos MongoDB"""
        exito, resultado = obtener_todos_roles()
        if exito:
            return resultado
        return []

    def refrescar_lista_ui():
        """Recarga los datos de la BD y actualiza los controles de la lista"""
        nonlocal roles_db
        roles_db = cargar_roles_real()
        
        lista_roles.controls = []
        if not roles_db:
            lista_roles.controls.append(
                ft.Container(
                    padding=20,
                    content=ft.Text("No hay roles configurados", color="grey", text_align="center")
                )
            )
        else:
            for rol in roles_db:
                lista_roles.controls.append(crear_tarjeta_rol(rol))
        
        texto_contador.value = f"{len(roles_db)} roles configurados"
        page.update()

    async def btn_volver_click(e):
        """Acción al hacer clic en el botón volver atrás - CORREGIDO A ADMIN"""
        await page.push_route("/area_admin")

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

    # --- DIÁLOGOS CRUD ---

    #dialog detalle rol simplificado
    def mostrar_detalle_rol(rol):
        """Muestra el diálogo con el detalle del rol"""
        
        dialog_detalle = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Row(
                controls=[
                    ft.Container(
                        width=12,
                        height=12,
                        border_radius=6,
                        bgcolor=rol.get("color", "#4682B4"),
                    ),
                    ft.Text(rol["nombre"], size=16, weight=ft.FontWeight.BOLD, color="black"),
                    ft.Text(f"({rol['codigo']})", size=12, color=COLOR_LABEL),
                ],
                spacing=8,
            ),
            content=ft.Container(
                width=320,
                height=150,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Text(rol.get("descripcion", "Sin descripción"), size=12, color="#666666"),
                        ft.Text(f"👥 {rol.get('usuarios', 0)} usuarios asignados", size=11, color=COLOR_LABEL),
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

    #dialog editar rol simplificado
    def mostrar_editar_rol(rol):
        """Muestra el diálogo para editar rol persistente"""
        
        input_nombre = ft.TextField(label="Nombre del rol", value=rol["nombre"], border_color=COLOR_BORDE, height=50, text_size=13)
        input_desc = ft.TextField(label="Descripción", value=rol.get("descripcion", ""), border_color=COLOR_BORDE, height=50, text_size=13)

        def guardar_cambios_click(e):
            datos_actualizados = {
                "nombre": input_nombre.value,
                "descripcion": input_desc.value,
            }

            # 2. Llamada al CRUD
            exito, msj = actualizar_rol(rol["_id"], datos_actualizados)
            if exito:
                mostrar_mensaje_dialog(page, "✅ Éxito", f"Rol '{input_nombre.value}' actualizado", "green")
                dialog_editar.open = False
                refrescar_lista_ui()
            else:
                mostrar_mensaje_dialog(page, "❌ Error", f"Error: {msj}", "red")
            
            page.update()

        dialog_editar = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text(f"Editar: {rol['nombre']}", size=16, weight=ft.FontWeight.BOLD, color="black"),
            content=ft.Container(
                width=340, height=200,
                content=ft.Column(
                    spacing=10,
                    controls=[
                        input_nombre,
                        input_desc,
                    ]
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialog(dialog_editar)),
                ft.FilledButton("Guardar", bgcolor=COLOR_BTN_CREAR, color="white", on_click=guardar_cambios_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_editar)
        dialog_editar.open = True
        page.update()

    #dialog confirmar eliminación
    def mostrar_confirmar_eliminar(rol):
        """Muestra el diálogo de confirmación para eliminar rol real"""
        def confirmar_eliminar(e):
            exito, msj = eliminar_rol(rol["_id"])
            if exito:
                mostrar_mensaje_dialog(page, "✅ Éxito", f"Rol '{rol['nombre']}' eliminado", "green")
                dialog_confirmar.open = False
                refrescar_lista_ui()
            else:
                mostrar_mensaje_dialog(page, "❌ Error", f"Error: {msj}", "red")
            
            page.update()

        dialog_confirmar = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text("Eliminar rol", size=16, weight=ft.FontWeight.BOLD, color="black"),
            content=ft.Container(
                width=280,
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
                                    ft.Container(width=10, height=10, border_radius=5, bgcolor=rol.get("color", "red")),
                                    ft.Text(rol["nombre"], size=12, color="black", weight=ft.FontWeight.BOLD),
                                ],
                                spacing=8,
                            ),
                        ),
                        ft.Text("Los usuarios con este rol perderán sus permisos.", size=11, color=COLOR_ELIMINAR, italic=True),
                    ]
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialog(dialog_confirmar)),
                ft.TextButton("Eliminar", on_click=confirmar_eliminar, style=ft.ButtonStyle(color=COLOR_ELIMINAR)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_confirmar)
        dialog_confirmar.open = True
        page.update()

    #dialog crear nuevo rol simplificado
    def mostrar_crear_rol(e):
        """Muestra el diálogo para crear un nuevo rol en la base de datos"""
        
        input_nombre = ft.TextField(label="Nombre del rol", hint_text="Ej: Supervisor", border_color=COLOR_BORDE, height=50, text_size=13)
        input_codigo = ft.TextField(label="Código", hint_text="Ej: SUP", border_color=COLOR_BORDE, height=50, text_size=13)
        input_descripcion = ft.TextField(label="Descripción", hint_text="Descripción corta...", border_color=COLOR_BORDE, height=50, text_size=13)
        
        def crear_rol_confirmar(e):
            if not input_nombre.value or not input_codigo.value:
                mostrar_mensaje_dialog(page, "⚠️ Campos obligatorios", "❌ Nombre y Código son obligatorios", "red")
                page.update()
                return

            nuevo_rol_data = {
                "nombre": input_nombre.value,
                "codigo": input_codigo.value.upper(),
                "descripcion": input_descripcion.value,
                "usuarios": 0,
                "color": "#4682B4", # Color por defecto
                "permisos": {} # Sin permisos detallados
            }

            exito, msj = crear_rol(nuevo_rol_data)
            if exito:
                mostrar_mensaje_dialog(page, "✅ Éxito", f"Rol '{input_nombre.value}' creado con éxito", "green")
                dialog_crear.open = False
                refrescar_lista_ui()
            else:
                mostrar_mensaje_dialog(page, "❌ Error", f"Error: {msj}", "red")
            
            page.update()

        dialog_crear = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text("Crear Nuevo Rol", size=16, weight=ft.FontWeight.BOLD, color="black"),
            content=ft.Container(
                width=340, height=280,
                content=ft.Column(
                    spacing=10,
                    controls=[
                        input_nombre, input_codigo, input_descripcion,
                    ]
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialog(dialog_crear)),
                ft.FilledButton("Crear", bgcolor=COLOR_BTN_CREAR, color="white", on_click=crear_rol_confirmar),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_crear)
        dialog_crear.open = True
        page.update()

    def cerrar_dialog(dialog):
        dialog.open = False
        page.update()

    # --- RENDERIZADO DE TARJETAS ---

    def crear_tarjeta_rol(rol):
        """Crea una tarjeta visual para cada rol"""
        return ft.Container(
            bgcolor="white",
            border_radius=10,
            padding=12,
            margin=ft.Margin(bottom=10, left=0, right=0, top=0),
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
                        bgcolor=rol.get("color", "#4682B4"),
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
                                            padding=ft.Padding(left=8, right=8, top=2, bottom=2),
                                            content=ft.Text(rol.get("codigo", "ROL"), size=9, color="white"),
                                        ),
                                    ]
                                ),
                                ft.Text(rol.get("descripcion", ""), size=10, color="#666666", max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(f"👥 {rol.get('usuarios', 0)} usuarios", size=10, color=COLOR_LABEL),
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
                        padding=5,
                        border_radius=5,
                    ),
                    ft.Container(
                        content=ft.Icon(ft.Icons.DELETE, size=18, color=COLOR_ELIMINAR),
                        on_click=lambda e, r=rol: mostrar_confirmar_eliminar(r),
                        ink=True,
                        padding=5,
                        border_radius=5,
                    ),
                ]
            ),
        )

    # --- ELEMENTOS FIJOS DE LA PÁGINA ---

    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight=ft.FontWeight.BOLD),
        on_click=btn_volver_click,
        ink=True,
        padding=10,
    )

    texto_contador = ft.Text("0 roles configurados", size=11, color=COLOR_LABEL)

    lista_roles = ft.ListView(
        spacing=0,
        expand=True,
    )

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
            padding=ft.Padding(left=18, right=18, top=55, bottom=20),
            content=ft.Column(
                spacing=12,
                controls=[
                    texto_contador,
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

    # --- INICIALIZACIÓN ---
    refrescar_lista_ui()

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
def main(page):
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