import flet as ft

def VistaConfiguracion(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_BTN_GUARDAR = "#4682B4"
    COLOR_PELIGRO = "#E53935"

    def btn_volver_click(e):
        """Acción al hacer clic en el botón volver atrás"""
        page.snack_bar = ft.SnackBar(ft.Text("Volver atrás"))
        page.snack_bar.open = True
        page.update()

    def btn_guardar_click(e):
        """Acción al hacer clic en el botón guardar"""
        page.snack_bar = ft.SnackBar(ft.Text("Configuración guardada correctamente"))
        page.snack_bar.open = True
        page.update()

    def crear_seccion_titulo(titulo: str, icono: str):
        """Crea un título de sección"""
        return ft.Container(
            padding=ft.padding.only(top=10, bottom=5),
            content=ft.Row(
                spacing=8,
                controls=[
                    ft.Text(icono, size=16),
                    ft.Text(titulo, size=13, color="black", weight=ft.FontWeight.BOLD),
                ]
            )
        )

    def crear_opcion_switch(label: str, valor: bool = False, on_change=None):
        """Crea una opción con switch"""
        switch = ft.Switch(value=valor, active_color=COLOR_LABEL, on_change=on_change)
        return ft.Container(
            padding=ft.padding.only(top=5, bottom=5),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(label, size=12, color="black"),
                    switch,
                ]
            )
        )

    def crear_opcion_dropdown(label: str, opciones: list, valor: str = None):
        """Crea una opción con dropdown"""
        return ft.Column(
            spacing=3,
            controls=[
                ft.Text(label, size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                ft.DropdownM2(
                    value=valor,
                    hint_text="Seleccionar...",
                    hint_style=ft.TextStyle(size=11, color="#999999"),
                    text_style=ft.TextStyle(size=12, color="black"),
                    bgcolor="white",
                    fill_color="white",
                    border_color=COLOR_BORDE,
                    border_radius=5,
                    height=40,
                    expand=True,
                    content_padding=ft.padding.only(left=10, right=10),
                    options=[ft.dropdownm2.Option(op) for op in opciones],
                ),
            ]
        )

    def crear_opcion_texto(label: str, valor: str = "", hint: str = ""):
        """Crea una opción con campo de texto"""
        return ft.Column(
            spacing=3,
            controls=[
                ft.Text(label, size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                ft.TextField(
                    value=valor,
                    hint_text=hint,
                    hint_style=ft.TextStyle(size=11, color="#999999"),
                    text_style=ft.TextStyle(size=12, color="black"),
                    border_color=COLOR_BORDE,
                    border_radius=5,
                    height=40,
                    content_padding=ft.padding.only(left=10, right=10, top=8, bottom=8),
                ),
            ]
        )

    #diálogo zona peligrosa
    def mostrar_dialog_restablecer(e):
        """Muestra diálogo de confirmación para restablecer"""
        def confirmar(e):
            dialog.open = False
            page.snack_bar = ft.SnackBar(ft.Text("Configuración restablecida"))
            page.snack_bar.open = True
            page.update()

        def cancelar(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("⚠️ Restablecer configuración", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=280,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    tight=True,
                    controls=[
                        ft.Text("¿Estás seguro de que deseas restablecer toda la configuración a los valores por defecto?", size=12, color="black"),
                        ft.Text("Esta acción no se puede deshacer.", size=11, color=COLOR_PELIGRO, italic=True),
                    ]
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.TextButton("Restablecer", on_click=confirmar, style=ft.ButtonStyle(color=COLOR_PELIGRO)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def mostrar_dialog_limpiar_cache(e):
        """Muestra diálogo de confirmación para limpiar caché"""
        def confirmar(e):
            dialog.open = False
            page.snack_bar = ft.SnackBar(ft.Text("Caché limpiada correctamente"))
            page.snack_bar.open = True
            page.update()

        def cancelar(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("🗑️ Limpiar caché", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=280,
                bgcolor="white",
                content=ft.Text("¿Deseas limpiar toda la caché del sistema? Esto puede mejorar el rendimiento.", size=12, color="black"),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.TextButton("Limpiar", on_click=confirmar),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    #botón volver
    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight=ft.FontWeight.BOLD),
        on_click=btn_volver_click,
        ink=True,
        padding=10,
    )

    #sección General
    seccion_general = ft.Column(
        spacing=5,
        controls=[
            crear_seccion_titulo("General", "⚙️"),
            crear_opcion_texto("Nombre de la empresa", "TechSolutions S.L", "Nombre de la empresa"),
            crear_opcion_dropdown("Idioma", ["Español", "English", "Português", "Français"], "Español"),
            crear_opcion_dropdown("Zona horaria", ["Europe/Madrid", "Europe/London", "America/New_York", "Asia/Tokyo"], "Europe/Madrid"),
        ]
    )

    #sección Notificaciones
    seccion_notificaciones = ft.Column(
        spacing=5,
        controls=[
            crear_seccion_titulo("Notificaciones", "🔔"),
            crear_opcion_switch("Notificaciones por email", True),
            crear_opcion_switch("Notificaciones push", True),
            crear_opcion_switch("Resumen diario", False),
            crear_opcion_switch("Alertas de tareas atrasadas", True),
        ]
    )

    #sección Tareas
    seccion_tareas = ft.Column(
        spacing=5,
        controls=[
            crear_seccion_titulo("Tareas", "📋"),
            crear_opcion_dropdown("Prioridad por defecto", ["Alta", "Media", "Baja"], "Media"),
            crear_opcion_dropdown("Días para marcar como atrasada", ["1 día", "2 días", "3 días", "5 días", "7 días"], "3 días"),
            crear_opcion_switch("Permitir tareas sin asignar", False),
            crear_opcion_switch("Requerir fecha límite", True),
        ]
    )

    #sección Seguridad
    seccion_seguridad = ft.Column(
        spacing=5,
        controls=[
            crear_seccion_titulo("Seguridad", "🔐"),
            crear_opcion_switch("Autenticación de dos factores", False),
            crear_opcion_dropdown("Tiempo de sesión", ["15 minutos", "30 minutos", "1 hora", "4 horas", "8 horas"], "1 hora"),
            crear_opcion_switch("Registro de actividad", True),
        ]
    )

    #sección Zona Peligrosa
    seccion_peligrosa = ft.Container(
        bgcolor="#FFF5F5",
        border_radius=10,
        border=ft.border.all(1, COLOR_PELIGRO),
        padding=ft.padding.all(12),
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    spacing=8,
                    controls=[
                        ft.Text("⚠️", size=16),
                        ft.Text("Zona Peligrosa", size=13, color=COLOR_PELIGRO, weight=ft.FontWeight.BOLD),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Limpiar caché", size=11, color="black"),
                        ft.Container(
                            content=ft.Text("Limpiar", size=10, color=COLOR_PELIGRO),
                            border=ft.border.all(1, COLOR_PELIGRO),
                            border_radius=5,
                            padding=ft.padding.only(left=10, right=10, top=5, bottom=5),
                            on_click=mostrar_dialog_limpiar_cache,
                            ink=True,
                        ),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Restablecer configuración", size=11, color="black"),
                        ft.Container(
                            content=ft.Text("Restablecer", size=10, color="white"),
                            bgcolor=COLOR_PELIGRO,
                            border_radius=5,
                            padding=ft.padding.only(left=10, right=10, top=5, bottom=5),
                            on_click=mostrar_dialog_restablecer,
                            ink=True,
                        ),
                    ]
                ),
            ]
        )
    )

    #botón guardar
    btn_guardar = ft.Container(
        width=180,
        height=44,
        bgcolor=COLOR_BTN_GUARDAR,
        border_radius=22,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_guardar_click,
        content=ft.Text("Guardar Cambios", color="white", weight=ft.FontWeight.BOLD, size=14),
    )

    #contenido scrolleable
    contenido_scroll = ft.Column(
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            seccion_general,
            ft.Divider(height=1, color=COLOR_BORDE),
            seccion_notificaciones,
            ft.Divider(height=1, color=COLOR_BORDE),
            seccion_tareas,
            ft.Divider(height=1, color=COLOR_BORDE),
            seccion_seguridad,
            ft.Divider(height=1, color=COLOR_BORDE),
            seccion_peligrosa,
        ]
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
                spacing=15,
                controls=[
                    ft.Container(
                        height=500,
                        content=contenido_scroll,
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[btn_guardar],
                    ),
                ]
            )
        )
    )

    #header flotante
    header_flotante = ft.Container(
        width=220,
        height=50,
        bgcolor=COLOR_HEADER_BG,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            "CONFIGURACIÓN",
            size=18,
            weight=ft.FontWeight.BOLD,
            color="white"
        )
    )

    #contenido superpuesto (tarjeta + header)
    contenido_superpuesto = ft.Container(
        width=380,
        height=680,
        content=ft.Stack(
            controls=[
                ft.Container(
                    content=tarjeta_blanca,
                    top=30,
                ),
                ft.Container(
                    content=header_flotante,
                    top=0,
                    left=80,
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
    page.title = "App Tareas - Configuración"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 400
    page.window.min_height = 750
    page.padding = 0 
    
    vista = VistaConfiguracion(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)