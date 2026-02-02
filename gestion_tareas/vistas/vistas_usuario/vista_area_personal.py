import flet as ft
from servicios.sesion_service import establecer_contexto

def VistaAreaPersonal(page: ft.Page):
    #marcamos que estamos en el area personal
    establecer_contexto("personal")
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_BOTON_BG = "#EEF2FF"
    COLOR_BOTON_BORDE = "#D0D8E8"

    def crear_boton_menu(emoji: str, texto: str, on_click=None):
        return ft.Container(
            width=95,
            height=95,
            bgcolor=COLOR_BOTON_BG,
            border_radius=12,
            border=ft.border.all(1, COLOR_BOTON_BORDE),
            ink=True,
            on_click=on_click,
            padding=ft.padding.only(top=12, bottom=8, left=5, right=5),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                controls=[
                    ft.Text(emoji, size=36),
                    ft.Text(texto, size=10, color="black", text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_500, max_lines=3)
                ]
            )
        )

    def click_mis_datos(e):
        page.go("/mis_datos")

    def click_tareas_pendientes(e):
        page.go("/tareas_pendientes")

    def click_tareas_realizadas(e):
        page.go("/tareas_realizadas")

    def click_crear_tarea(e):
        page.go("/nueva_tarea")

    def click_tareas_compartidas(e):
        page.go("/compartido_conmigo")

    def click_tareas_atrasadas(e):
        page.go("/tareas_atrasadas")

    def click_mis_proyectos(e):
        page.go("/mis_proyectos")

    tarjeta_blanca = ft.Container(
        width=340,
        bgcolor="white",
        border_radius=20,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=COLOR_SOMBRA),
        content=ft.Container(
            padding=ft.padding.only(left=20, right=20, top=45, bottom=25),
            content=ft.Column(
                spacing=12,
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=12, controls=[
                        crear_boton_menu("🪪", "Mis datos", click_mis_datos),
                        crear_boton_menu("📋", "Tareas Pendientes", click_tareas_pendientes),
                        crear_boton_menu("✅", "Tareas Realizadas", click_tareas_realizadas),
                    ]),
                    ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=12, controls=[
                        crear_boton_menu("✏️", "Crear Nueva Tarea", click_crear_tarea),
                        crear_boton_menu("👥", "Tareas Compartidas\nConmigo", click_tareas_compartidas),
                        crear_boton_menu("⚠️", "Tareas Atrasadas", click_tareas_atrasadas),
                    ]),
                    ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=12, controls=[
                        ft.Container(width=95, height=95), 
                        crear_boton_menu("🚀", "Mis Proyectos", click_mis_proyectos),
                        ft.Container(width=95, height=95),
                    ]),
                ]
            )
        )
    )

    header_flotante = ft.Container(
        width=220, height=50, bgcolor=COLOR_HEADER_BG, border_radius=25, alignment=ft.Alignment(0, 0),
        content=ft.Text("ÁREA PERSONAL", size=18, weight=ft.FontWeight.BOLD, color="white")
    )

    contenido_superpuesto = ft.Container(
        width=340, height=420,
        content=ft.Stack(controls=[
            ft.Container(content=tarjeta_blanca, top=25),
            ft.Container(content=header_flotante, top=0, left=60)
        ])
    )

    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[COLOR_FONDO_TOP, COLOR_FONDO_BOT]),
        alignment=ft.Alignment(0, 0),
        content=contenido_superpuesto
    )