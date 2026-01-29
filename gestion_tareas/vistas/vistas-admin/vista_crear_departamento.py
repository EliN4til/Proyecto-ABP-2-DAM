import flet as ft

def VistaCrearDepartamento(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_BTN_CREAR = "#4682B4"

    #opciones para los dropdowns
    EMPRESAS = ["TechSolutions S.L", "InnovateTech Corp", "Digital Systems S.A", "CloudNet Solutions"]
    UBICACIONES = ["Oficina Central - Madrid", "Oficina Barcelona", "Oficina Valencia", "Remoto", "Todas las sedes"]
    ESTADOS = ["ACTIVO", "INACTIVO", "EN CREACIÓN"]
    RESPONSABLES = [
        "Ana García (EMP001)", 
        "Carlos López (EMP002)", 
        "María Rodríguez (EMP003)", 
        "Pedro Martínez (EMP004)",
        "Laura Sánchez (EMP005)",
    ]

    def btn_volver_click(e):
        """Acción al hacer clic en el botón volver atrás"""
        page.snack_bar = ft.SnackBar(ft.Text("Volver atrás"))
        page.snack_bar.open = True
        page.update()

    def btn_crear_click(e):
        """Acción al hacer clic en el botón crear departamento"""
        #validar campos obligatorios
        if not input_nombre.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa los campos obligatorios"))
            page.snack_bar.open = True
            page.update()
            return
        
        page.snack_bar = ft.SnackBar(ft.Text(f"Departamento '{input_nombre.value}' creado correctamente"))
        page.snack_bar.open = True
        page.update()

    def crear_campo_texto(hint: str, expand: bool = False, multiline: bool = False, min_lines: int = 1):
        """Crea un campo de texto estándar"""
        return ft.TextField(
            hint_text=hint,
            hint_style=ft.TextStyle(size=11, color="#999999"),
            text_style=ft.TextStyle(size=12, color="black"),
            border_color=COLOR_BORDE,
            border_radius=5,
            height=40 if not multiline else None,
            expand=expand,
            multiline=multiline,
            min_lines=min_lines if multiline else None,
            max_lines=min_lines if multiline else None,
            content_padding=ft.padding.only(left=10, right=10, top=8, bottom=8),
        )

    def crear_dropdown(opciones: list, hint: str):
        """Crea un dropdown con las opciones dadas"""
        return ft.DropdownM2(
            hint_text=hint,
            hint_style=ft.TextStyle(size=11, color="#999999"),
            text_style=ft.TextStyle(size=12, color="black"),
            bgcolor="white",
            fill_color="white",
            border_color=COLOR_BORDE,
            border_radius=5,
            height=40,
            expand=True,
            content_padding=ft.padding.only(left=10, right=10),
            options=[ft.dropdownm2.Option(opcion) for opcion in opciones],
        )

    def crear_label(texto: str):
        """Crea una etiqueta de campo"""
        return ft.Text(texto, size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500)

    #botón volver
    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight=ft.FontWeight.BOLD),
        on_click=btn_volver_click,
        ink=True,
        padding=10,
    )

    #campos del formulario
    input_nombre = crear_campo_texto("Nombre del departamento")
    input_codigo = crear_campo_texto("Ej: DEV, HR, FIN...")
    input_descripcion = crear_campo_texto("Descripción del departamento...", multiline=True, min_lines=3)
    input_presupuesto = crear_campo_texto("Presupuesto anual (€)")
    input_email = crear_campo_texto("departamento@empresa.com")
    input_telefono = crear_campo_texto("+34 XXX XXX XXX")

    dropdown_empresa = crear_dropdown(EMPRESAS, "Selecciona empresa...")
    dropdown_responsable = crear_dropdown(RESPONSABLES, "Selecciona responsable...")
    dropdown_ubicacion = crear_dropdown(UBICACIONES, "Selecciona ubicación...")
    dropdown_estado = crear_dropdown(ESTADOS, "Selecciona estado...")

    #contenido del formulario
    formulario = ft.Column(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            #nombre del departamento
            ft.Column(spacing=3, controls=[
                crear_label("Nombre del Departamento *"),
                input_nombre,
            ]),
            
            #código
            ft.Column(spacing=3, controls=[
                crear_label("Código"),
                input_codigo,
            ]),
            
            #empresa
            ft.Column(spacing=3, controls=[
                crear_label("Empresa"),
                dropdown_empresa,
            ]),
            
            #responsable
            ft.Column(spacing=3, controls=[
                crear_label("Responsable"),
                dropdown_responsable,
            ]),
            
            #descripción
            ft.Column(spacing=3, controls=[
                crear_label("Descripción"),
                input_descripcion,
            ]),
            
            #ubicación
            ft.Column(spacing=3, controls=[
                crear_label("Ubicación"),
                dropdown_ubicacion,
            ]),
            
            #email y teléfono
            ft.Column(spacing=3, controls=[
                crear_label("Email de contacto"),
                input_email,
            ]),
            ft.Column(spacing=3, controls=[
                crear_label("Teléfono"),
                input_telefono,
            ]),
            
            #presupuesto
            ft.Column(spacing=3, controls=[
                crear_label("Presupuesto anual"),
                input_presupuesto,
            ]),
            
            #estado
            ft.Column(spacing=3, controls=[
                crear_label("Estado"),
                dropdown_estado,
            ]),
        ]
    )

    #botón crear departamento
    btn_crear = ft.Container(
        width=200,
        height=44,
        bgcolor=COLOR_BTN_CREAR,
        border_radius=22,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_crear_click,
        content=ft.Text("Crear Departamento", color="white", weight=ft.FontWeight.BOLD, size=14),
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
            padding=ft.padding.only(left=20, right=20, top=55, bottom=25),
            content=ft.Column(
                spacing=15,
                tight=True,
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
        width=260,
        height=50,
        bgcolor=COLOR_HEADER_BG,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            "CREAR DEPARTAMENTO",
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
                    left=60,
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
    page.title = "App Tareas - Crear Departamento"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 400
    page.window.min_height = 700
    page.padding = 0 
    
    vista = VistaCrearDepartamento(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)