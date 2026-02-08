import flet as ft
from gestion_tareas.modelos.crud import obtener_configuracion, actualizar_configuracion

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

    # --- LÓGICA DE BASE DE DATOS ---
    
    config_db = {}
    
    def cargar_datos_config():
        nonlocal config_db
        exito, res = obtener_configuracion()
        if exito:
            config_db = res
        else:
            config_db = {"empresa": "TechSolutions S.L", "sesion": "1 hora"} # Fallback

    # Carga inicial
    cargar_datos_config()
    empresa_valor = config_db.get("empresa", "TechSolutions S.L")
    sesion_valor = config_db.get("sesion", "1 hora")


    #manejadores de eventos
    async def btn_volver_click(e):
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

    def btn_guardar_click(e):
        #guardamos los cambios en la BD
        nuevos_datos = {
            "empresa": input_empresa.value,
            "sesion": dd_sesion.value
        }
        exito, msg = actualizar_configuracion(nuevos_datos)
        
        if exito:
            mostrar_mensaje_dialog(page, "✅ Éxito", "Configuración actualizada en BD", "green")
        else:
            mostrar_mensaje_dialog(page, "❌ Error", f"Error al guardar: {msg}", "red")
        page.update()

    def btn_restablecer_click(e):
        #volvemos a los valores originales
        input_empresa.value = "TechSolutions S.L"
        dd_sesion.value = "1 hora"
        
        nuevos_datos = {
            "empresa": "TechSolutions S.L",
            "sesion": "1 hora"
        }
        actualizar_configuracion(nuevos_datos)
        
        mostrar_mensaje_dialog(page, "🔄 Restablecido", "Valores restablecidos a defecto", "blue")
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
        border=ft.Border(top=ft.BorderSide(1, COLOR_PELIGRO), bottom=ft.BorderSide(1, COLOR_PELIGRO), left=ft.BorderSide(1, COLOR_PELIGRO), right=ft.BorderSide(1, COLOR_PELIGRO)),
        padding=12,
        content=ft.Column([
            ft.Row([ft.Text("⚠️", size=16), ft.Text("Zona Crítica", size=13, color=COLOR_PELIGRO, weight="bold")], spacing=8),
            ft.Row([
                ft.Text("Restablecer ajustes", size=11, color="black"),
                ft.FilledButton("Reset", color="white", bgcolor=COLOR_PELIGRO, on_click=btn_restablecer_click, height=30)
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
            padding=ft.Padding(left=20, right=20, top=55, bottom=25),
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