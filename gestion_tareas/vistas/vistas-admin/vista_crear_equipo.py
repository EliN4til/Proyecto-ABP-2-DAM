import flet as ft

def VistaCrearEquipo(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_BTN_CREAR = "#4682B4"

    #opciones para los dropdowns
    EMPRESAS = ["TechSolutions S.L", "InnovateTech Corp", "Digital Systems S.A", "CloudNet Solutions"]
    DEPARTAMENTOS = ["Desarrollo", "Diseño", "QA", "DevOps", "Backend", "Frontend", "Documentación", "Base de Datos", "Recursos Humanos", "Finanzas"]
    ESTADOS = ["ACTIVO", "INACTIVO", "EN FORMACIÓN"]
    METODOLOGIAS = ["Scrum", "Kanban", "Waterfall", "Agile", "Híbrido", "Sin definir"]
    LIDERES = [
        "Ana García (EMP001 - Tech Lead)", 
        "Carlos López (EMP002 - Senior Dev)", 
        "María Rodríguez (EMP003 - QA Lead)", 
        "Pedro Martínez (EMP004 - DevOps Lead)",
        "Laura Sánchez (EMP005 - Backend Lead)",
        "Juan Fernández (EMP006 - Frontend Lead)",
    ]
    MIEMBROS = [
        "Ana García (EMP001)",
        "Carlos López (EMP002)",
        "María Rodríguez (EMP003)",
        "Pedro Martínez (EMP004)",
        "Laura Sánchez (EMP005)",
        "Juan Fernández (EMP006)",
        "Sofia Ruiz (EMP007)",
        "Diego Torres (EMP008)",
    ]

    #lista de miembros seleccionados
    miembros_seleccionados = []

    def btn_volver_click(e):
        """Acción al hacer clic en el botón volver atrás"""
        page.snack_bar = ft.SnackBar(ft.Text("Volver atrás"))
        page.snack_bar.open = True
        page.update()

    def btn_crear_click(e):
        """Acción al hacer clic en el botón crear equipo"""
        #validar campos obligatorios
        if not input_nombre.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa los campos obligatorios"))
            page.snack_bar.open = True
            page.update()
            return
        
        page.snack_bar = ft.SnackBar(ft.Text(f"Equipo '{input_nombre.value}' creado correctamente"))
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

    #texto para mostrar miembros seleccionados
    texto_miembros_seleccionados = ft.Text(
        "Selecciona miembros...", 
        size=11, 
        color="#999999",
        max_lines=1,
        overflow=ft.TextOverflow.ELLIPSIS,
    )

    #dialog para seleccionar miembros
    def mostrar_dialog_miembros(e):
        """Muestra el diálogo para seleccionar miembros del equipo"""
        checkboxes_miembros = []
        
        def on_checkbox_change(e):
            miembro = e.control.data
            if e.control.value:
                if miembro not in miembros_seleccionados:
                    miembros_seleccionados.append(miembro)
            else:
                if miembro in miembros_seleccionados:
                    miembros_seleccionados.remove(miembro)
        
        for miembro in MIEMBROS:
            cb = ft.Checkbox(
                label=miembro,
                value=miembro in miembros_seleccionados,
                data=miembro,
                on_change=on_checkbox_change,
                label_style=ft.TextStyle(size=12, color="black"),
            )
            checkboxes_miembros.append(cb)
        
        def cerrar_dialog(e):
            dialog_miembros.open = False
            #actualizar texto
            if len(miembros_seleccionados) == 0:
                texto_miembros_seleccionados.value = "Selecciona miembros..."
                texto_miembros_seleccionados.color = "#999999"
            elif len(miembros_seleccionados) == 1:
                texto_miembros_seleccionados.value = miembros_seleccionados[0]
                texto_miembros_seleccionados.color = "black"
            else:
                texto_miembros_seleccionados.value = f"{len(miembros_seleccionados)} miembros seleccionados"
                texto_miembros_seleccionados.color = "black"
            page.update()
        
        dialog_miembros = ft.AlertDialog(
            modal=True,
            title=ft.Text("Seleccionar Miembros", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=300,
                bgcolor="white",
                content=ft.ListView(
                    controls=checkboxes_miembros,
                    spacing=5,
                ),
            ),
            actions=[
                ft.TextButton("Aceptar", on_click=cerrar_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.overlay.append(dialog_miembros)
        dialog_miembros.open = True
        page.update()

    #contenedor clickeable para miembros (simula dropdown multiselect)
    selector_miembros = ft.Container(
        content=ft.Row(
            controls=[
                texto_miembros_seleccionados,
                ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=20, color="#666666"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor="white",
        border=ft.border.all(1, COLOR_BORDE),
        border_radius=5,
        padding=ft.padding.only(left=10, right=5, top=10, bottom=10),
        on_click=mostrar_dialog_miembros,
        ink=True,
    )

    #botón volver
    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight=ft.FontWeight.BOLD),
        on_click=btn_volver_click,
        ink=True,
        padding=10,
    )

    #campos del formulario
    input_nombre = crear_campo_texto("Nombre del equipo")
    input_codigo = crear_campo_texto("Ej: TEAM-DEV, TEAM-QA...")
    input_descripcion = crear_campo_texto("Descripción y objetivos del equipo...", multiline=True, min_lines=3)
    input_capacidad = crear_campo_texto("Número máximo de miembros")

    dropdown_empresa = crear_dropdown(EMPRESAS, "Selecciona empresa...")
    dropdown_departamento = crear_dropdown(DEPARTAMENTOS, "Selecciona departamento...")
    dropdown_lider = crear_dropdown(LIDERES, "Selecciona líder...")
    dropdown_metodologia = crear_dropdown(METODOLOGIAS, "Selecciona metodología...")
    dropdown_estado = crear_dropdown(ESTADOS, "Selecciona estado...")

    #contenido del formulario
    formulario = ft.Column(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            #nombre del equipo
            ft.Column(spacing=3, controls=[
                crear_label("Nombre del Equipo *"),
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
            
            #departamento
            ft.Column(spacing=3, controls=[
                crear_label("Departamento"),
                dropdown_departamento,
            ]),
            
            #líder del equipo
            ft.Column(spacing=3, controls=[
                crear_label("Líder del Equipo"),
                dropdown_lider,
            ]),
            
            #miembros (multiselect)
            ft.Column(spacing=3, controls=[
                crear_label("Miembros del Equipo"),
                selector_miembros,
            ]),
            
            #descripción
            ft.Column(spacing=3, controls=[
                crear_label("Descripción"),
                input_descripcion,
            ]),
            
            #metodología
            ft.Column(spacing=3, controls=[
                crear_label("Metodología de trabajo"),
                dropdown_metodologia,
            ]),
            
            #capacidad
            ft.Column(spacing=3, controls=[
                crear_label("Capacidad máxima"),
                input_capacidad,
            ]),
            
            #estado
            ft.Column(spacing=3, controls=[
                crear_label("Estado"),
                dropdown_estado,
            ]),
        ]
    )

    #botón crear equipo
    btn_crear = ft.Container(
        width=180,
        height=44,
        bgcolor=COLOR_BTN_CREAR,
        border_radius=22,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_crear_click,
        content=ft.Text("Crear Equipo", color="white", weight=ft.FontWeight.BOLD, size=14),
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
        width=220,
        height=50,
        bgcolor=COLOR_HEADER_BG,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            "CREAR EQUIPO",
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
    page.title = "App Tareas - Crear Equipo"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 400
    page.window.min_height = 700
    page.padding = 0 
    
    vista = VistaCrearEquipo(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)