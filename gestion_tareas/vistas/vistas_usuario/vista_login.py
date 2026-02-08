import flet as ft
from gestion_tareas.modelos.crud import validar_login
from gestion_tareas.servicios.sesion_service import guardar_usuario
import os
import json
import time

def VistaLogin(page):
    # configuracion de colores del tema
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"
    COLOR_BTN_BG = "#5B88C4"
    COLOR_INPUT_BG = "#EEEEEE"       
    COLOR_SOMBRA = "#66000000"
    
    # gestion de rutas para el archivo fisico de login
    ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    carpeta_util = os.path.join(ruta_raiz, "utilidades")
    archivo_login = os.path.join(carpeta_util, "config_login.json")

    # funciones para guardar y leer el correo guardado
    def guardar_login_local(email):
        if not os.path.exists(carpeta_util):
            os.makedirs(carpeta_util)
        datos = {"email": email}
        with open(archivo_login, "w") as f:
            json.dump(datos, f)

    def leer_login_local():
        if os.path.exists(archivo_login):
            try:
                with open(archivo_login, "r") as f:
                    return json.load(f)
            except:
                return None
        return None

    # recuperamos el email guardado si existe
    config_login = leer_login_local()
    email_guardado = config_login["email"] if config_login else None

    # texto para mostrar mensajes de error
    txt_error = ft.Text(
        "",
        color="#D32F2F",
        size=12,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )

    # indicador de carga a pantalla completa
    overlay_carga = ft.Container(
        content=ft.Column([
            ft.ProgressRing(width=50, height=50, stroke_width=4, color="white"),
            ft.Text("Iniciando sesión...", color="white", weight="bold")
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#aa000000",
        expand=True,
        visible=False
    )

    # manejador del click de login manual
    async def btn_login_click(e):
        txt_error.value = ""
        overlay_carga.visible = True
        page.update()
        
        # pausa para renderizado
        time.sleep(0.1)
        
        # validamos las credenciales en la base de datos
        exito, resultado = validar_login(txt_email.value, txt_pass.value)
        
        if exito:
            # guardamos el usuario en la sesion global
            guardar_usuario(resultado)
            # guardamos el email en el archivo fisico para la proxima vez
            guardar_login_local(txt_email.value)
            
            # redireccion segun el rol del trabajador
            if resultado.get("es_admin", False):
                await page.push_route("/area_admin")
            else:
                await page.push_route("/area_personal")
        else:
            # ocultamos carga y mostramos el error
            overlay_carga.visible = False
            txt_error.value = "❌ " + str(resultado)
            page.update()

    # segundo paso de login rapido: pedir password
    def mostrar_paso_password(e):
        dialog_confirmar.open = False
        page.update()

        txt_p_rapida = ft.TextField(
            label="Tu contraseña",
            password=True,
            can_reveal_password=True,
            bgcolor=COLOR_INPUT_BG,
            color="black",
            border_radius=10
        )

        async def ejecutar_login_rapido(e):
            overlay_carga.visible = True
            dialog_p.open = False
            page.update()
            
            exito, resultado = validar_login(email_guardado, txt_p_rapida.value)
            if exito:
                guardar_usuario(resultado)
                if resultado.get("es_admin", False):
                    await page.push_route("/area_admin")
                else:
                    await page.push_route("/area_personal")
            else:
                overlay_carga.visible = False
                page.snack_bar = ft.SnackBar(ft.Text("❌ Contraseña de usuario incorrecta"), bgcolor="red")
                page.snack_bar.open = True
                page.update()

        dialog_p = ft.AlertDialog(
            modal=True,
            title=ft.Text("Acceso Rápido"),
            content=ft.Column([
                ft.Text(f"Identificando a:\n{email_guardado}", size=12, color="grey"),
                txt_p_rapida
            ], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: setattr(dialog_p, "open", False) or page.update()),
                ft.FilledButton("Entrar", on_click=ejecutar_login_rapido, bgcolor=COLOR_BTN_BG, color="white")
            ]
        )
        page.overlay.append(dialog_p)
        dialog_p.open = True
        page.update()

    # primer paso de login rapido: confirmacion de cuenta
    dialog_confirmar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cuenta Guardada"),
        content=ft.Text(f"¿Quieres iniciar sesión con esta cuenta?\n{email_guardado}"),
        actions=[
            ft.TextButton("No", on_click=lambda _: setattr(dialog_confirmar, "open", False) or page.update()),
            ft.TextButton("Sí, continuar", on_click=mostrar_paso_password),
        ]
    )
    page.overlay.append(dialog_confirmar)

    # widget condicional de cuenta guardada
    if email_guardado:
        seccion_cuenta = ft.Container(
            padding=ft.Padding(bottom=15),
            content=ft.Column([
                ft.Text("Se ha detectado tu cuenta", size=10, color="grey", italic=True),
                ft.FilledButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ACCOUNT_CIRCLE, color="white", size=18),
                        ft.Text(f"Login como {email_guardado.split('@')[0]}", size=12)
                    ], tight=True),
                    on_click=lambda _: setattr(dialog_confirmar, "open", True) or page.update()
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5)
        )
    else:
        seccion_cuenta = ft.Container(
            padding=ft.Padding(bottom=15),
            content=ft.Text("No tienes ninguna cuenta guardada", size=11, color="grey", italic=True),
            alignment=ft.Alignment(0, 0)
        )

    async def btn_back_click(e):
        await page.push_route("/")

    # helper para crear inputs
    def crear_input(es_password=False):
        return ft.TextField(
            password=es_password,
            can_reveal_password=es_password,
            border_color="transparent",        
            focused_border_color="transparent",
            bgcolor=COLOR_INPUT_BG,
            border_radius=15,
            text_size=14,
            content_padding=15,
            height=45,
            color="black",
            cursor_color="black",
        )

    txt_email = crear_input()
    txt_pass = crear_input(es_password=True)

    btn_iniciar = ft.FilledButton(
        content=ft.Text("Iniciar Sesión", color="white", weight=ft.FontWeight.BOLD),
        bgcolor=COLOR_BTN_BG,
        width=180,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=25),
        ),
        on_click=btn_login_click
    )

    tarjeta_blanca = ft.Container(
        width=320,
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=COLOR_SOMBRA),
        content=ft.Column(
            spacing=0,
            tight=True,
            controls=[
                ft.Container(
                    padding=ft.Padding(left=20, top=15, bottom=10),
                    alignment=ft.Alignment(-1, 0),
                    content=ft.Container(
                        content=ft.Text("←", size=30, color="black", weight="bold"),
                        on_click=btn_back_click,
                        ink=True,
                        border_radius=50,
                        padding=5,
                    ),
                ),

                ft.Container(
                    height=55,
                    width=320,
                    bgcolor=COLOR_HEADER_BG,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("INICIO DE SESIÓN", size=18, weight=ft.FontWeight.BOLD, color="white")
                ),
                
                ft.Container(
                    padding=ft.Padding(left=30, right=30, top=20, bottom=40),
                    content=ft.Column(
                        spacing=5,
                        tight=True,
                        controls=[
                            seccion_cuenta,
                            ft.Divider(height=20, color="#EEEEEE"),
                            ft.Text("Correo Electrónico", weight=ft.FontWeight.BOLD, color="black", size=14),
                            ft.Container(content=txt_email, margin=ft.Margin(bottom=15, left=0, right=0, top=0)),
                            
                            ft.Text("Contraseña", weight=ft.FontWeight.BOLD, color="black", size=14),
                            ft.Container(content=txt_pass, margin=ft.Margin(bottom=15, left=0, right=0, top=0)),
                            
                            ft.Container(content=txt_error, margin=ft.Margin(bottom=10, left=0, right=0, top=0)),

                            ft.Container(content=btn_iniciar, alignment=ft.Alignment(0, 0))
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
        content=ft.Stack([
            ft.Container(content=tarjeta_blanca, alignment=ft.Alignment(0, 0)),
            overlay_carga
        ])
    )