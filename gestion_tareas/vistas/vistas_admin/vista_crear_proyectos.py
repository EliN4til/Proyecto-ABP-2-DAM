import flet as ft

def VistaCrearProyecto(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_BTN_CREAR = "#4682B4"

    def btn_volver_click(e):
        """Acción al hacer clic en el botón volver atrás"""
        page.snack_bar = ft.SnackBar(ft.Text("Volver atrás"))
        page.snack_bar.open = True
        page.update()

    def btn_crear_click(e):
        """Acción al hacer clic en el botón crear"""
        if not input_nombre.value:
            page.snack_bar = ft.SnackBar(ft.Text("El nombre del proyecto es obligatorio"))
            page.snack_bar.open = True
            page.update()
            return
        
        page.snack_bar = ft.SnackBar(ft.Text(f"Proyecto '{input_nombre.value}' creado correctamente"))
        page.snack_bar.open = True
        page.update()

    def crear_campo_texto(label: str, hint: str = "", obligatorio: bool = False, multiline: bool = False):
        """Crea un campo de texto con etiqueta"""
        label_text = f"{label} *" if obligatorio else label
        return ft.Column(
            spacing=3,
            controls=[
                ft.Text(label_text, size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                ft.TextField(
                    hint_text=hint,
                    hint_style=ft.TextStyle(size=11, color="#999999"),
                    text_style=ft.TextStyle(size=12, color="black"),
                    border_color=COLOR_BORDE,
                    border_radius=5,
                    height=40 if not multiline else 80,
                    content_padding=ft.padding.only(left=10, right=10, top=8, bottom=8),
                    multiline=multiline,
                    min_lines=3 if multiline else 1,
                    max_lines=3 if multiline else 1,
                ),
            ]
        )

    def crear_campo_dropdown(label: str, opciones: list, hint: str = "Seleccionar..."):
        """Crea un campo dropdown con etiqueta"""
        return ft.Column(
            spacing=3,
            controls=[
                ft.Text(label, size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                ft.DropdownM2(
                    hint_text=hint,
                    hint_style=ft.TextStyle(size=11, color="#999999"),
                    text_style=ft.TextStyle(size=12, color="black"),
                    bgcolor="white",
                    fill_color="white",
                    border_color=COLOR_BORDE,
                    border_radius=5,
                    height=40,
                    content_padding=ft.padding.only(left=10, right=10),
                    options=[ft.dropdownm2.Option(op) for op in opciones],
                ),
            ]
        )

    def crear_campo_fecha(label: str):
        """Crea un campo de fecha con etiqueta"""
        return ft.Column(
            spacing=3,
            controls=[
                ft.Text(label, size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                ft.TextField(
                    hint_text="DD/MM/AAAA",
                    hint_style=ft.TextStyle(size=11, color="#999999"),
                    text_style=ft.TextStyle(size=12, color="black"),
                    border_color=COLOR_BORDE,
                    border_radius=5,
                    height=40,
                    content_padding=ft.padding.only(left=10, right=10, top=8, bottom=8),
                    suffix=ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=COLOR_LABEL),
                ),
            ]
        )

    #botón volver
    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight=ft.FontWeight.BOLD),
        on_click=btn_volver_click,
        ink=True,
        padding=10,
    )

    #campos del formulario
    input_nombre = ft.TextField(
        hint_text="Nombre del proyecto",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=40,
        content_padding=ft.padding.only(left=10, right=10, top=8, bottom=8),
    )

    campo_nombre = ft.Column(
        spacing=3,
        controls=[
            ft.Text("Nombre del Proyecto *", size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
            input_nombre,
        ]
    )

    campo_codigo = crear_campo_texto("Código", "Ej: PRY001")
    campo_descripcion = crear_campo_texto("Descripción", "Descripción del proyecto...", multiline=True)
    
    campo_cliente = crear_campo_dropdown("Cliente", [
        "TechCorp S.A.",
        "Innovatech Ltd.",
        "GlobalMedia",
        "FinanceHub",
        "StartupXYZ",
        "Interno",
    ])

    campo_responsable = crear_campo_dropdown("Responsable", [
        "Ana García (EMP001)",
        "Carlos López (EMP002)",
        "María Rodríguez (EMP003)",
        "Pedro Martínez (EMP004)",
        "Laura Sánchez (EMP005)",
        "Juan Fernández (EMP006)",
        "Sofia Ruiz (EMP007)",
        "Diego Torres (EMP008)",
    ])

    campo_presupuesto = ft.Column(
        spacing=3,
        controls=[
            ft.Text("Presupuesto", size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
            ft.TextField(
                hint_text="0.00",
                hint_style=ft.TextStyle(size=11, color="#999999"),
                text_style=ft.TextStyle(size=12, color="black"),
                border_color=COLOR_BORDE,
                border_radius=5,
                height=40,
                content_padding=ft.padding.only(left=10, right=10, top=8, bottom=8),
                suffix=ft.Text("€", size=12, color=COLOR_LABEL),
                keyboard_type=ft.KeyboardType.NUMBER,
            ),
        ]
    )

    campo_fecha_inicio = crear_campo_fecha("Fecha de inicio")
    campo_fecha_fin = crear_campo_fecha("Fecha de fin")

    campo_estado = crear_campo_dropdown("Estado", [
        "ACTIVO",
        "INACTIVO",
        "EN CREACIÓN",
    ], "Seleccionar estado...")

    #botón crear
    btn_crear = ft.Container(
        width=170,
        height=44,
        bgcolor=COLOR_BTN_CREAR,
        border_radius=22,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_crear_click,
        content=ft.Text("Crear Proyecto", color="white", weight=ft.FontWeight.BOLD, size=14),
    )

    #formulario scrolleable
    formulario = ft.Column(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            campo_nombre,
            campo_codigo,
            campo_descripcion,
            campo_cliente,
            campo_responsable,
            campo_presupuesto,
            ft.Row(
                spacing=10,
                controls=[
                    ft.Container(expand=True, content=campo_fecha_inicio),
                    ft.Container(expand=True, content=campo_fecha_fin),
                ]
            ),
            campo_estado,
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
                        height=520,
                        content=formulario,
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
        width=220,
        height=50,
        bgcolor=COLOR_HEADER_BG,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            "CREAR PROYECTO",
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
    page.title = "App Tareas - Crear Proyecto"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 400
    page.window.min_height = 750
    page.padding = 0 
    
    vista = VistaCrearProyecto(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)