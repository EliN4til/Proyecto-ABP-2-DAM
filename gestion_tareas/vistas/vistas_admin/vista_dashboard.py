import flet as ft
from gestion_tareas.servicios.sesion_service import establecer_contexto

def VistaAreaAdmin(page):
    #marcamos que estamos en el area de admin
    establecer_contexto("admin")
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_BOTON_BG = "#EEF2FF"
    COLOR_BOTON_BORDE = "#D0D8E8"

    def crear_boton_menu(emoji, texto, on_click=None):
        #crea un botón del menú con emoji y texto
        return ft.Container(
            width=95,
            height=95,
            bgcolor=COLOR_BOTON_BG,
            border_radius=12,
            border=ft.Border(top=ft.BorderSide(1, COLOR_BOTON_BORDE), bottom=ft.BorderSide(1, COLOR_BOTON_BORDE), left=ft.BorderSide(1, COLOR_BOTON_BORDE), right=ft.BorderSide(1, COLOR_BOTON_BORDE)),
            ink=True,
            on_click=on_click,
            padding=ft.Padding(top=12, bottom=8, left=5, right=5),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                controls=[
                    ft.Text(emoji, size=36),
                    ft.Text(
                        texto, 
                        size=10, 
                        color="black",
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_500,
                        max_lines=3,
                    )
                ]
            )
        )

    async def click_mis_datos(e):
        await page.push_route("/mis_datos")

    async def click_gestionar_trabajadores(e):
        await page.push_route("/gestionar_trabajadores")

    async def click_gestionar_departamentos(e):
        await page.push_route("/gestionar_departamentos")

    async def click_gestionar_proyectos(e):
        await page.push_route("/gestionar_proyectos")

    async def click_ver_estadisticas(e):
        await page.push_route("/estadisticas")

    async def click_configuracion(e):
        await page.push_route("/configuracion")

    async def click_auditoria(e):
        await page.push_route("/auditoria")
    
    async def click_ir_area_personal(e):
        await page.push_route("/area_personal")
    
    async def click_logout(e):
        await page.push_route("/login")

    tarjeta_blanca = ft.Container(
        width=340,
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color="#40000000", offset=ft.Offset(0, 5)),
        content=ft.Container(
            padding=ft.Padding(left=20, right=20, top=45, bottom=25),
            content=ft.Column(
                spacing=12,
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            crear_boton_menu("🪪", "Mis datos", click_mis_datos),
                            crear_boton_menu("👥", "Gestionar\nTrabajadores", click_gestionar_trabajadores),
                            crear_boton_menu("🏢", "Gestionar\nDepartamentos", click_gestionar_departamentos),
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            crear_boton_menu("📁", "Gestionar\nProyectos", click_gestionar_proyectos),
                            crear_boton_menu("📈", "Ver\nEstadísticas", click_ver_estadisticas),
                            crear_boton_menu("⚙️", "Configuración", click_configuracion),
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            crear_boton_menu("📋", "Registro de\nAuditoría", click_auditoria),
                            crear_boton_menu("👤", "Ir al Área\nPersonal", click_ir_area_personal),
                            crear_boton_menu("🚪", "Cerrar\nSesión", click_logout),
                        ]
                    ),
                ]
            )
        )
    )

    header_flotante = ft.Container(
        width=220,
        height=50,
        bgcolor=COLOR_HEADER_BG,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text("ÁREA ADMIN", size=18, weight=ft.FontWeight.BOLD, color="white")
    )

    contenido_superpuesto = ft.Container(
        width=340,
        height=420,
        content=ft.Stack(
            controls=[
                ft.Container(content=tarjeta_blanca, top=25),
                ft.Container(content=header_flotante, top=0, left=60)
            ]
        )
    )

    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[COLOR_FONDO_TOP, COLOR_FONDO_BOT]),
        alignment=ft.Alignment(0, 0),
        content=contenido_superpuesto
    )