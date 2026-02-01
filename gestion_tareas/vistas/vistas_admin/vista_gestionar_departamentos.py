import flet as ft
from modelos.crud import obtener_todos_departamentos, eliminar_departamento, actualizar_departamento

def VistaGestionarDepartamentos(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_SOMBRA_TARJETAS = "#30000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_ACTIVO = "#4CAF50"
    COLOR_INACTIVO = "#F44336"
    COLOR_EN_CREACION = "#FF9800"
    COLOR_EDITAR = "#2196F3"
    COLOR_ELIMINAR = "#E53935"
    COLOR_BTN_CREAR = "#4682B4"

    # Variable para almacenar los departamentos reales de la BD
    deptos_db = []

    #opciones de filtro
    FILTROS_ESTADO = ["Todos", "ACTIVO", "INACTIVO", "EN CREACIÓN"]
    FILTROS_ORDEN = [
        "Nombre A-Z",
        "Nombre Z-A",
        "Más empleados",
        "Menos empleados",
    ]

    filtro_estado_actual = ["Todos"]
    filtro_orden_actual = ["Nombre A-Z"]

    # --- LÓGICA DE DATOS ---

    def cargar_departamentos_real():
        """Obtiene los departamentos desde la base de datos MongoDB"""
        exito, resultado = obtener_todos_departamentos()
        if exito:
            return resultado
        return []

    def actualizar_lista_ui():
        """Aplica filtros a los datos cargados y actualiza la interfaz"""
        texto = input_busqueda.value.lower() if input_busqueda.value else ""
        
        filtrados = []
        for d in deptos_db:
            nombre = d.get("nombre", "").lower()
            # Filtro búsqueda
            if texto and texto not in nombre:
                continue
            # Filtro estado
            if filtro_estado_actual[0] != "Todos" and d.get("estado") != filtro_estado_actual[0]:
                continue
            filtrados.append(d)

        # Ordenación
        if filtro_orden_actual[0] == "Nombre A-Z":
            filtrados.sort(key=lambda x: x.get("nombre", ""))
        elif filtro_orden_actual[0] == "Nombre Z-A":
            filtrados.sort(key=lambda x: x.get("nombre", ""), reverse=True)

        lista_departamentos.controls = []
        if not filtrados:
            lista_departamentos.controls.append(
                ft.Container(padding=20, content=ft.Text("No se encontraron departamentos", color="grey"))
            )
        else:
            for depto in filtrados:
                lista_departamentos.controls.append(crear_tarjeta_departamento(depto))
        
        texto_contador.value = f"{len(filtrados)} departamentos"
        page.update()

    def refrescar_todo():
        """Recarga datos de la BD y refresca la UI"""
        nonlocal deptos_db
        deptos_db = cargar_departamentos_real()
        actualizar_lista_ui()

    def btn_volver_click(e):
        """Acción al hacer clic en el botón volver atrás - CORREGIDO A ADMIN"""
        page.go("/area_admin")

    def btn_buscar_click(e):
        """Acción al hacer clic en el botón buscar"""
        actualizar_lista_ui()
        page.snack_bar = ft.SnackBar(ft.Text(f"Buscando: {input_busqueda.value}"))
        page.snack_bar.open = True
        page.update()

    def btn_crear_departamento_click(e):
        """Navega a la vista de creación de departamento"""
        page.go("/crear_departamento")

    # --- DIÁLOGOS CRUD ---

    #dialog detalle departamento
    def mostrar_detalle_departamento(depto):
        """Muestra el diálogo con el detalle del departamento"""
        estado = depto.get("estado", "ACTIVO")
        estado_color = COLOR_ACTIVO if estado == "ACTIVO" else (COLOR_INACTIVO if estado == "INACTIVO" else COLOR_EN_CREACION)
        
        dialog_detalle = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text(depto.get("nombre", "Sin nombre"), size=16, weight=ft.FontWeight.BOLD, color="black"),
            content=ft.Container(
                width=300,
                bgcolor="white",
                content=ft.Column(
                    spacing=12,
                    tight=True,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"Código: {depto.get('codigo', 'N/A')}", size=12, color=COLOR_LABEL),
                                ft.Container(
                                    bgcolor=estado_color,
                                    border_radius=10,
                                    padding=ft.padding.only(left=10, right=10, top=3, bottom=3),
                                    content=ft.Text(estado, size=10, color="white", weight=ft.FontWeight.BOLD),
                                ),
                            ]
                        ),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Responsable", size=11, color=COLOR_LABEL),
                            ft.Text(depto.get("responsable", "No asignado"), size=12, color="black"),
                        ]),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Email", size=11, color=COLOR_LABEL),
                            ft.Text(depto.get("email", "N/A"), size=12, color="black"),
                        ]),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Ubicación", size=11, color=COLOR_LABEL),
                            ft.Text(depto.get("ubicacion", "N/A"), size=12, color="black"),
                        ]),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(spacing=2, controls=[
                                    ft.Text("Presupuesto", size=11, color=COLOR_LABEL),
                                    ft.Text(f"{depto.get('presupuesto', 0)} €", size=12, color="black"),
                                ]),
                                ft.Column(spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END, controls=[
                                    ft.Text("Teléfono", size=11, color=COLOR_LABEL),
                                    ft.Text(depto.get("telefono", "N/A"), size=12, color="black"),
                                ]),
                            ]
                        ),
                    ]
                ),
            ),
            actions=[
                ft.TextButton(content=ft.Text("Cerrar", color="black"), on_click=lambda e: cerrar_dialog(dialog_detalle)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_detalle)
        dialog_detalle.open = True
        page.update()

    #dialog editar departamento
    def mostrar_editar_departamento(depto):
        """Muestra el diálogo para editar departamento real"""
        
        input_nom = ft.TextField(label="Nombre", value=depto.get("nombre"), border_color=COLOR_BORDE, height=50, text_size=12)
        input_resp = ft.TextField(label="Responsable", value=depto.get("responsable"), border_color=COLOR_BORDE, height=50, text_size=12)
        input_mail = ft.TextField(label="Email", value=depto.get("email"), border_color=COLOR_BORDE, height=50, text_size=12)
        dropdown_est = ft.DropdownM2(
            label="Estado", value=depto.get("estado"), border_color=COLOR_BORDE, height=50,
            options=[ft.dropdownm2.Option(opt) for opt in ["ACTIVO", "INACTIVO", "EN CREACIÓN"]]
        )

        def guardar_cambios_click(e):
            datos = {
                "nombre": input_nom.value,
                "responsable": input_resp.value,
                "email": input_mail.value,
                "estado": dropdown_est.value
            }
            exito, msj = actualizar_departamento(depto["_id"], datos)
            if exito:
                page.snack_bar = ft.SnackBar(ft.Text(f"✅ Departamento '{input_nom.value}' actualizado"), bgcolor="green")
                dialog_editar.open = False
                refrescar_todo()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {msj}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

        dialog_editar = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text(f"Editar: {depto.get('nombre')}", size=16, weight=ft.FontWeight.BOLD, color="black"),
            content=ft.Container(
                width=300,
                content=ft.Column([input_nom, input_resp, input_mail, dropdown_est], tight=True, spacing=10)
            ),
            actions=[
                ft.TextButton(content=ft.Text("Cancelar", color="black"), on_click=lambda e: cerrar_dialog(dialog_editar)),
                ft.ElevatedButton(content=ft.Text("Guardar", color="white"), bgcolor=COLOR_BTN_CREAR, on_click=guardar_cambios_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_editar)
        dialog_editar.open = True
        page.update()

    #dialog confirmar eliminación
    def mostrar_confirmar_eliminar(depto):
        """Muestra el diálogo de confirmación para eliminar departamento real"""
        def confirmar_eliminar(e):
            exito, msj = eliminar_departamento(depto["_id"])
            if exito:
                page.snack_bar = ft.SnackBar(ft.Text(f"✅ Departamento '{depto.get('nombre')}' eliminado"), bgcolor="green")
                dialog_confirmar.open = False
                refrescar_todo()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {msj}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

        dialog_confirmar = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text("Eliminar departamento", size=16, weight=ft.FontWeight.BOLD, color="black"),
            content=ft.Container(
                width=280,
                content=ft.Column(
                    spacing=10,
                    tight=True,
                    controls=[
                        ft.Text("¿Estás seguro de que deseas eliminar este departamento?", size=12, color="black"),
                        ft.Container(
                            bgcolor="#FFF3F3",
                            border_radius=8,
                            padding=10,
                            content=ft.Column(
                                spacing=3,
                                controls=[
                                    ft.Text(depto.get("nombre"), size=13, color="black", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Código: {depto.get('codigo')}", size=11, color="#666666"),
                                ],
                            ),
                        ),
                        ft.Text("Esta acción no se puede deshacer.", size=11, color=COLOR_ELIMINAR, italic=True),
                    ]
                ),
            ),
            actions=[
                ft.TextButton(content=ft.Text("Cancelar", color="black"), on_click=lambda e: cerrar_dialog(dialog_confirmar)),
                ft.TextButton(content=ft.Text("Eliminar", color="white"), on_click=confirmar_eliminar, style=ft.ButtonStyle(bgcolor=COLOR_ELIMINAR)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_confirmar)
        dialog_confirmar.open = True
        page.update()

    # --- DIÁLOGOS DE FILTRO ---

    def mostrar_dialog_filtros(e):
        radio_estado = ft.RadioGroup(
            value=filtro_estado_actual[0],
            content=ft.Column([ft.Radio(value=estado, label=estado, label_style=ft.TextStyle(color="black", size=12)) for estado in FILTROS_ESTADO])
        )
        radio_orden = ft.RadioGroup(
            value=filtro_orden_actual[0],
            content=ft.Column([ft.Radio(value=orden, label=orden, label_style=ft.TextStyle(color="black", size=12)) for orden in FILTROS_ORDEN])
        )

        def aplicar_filtros(e):
            filtro_estado_actual[0] = radio_estado.value
            filtro_orden_actual[0] = radio_orden.value
            dialog_filtros.open = False
            actualizar_lista_ui()

        dialog_filtros = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text("Filtrar departamentos", size=16, weight=ft.FontWeight.BOLD, color="black"),
            content=ft.Container(
                width=300, height=350,
                content=ft.Column([
                    ft.Text("Por Estado:", size=13, weight="bold", color=COLOR_LABEL), radio_estado,
                    ft.Divider(),
                    ft.Text("Ordenar por:", size=13, weight="bold", color=COLOR_LABEL), radio_orden,
                ], scroll="auto")
            ),
            actions=[
                ft.TextButton(content=ft.Text("Limpiar", color="black"), on_click=lambda e: refrescar_todo() or (dialog_filtros.__setattr__('open', False) or page.update())),
                ft.TextButton(content=ft.Text("Aplicar", color=COLOR_LABEL), on_click=aplicar_filtros),
            ],
        )
        page.overlay.append(dialog_filtros)
        dialog_filtros.open = True
        page.update()

    def cerrar_dialog(dialog):
        dialog.open = False
        page.update()

    # --- RENDERIZADO DE TARJETAS ---

    def crear_tarjeta_departamento(departamento):
        """Crea una tarjeta visual para cada departamento real"""
        estado = departamento.get("estado", "ACTIVO")
        estado_color = COLOR_ACTIVO if estado == "ACTIVO" else (COLOR_INACTIVO if estado == "INACTIVO" else COLOR_EN_CREACION)
        
        return ft.Container(
            bgcolor="white",
            border_radius=10,
            padding=ft.padding.all(10),
            margin=ft.margin.only(bottom=8),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=4, color=COLOR_SOMBRA_TARJETAS, offset=ft.Offset(0, 2)),
            content=ft.Row(
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # Contenido principal
                    ft.Container(
                        expand=True,
                        on_click=lambda e, d=departamento: mostrar_detalle_departamento(d),
                        ink=True,
                        content=ft.Column(
                            spacing=3,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(departamento.get("nombre", "Sin nombre"), size=12, color="black", weight=ft.FontWeight.BOLD, max_lines=1, overflow="ellipsis"),
                                        ft.Container(width=10, height=10, border_radius=5, bgcolor=estado_color),
                                    ]
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(departamento.get("codigo", "N/A"), size=10, color=COLOR_LABEL),
                                        ft.Text(f"Responsable: {departamento.get('responsable', 'Admin')[:10]}...", size=10, color="#666666"),
                                    ]
                                ),
                            ]
                        ),
                    ),
                    # Botones acción
                    ft.Container(content=ft.Icon(ft.Icons.EDIT, size=18, color=COLOR_EDITAR), on_click=lambda e, d=departamento: mostrar_editar_departamento(d), ink=True, padding=5),
                    ft.Container(content=ft.Icon(ft.Icons.DELETE, size=18, color=COLOR_ELIMINAR), on_click=lambda e, d=departamento: mostrar_confirmar_eliminar(d), ink=True, padding=5),
                ]
            ),
        )

    # --- ESTRUCTURA DE LA PÁGINA ---

    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight=ft.FontWeight.BOLD),
        on_click=btn_volver_click,
        ink=True,
        padding=10,
    )

    input_busqueda = ft.TextField(
        hint_text="Buscar por nombre...",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=38,
        expand=True,
        content_padding=ft.padding.only(left=10, top=8, bottom=8),
        on_submit=lambda e: actualizar_lista_ui()
    )

    btn_filtrar = ft.Container(
        content=ft.Text("Filtrar", size=11, color="black"),
        bgcolor="white", border=ft.border.all(1, COLOR_BORDE), border_radius=5,
        padding=ft.padding.only(left=12, right=12, top=8, bottom=8),
        on_click=mostrar_dialog_filtros, ink=True,
    )

    btn_buscar = ft.Container(
        content=ft.Icon(ft.Icons.SEARCH, size=20, color="white"),
        bgcolor=COLOR_LABEL, border_radius=5, padding=8,
        on_click=btn_buscar_click, ink=True,
    )

    texto_contador = ft.Text("0 departamentos", size=11, color=COLOR_LABEL)

    lista_departamentos = ft.ListView(spacing=0, expand=True)

    btn_crear = ft.Container(
        width=180, height=44, bgcolor=COLOR_BTN_CREAR, border_radius=22,
        alignment=ft.Alignment(0, 0), ink=True, on_click=btn_crear_departamento_click,
        content=ft.Text("Crear Departamento", color="white", weight=ft.FontWeight.BOLD, size=13),
    )

    # Tarjeta blanca principal
    tarjeta_blanca = ft.Container(
        width=380, bgcolor="white", border_radius=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color=COLOR_SOMBRA, offset=ft.Offset(0, 5)),
        content=ft.Container(
            padding=ft.padding.only(left=18, right=18, top=55, bottom=20),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row([input_busqueda, btn_filtrar, btn_buscar], spacing=8),
                    texto_contador,
                    ft.Container(height=390, content=lista_departamentos),
                    ft.Row([btn_crear], alignment=ft.MainAxisAlignment.CENTER),
                ]
            )
        )
    )

    header_flotante = ft.Container(
        width=320, height=50, bgcolor=COLOR_HEADER_BG, border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text("GESTIONAR DEPARTAMENTOS", size=17, weight=ft.FontWeight.BOLD, color="white")
    )

    contenido_superpuesto = ft.Container(
        width=380, height=620,
        content=ft.Stack([
            ft.Container(content=tarjeta_blanca, top=30),
            ft.Container(content=header_flotante, top=0, left=30)
        ])
    )

    # --- INICIALIZACIÓN ---
    refrescar_todo()

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
                ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=contenido_superpuesto),
                ft.Container(content=btn_volver, top=10, left=10)
            ]
        )
    )


#para probar directamente
def main(page: ft.Page):
    page.title = "App Tareas - Gestionar Departamentos"
    page.window.width = 1200
    page.window.height = 800
    page.padding = 0 
    vista = VistaGestionarDepartamentos(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)