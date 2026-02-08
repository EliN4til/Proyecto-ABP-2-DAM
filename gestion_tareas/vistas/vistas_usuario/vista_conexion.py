import flet as ft
from gestion_tareas.servicios.db_manager import realizar_conexion
import os
import json

def VistaConexion(page):
    #configuracion de colores
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_BTN_BG = "#4682B4"         
    COLOR_INPUT_BG = "#EEEEEE"       
    COLOR_SOMBRA = "#66000000"
    
    #ruta del archivo de configuracion
    #buscamos la raiz del proyecto y creamos la carpeta utilidades
    ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    carpeta_util = os.path.join(ruta_raiz, "utilidades")
    archivo_config = os.path.join(carpeta_util, "config_db.json")

    #funciones para gestionar el archivo
    def guardar_datos_fisicos(uri, usuario):
        if not os.path.exists(carpeta_util):
            os.makedirs(carpeta_util)
        datos = {"uri": uri, "usuario": usuario}
        with open(archivo_config, "w") as f:
            json.dump(datos, f)

    def leer_datos_fisicos():
        if os.path.exists(archivo_config):
            try:
                with open(archivo_config, "r") as f:
                    return json.load(f)
            except:
                return None
        return None

    #intentamos recuperar conexion anterior
    config_guardada = leer_datos_fisicos()
    uri_persistente = config_guardada["uri"] if config_guardada else None
    user_persistente = config_guardada["usuario"] if config_guardada else None

    #texto para errores
    txt_error = ft.Text(
        "",
        color="#D32F2F",
        size=12,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )

    #overlay de carga centrado
    overlay_carga = ft.Container(
        content=ft.Column([
            ft.ProgressRing(width=50, height=50, stroke_width=4, color="white"),
            ft.Text("Conectando con Atlas...", color="white", weight="bold")
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#aa000000",
        expand=True,
        visible=False #empieza oculto
    )

    #manejador boton conectarse
    async def btn_conectar_click(e):
        txt_error.value = ""
        overlay_carga.visible = True
        page.update()
        
        #intentamos la conexion tecnica
        exito = realizar_conexion(txt_uri.value, txt_usuario.value, txt_pass.value)

        if exito:
            #guardamos en archivo json fisico
            guardar_datos_fisicos(txt_uri.value, txt_usuario.value)
            await page.push_route("/login")
        else:
            overlay_carga.visible = False
            txt_error.value = "❌ Error de conexión. Revisa los datos."
            page.update()

    #segundo pop up para la password
    def mostrar_paso_password(e):
        dialog_confirmar.open = False
        page.update()

        txt_p_rapida = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            bgcolor=COLOR_INPUT_BG,
            color="black"
        )

        async def login_rapido_final(e):
            overlay_carga.visible = True
            dialog_p.open = False
            page.update()
            
            exito = realizar_conexion(uri_persistente, user_persistente, txt_p_rapida.value)
            if exito:
                await page.push_route("/login")
            else:
                overlay_carga.visible = False
                page.snack_bar = ft.SnackBar(ft.Text("❌ Password incorrecta"), bgcolor="red")
                page.snack_bar.open = True
                page.update()

        dialog_p = ft.AlertDialog(
            modal=True,
            title=ft.Text("Seguridad"),
            content=ft.Column([
                ft.Text(f"Usando usuario: {user_persistente}", size=12, color="grey"),
                txt_p_rapida
            ], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: setattr(dialog_p, "open", False) or page.update()),
                ft.FilledButton("Conectar", on_click=login_rapido_final, bgcolor=COLOR_BTN_BG, color="white")
            ]
        )
        page.overlay.append(dialog_p)
        dialog_p.open = True
        page.update()

    #primer popup de confirmacion
    dialog_confirmar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Conexión Guardada"),
        content=ft.Text(f"¿Quieres iniciar sesión en:\n{uri_persistente}?"),
        actions=[
            ft.TextButton("No", on_click=lambda _: setattr(dialog_confirmar, "open", False) or page.update()),
            ft.TextButton("Sí, entrar", on_click=mostrar_paso_password),
        ]
    )
    page.overlay.append(dialog_confirmar)

    #widget condicional de la parte superior
    if uri_persistente and user_persistente:
        #mostramos boton si hay archivo fisico
        seccion_persistente = ft.Container(
            padding=ft.Padding(bottom=15),
            content=ft.Column([
                ft.Text("Se ha detectado una configuración", size=10, color="grey", italic=True),
                ft.FilledButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CLOUD_DONE, color="amber", size=18),
                        ft.Text(f"Entrar como {user_persistente}", size=12)
                    ], tight=True),
                    on_click=lambda _: setattr(dialog_confirmar, "open", True) or page.update()
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5)
        )
    else:
        #mostramos texto si no existe el archivo
        seccion_persistente = ft.Container(
            padding=ft.Padding(bottom=15),
            content=ft.Text("No tienes ninguna conexión guardada", size=11, color="grey", italic=True),
            alignment=ft.Alignment(0, 0)
        )

    #creacion de campos de entrada
    def crear_input(es_pass=False):
        return ft.TextField(
            password=es_pass,
            can_reveal_password=es_pass,
            border_color="transparent",        
            bgcolor=COLOR_INPUT_BG,
            border_radius=15,
            text_size=14,
            height=45,
            color="black"
        )

    txt_uri = crear_input()
    txt_usuario = crear_input()
    txt_pass = crear_input(es_pass=True)

    btn_conectar = ft.FilledButton(
        content=ft.Text("Conectarse", color="white", weight=ft.FontWeight.BOLD),
        bgcolor=COLOR_BTN_BG,
        width=200,
        height=45,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25)),
        on_click=btn_conectar_click
    )

    #tarjeta blanca diseño
    tarjeta = ft.Container(
        width=320,
        bgcolor="white",
        border_radius=20,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=COLOR_SOMBRA),
        content=ft.Column(
            spacing=0,
            tight=True,
            controls=[
                ft.Container(
                    height=60, width=320, bgcolor=COLOR_HEADER_BG,
                    border_radius=ft.BorderRadius(top_left=20, top_right=20, bottom_left=0, bottom_right=0),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("CONEXIÓN BD", size=18, weight="bold", color="white")
                ),
                ft.Container(
                    padding=30,
                    content=ft.Column(
                        spacing=5,
                        controls=[
                            seccion_persistente,
                            ft.Divider(height=10),
                            ft.Text("URI", weight="bold", color="black", size=13),
                            txt_uri,
                            ft.Text("Usuario", weight="bold", color="black", size=13),
                            txt_usuario,
                            ft.Text("Contraseña", weight="bold", color="black", size=13),
                            txt_pass,
                            ft.Container(content=txt_error, margin=ft.Margin(top=10, bottom=10, left=0, right=0), alignment=ft.Alignment(0,0)),
                            ft.Container(content=btn_conectar, alignment=ft.Alignment(0, 0))
                        ]
                    )
                )
            ]
        )
    )

    #retorno de la vista constack para loading
    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[COLOR_FONDO_TOP, COLOR_FONDO_BOT],
        ),
        content=ft.Stack([
            ft.Container(content=tarjeta, alignment=ft.Alignment(0, 0)),
            overlay_carga
        ])
    )