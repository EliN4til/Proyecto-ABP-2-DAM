import flet as ft
from servicios.sesion_service import obtener_usuario, obtener_contexto
from modelos.crud import cambiar_contrasenya

def VistaMisDatos(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_BTN_PASS = "#4682B4"

    #obtenemos los datos del usuario de la sesión
    usuario_sesion = obtener_usuario()
    
    #si hay sesión activa, cogemos los datos del usuario
    if usuario_sesion:
        id_usuario = usuario_sesion.get("_id")
        nombre = usuario_sesion.get("nombre", "Usuario")
        apellidos = usuario_sesion.get("apellidos", "")
        estado = usuario_sesion.get("estado", "ACTIVO")
        identificador = usuario_sesion.get("identificador", "N/A")
        empresa = usuario_sesion.get("empresa", "N/A")
        equipo = usuario_sesion.get("equipo", "N/A")
        cargo = usuario_sesion.get("cargo", "N/A")
        id_empleado = usuario_sesion.get("id_empleado", "N/A")
        correo = usuario_sesion.get("email", "N/A")
        telefono = usuario_sesion.get("telefono", "N/A")
        ubicacion = usuario_sesion.get("ubicacion", "N/A")
        
        #el departamento es un objeto con nombre y ubicacion
        departamento = usuario_sesion.get("departamento", {})
        if departamento:
            if isinstance(departamento, dict):
                nombre_depto = departamento.get("nombre", "N/A")
            else:
                nombre_depto = str(departamento)
        else:
            nombre_depto = "N/A"
        
        #la fecha de incorporacion viene como objeto, la convertimos a string
        fecha_incorporacion_raw = usuario_sesion.get("fecha_incorporacion", None)
        if fecha_incorporacion_raw:
            if isinstance(fecha_incorporacion_raw, str):
                fecha_incorporacion = fecha_incorporacion_raw
            else:
                fecha_incorporacion = str(fecha_incorporacion_raw)[:10]
        else:
            fecha_incorporacion = "N/A"
        
        foto_url = usuario_sesion.get("foto", None)
    else:
        #si no hay una sesión, ponemos valores por defecto
        id_usuario = None
        nombre = "Usuario"
        apellidos = ""
        estado = "ACTIVO"
        identificador = "N/A"
        empresa = "N/A"
        equipo = "N/A"
        cargo = "N/A"
        id_empleado = "N/A"
        correo = "N/A"
        telefono = "N/A"
        ubicacion = "N/A"
        nombre_depto = "N/A"
        fecha_incorporacion = "N/A"
        foto_url = None

    # --- LÓGICA DE CAMBIO DE CONTRASEÑA ---

    def mostrar_dialog_cambio_pass(e):
        #muestra el diálogo para cambiar la contraseña
        
        input_actual = ft.TextField(
            label="Contraseña actual",
            label_style=ft.TextStyle(color="black"),
            password=True,
            can_reveal_password=True,
            border_color=COLOR_BORDE,
            color="black",
            text_size=14,
            bgcolor="#F5F5F5"
        )
        input_nueva = ft.TextField(
            label="Nueva contraseña",
            label_style=ft.TextStyle(color="black"),
            password=True,
            can_reveal_password=True,
            border_color=COLOR_BORDE,
            color="black",
            text_size=14,
            bgcolor="#F5F5F5"
        )
        input_confirmar = ft.TextField(
            label="Confirmar nueva contraseña",
            label_style=ft.TextStyle(color="black"),
            password=True,
            can_reveal_password=True,
            border_color=COLOR_BORDE,
            color="black",
            text_size=14,
            bgcolor="#F5F5F5"
        )

        def ejecutar_cambio(e):
            if not input_actual.value or not input_nueva.value:
                page.snack_bar = ft.SnackBar(ft.Text("❌ Todos los campos son obligatorios"), bgcolor="#D32F2F")
                page.snack_bar.open = True
                page.update()
                return
            
            if input_nueva.value != input_confirmar.value:
                page.snack_bar = ft.SnackBar(ft.Text("❌ Las contraseñas nuevas no coinciden"), bgcolor="#D32F2F")
                page.snack_bar.open = True
                page.update()
                return

            exito, resultado = cambiar_contrasenya(id_usuario, input_actual.value, input_nueva.value)

            if exito:
                dialog_pass.open = False
                page.snack_bar = ft.SnackBar(ft.Text("✅ Contraseña actualizada correctamente"), bgcolor="#4CAF50")
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {resultado}"), bgcolor="#D32F2F")
            
            page.snack_bar.open = True
            page.update()

        dialog_pass = ft.AlertDialog(
            modal=True,
            bgcolor="white", 
            title=ft.Text("Cambiar Contraseña", size=18, weight=ft.FontWeight.BOLD, color="black"),
            content=ft.Container(
                width=300,
                content=ft.Column([
                    ft.Text("Introduce tus credenciales para actualizar la seguridad.", size=12, color="#444444"),
                    input_actual,
                    input_nueva,
                    input_confirmar
                ], tight=True, spacing=15)
            ),
            actions=[
                ft.TextButton(
                    content=ft.Text("Cancelar", color="black"), 
                    on_click=lambda e: setattr(dialog_pass, 'open', False) or page.update()
                ),
                ft.ElevatedButton(
                    content=ft.Text("Guardar Cambios", color="white", weight=ft.FontWeight.BOLD),
                    bgcolor=COLOR_BTN_PASS,
                    on_click=ejecutar_cambio
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_pass)
        dialog_pass.open = True
        page.update()

    # --- ELEMENTOS DE UI ---

    def crear_campo(label: str, valor: str):
        return ft.Column(
            spacing=2,
            controls=[
                ft.Text(label, size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                ft.Text(valor, size=14, color="black", weight=ft.FontWeight.BOLD),
            ]
        )

    def btn_volver_click(e):
        #navegación inteligente basada en el contexto guardado
        contexto = obtener_contexto()
        if contexto == "admin":
            page.go("/area_admin")
        else:
            page.go("/area_personal")

    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight=ft.FontWeight.BOLD),
        on_click=btn_volver_click,
        ink=True,
        padding=10,
    )

    #foto del perfil
    if foto_url:
        contenido_foto = ft.Image(src=foto_url, width=100, height=100, fit=ft.ImageFit.COVER, border_radius=10)
    else:
        contenido_foto = ft.Icon("person", size=50, color="#999999")
    
    foto_perfil = ft.Container(width=100, height=100, border_radius=10, bgcolor="#E0E0E0", content=contenido_foto)

    #estado
    color_estado = "#4CAF50" if estado == "ACTIVO" else "#F44336"
    estado_widget = ft.Row(spacing=5, controls=[ft.Text(estado, size=14, color="black", weight=ft.FontWeight.BOLD), ft.Container(width=12, height=12, border_radius=6, bgcolor=color_estado)])

    seccion_superior = ft.Row(
        spacing=15,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            foto_perfil,
            ft.Column(
                spacing=8,
                controls=[
                    ft.Column(spacing=2, controls=[ft.Text("Nombre", size=12, color=COLOR_LABEL), ft.Text(nombre, size=14, color="black", weight="bold")]),
                    ft.Column(spacing=2, controls=[ft.Text("Apellidos", size=12, color=COLOR_LABEL), ft.Text(apellidos, size=14, color="black", weight="bold")]),
                    ft.Column(spacing=2, controls=[ft.Text("Estado", size=12, color=COLOR_LABEL), estado_widget]),
                ]
            )
        ]
    )

    # --- TARJETA BLANCA ---
    tarjeta_blanca = ft.Container(
        width=340,
        bgcolor="white",
        border_radius=20, 
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color="#66000000"),
        padding=ft.padding.only(left=20, right=20, top=50, bottom=25),
        content=ft.Column(
            spacing=15,
            tight=True,
            controls=[
                seccion_superior,
                ft.Divider(height=1, color="#E0E0E0"),
                crear_campo("Identificador", identificador),
                crear_campo("Empresa", empresa),
                crear_campo("Departamento", nombre_depto),
                crear_campo("Equipo", equipo),
                crear_campo("Cargo", cargo),
                crear_campo("ID Empleado", id_empleado),
                crear_campo("Correo corporativo", correo),
                crear_campo("Teléfono", telefono),
                crear_campo("Ubicación", ubicacion),
                crear_campo("Fecha de Incorporación", fecha_incorporacion),
                
                ft.Divider(height=10, color="transparent"),
                
                # BOTÓN CAMBIAR CONTRASEÑA
                ft.Container(
                    alignment=ft.Alignment(0, 0),
                    content=ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.LOCK_OUTLINED, size=18, color="white"),
                            ft.Text("Cambiar Contraseña", weight=ft.FontWeight.BOLD, color="white")
                        ], alignment=ft.MainAxisAlignment.CENTER, tight=True),
                        bgcolor=COLOR_BTN_PASS,
                        height=45,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        on_click=mostrar_dialog_cambio_pass
                    )
                )
            ]
        )
    )

    # Cabecera flotante
    header_flotante = ft.Container(
        width=200, height=50, bgcolor=COLOR_HEADER_BG, border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text("MIS DATOS", size=18, weight=ft.FontWeight.BOLD, color="white")
    )

    # Contenedor con scroll
    scrollable_content = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(height=40), 
            ft.Stack(
                controls=[
                    ft.Container(content=tarjeta_blanca, top=25),
                    ft.Container(content=header_flotante, top=0, left=70)
                ],
                width=340,
                height=860, 
            ),
            ft.Container(height=40),
        ]
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
                    content=scrollable_content
                ),
                ft.Container(
                    content=btn_volver,
                    top=10,
                    left=10,
                )
            ]
        )
    )