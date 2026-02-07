import flet as ft
import os
import json

def VistaConfiguracion(page):
    #configuracion de colores del tema
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_BTN_GUARDAR = "#4682B4"
    COLOR_PELIGRO = "#E53935"

    #gestion de archivo fisico para persistencia sencilla
    ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    carpeta_util = os.path.join(ruta_raiz, "utilidades")
    archivo_settings = os.path.join(carpeta_util, "settings.json")

    def guardar_ajustes_locales(empresa, sesion):
        if not os.path.exists(carpeta_util):
            os.makedirs(carpeta_util)
        datos = {"empresa": empresa, "sesion": sesion}
        with open(archivo_settings, "w") as f:
            json.dump(datos, f)

    def leer_ajustes_locales():
        if os.path.exists(archivo_settings):
            try:
                with open(archivo_settings, "r") as f:
                    return json.load(f)
            except:
                return None
        return None

    #cargamos los datos guardados o ponemos por defecto
    config_actual = leer_ajustes_locales()
    empresa_valor = config_actual["empresa"] if config_actual else "TechSolutions S.L"
    sesion_valor = config_actual["sesion"] if config_actual else "1 hora"

    #manejadores de eventos
    def btn_volver_click(e):
        page.go("/area_admin")

    def btn_guardar_click(e):
        #guardamos los cambios en el archivo json
        guardar_ajustes_locales(input_empresa.value, dd_sesion.value)
        page.snack_bar = ft.SnackBar(ft.Text("✅ Configuración actualizada"), bgcolor="green")
        page.snack_bar.open = True
        page.update()

    def btn_restablecer_click(e):
        #volvemos a los valores originales
        input_empresa.value = "TechSolutions S.L"
        dd_sesion.value = "1 hora"
        guardar_ajustes_locales(input_empresa.value, dd_sesion.value)
        page.snack_bar = ft.SnackBar(ft.Text("🔄 Valores restablecidos"))
        page.snack_bar.open = True
        page.update()

    #componentes de la interfaz
    input_empresa = ft.TextField(
        label="Nombre de la Empresa",
        value=empresa_valor,
        border_color=COLOR_BORDE,
        text_size=12,
        height=45,
        color="black"
    )

    dd_sesion = ft.DropdownM2(
        label="Tiempo de expiración de sesión",
        value=sesion_valor,
        options=[
            ft.dropdownm2.Option("30 minutos"),
            ft.dropdownm2.Option("1 hora"),
            ft.dropdownm2.Option("4 horas"),
            ft.dropdownm2.Option("8 horas")
        ],
        border_color=COLOR_BORDE,
        text_size=12,
        height=45,
        color="black"
    )

    #seccion general
    seccion_general = ft.Column([
        ft.Row([ft.Text("⚙️", size=16), ft.Text("Ajustes Generales", size=13, color="black", weight="bold")], spacing=8),
        input_empresa,
    ], spacing=10)

    #seccion seguridad
    seccion_seguridad = ft.Column([
        ft.Row([ft.Text("🔐", size=16), ft.Text("Seguridad", size=13, color="black", weight="bold")], spacing=8),
        dd_sesion,
    ], spacing=10)

    #zona peligrosa
    seccion_peligrosa = ft.Container(
        bgcolor="#FFF5F5",
        border_radius=10,
        border=ft.border.all(1, COLOR_PELIGRO),
        padding=12,
        content=ft.Column([
            ft.Row([ft.Text("⚠️", size=16), ft.Text("Zona Crítica", size=13, color=COLOR_PELIGRO, weight="bold")], spacing=8),
            ft.Row([
                ft.Text("Restablecer ajustes", size=11, color="black"),
                ft.ElevatedButton("Reset", color="white", bgcolor=COLOR_PELIGRO, on_click=btn_restablecer_click, height=30)
            ], alignment="spaceBetween")
        ], spacing=10)
    )

    #boton de guardado
    btn_guardar = ft.Container(
        width=180, height=44, bgcolor=COLOR_BTN_GUARDAR, border_radius=22, alignment=ft.Alignment(0, 0),
        on_click=btn_guardar_click, ink=True,
        content=ft.Text("Guardar Cambios", color="white", weight="bold", size=14)
    )

    #maquetacion de la tarjeta central
    tarjeta_blanca = ft.Container(
        width=380, bgcolor="white", border_radius=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color=COLOR_SOMBRA, offset=ft.Offset(0, 5)),
        content=ft.Container(
            padding=ft.padding.only(left=20, right=20, top=55, bottom=25),
            content=ft.Column([
                ft.Container(height=400, content=ft.Column([
                    seccion_general,
                    ft.Divider(height=20, color=COLOR_BORDE),
                    seccion_seguridad,
                    ft.Divider(height=20, color=COLOR_BORDE),
                    seccion_peligrosa,
                ], scroll="auto", spacing=20)),
                ft.Row([btn_guardar], alignment="center")
            ], spacing=20)
        )
    )

    #cabecera flotante
    header_flotante = ft.Container(
        width=220, height=50, bgcolor=COLOR_HEADER_BG, border_radius=25, alignment=ft.Alignment(0, 0),
        content=ft.Text("CONFIGURACIÓN", size=18, weight="bold", color="white")
    )

    #boton de retorno
    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight="bold"),
        on_click=btn_volver_click, top=10, left=10, padding=10
    )

    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[COLOR_FONDO_TOP, COLOR_FONDO_BOT]),
        content=ft.Stack([
            ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=ft.Stack([
                ft.Container(content=tarjeta_blanca, top=30),
                ft.Container(content=header_flotante, top=0, left=80)
            ], width=380, height=620)),
            btn_volver
        ])
    )