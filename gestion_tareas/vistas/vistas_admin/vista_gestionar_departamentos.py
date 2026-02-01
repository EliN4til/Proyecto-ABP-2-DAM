import flet as ft
from modelos.crud import obtener_todos_departamentos, eliminar_departamento, actualizar_departamento, obtener_todos_proyectos

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

    # Variables para almacenar datos reales de la base de datos
    departamentos_db = []
    proyectos_db = []

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

    def cargar_datos_maestros():
        """Consulta la base de datos para traer departamentos y proyectos"""
        nonlocal departamentos_db, proyectos_db
        
        exito_d, list_d = obtener_todos_departamentos()
        if exito_d: departamentos_db = list_d
        
        exito_p, list_p = obtener_todos_proyectos()
        if exito_p: proyectos_db = list_p

    def actualizar_lista_ui():
        """Aplica filtros sobre los datos cargados y repinta las tarjetas"""
        texto = input_busqueda.value.lower() if input_busqueda.value else ""
        
        filtrados = []
        for d in departamentos_db:
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
            filtrados.sort(key=lambda x: x.get("nombre", "").lower())
        elif filtro_orden_actual[0] == "Nombre Z-A":
            filtrados.sort(key=lambda x: x.get("nombre", "").lower(), reverse=True)

        lista_departamentos.controls = []
        if not filtrados:
            lista_departamentos.controls.append(
                ft.Container(padding=20, content=ft.Text("No hay departamentos registrados", color="grey", text_align="center"))
            )
        else:
            for depto in filtrados:
                lista_departamentos.controls.append(crear_tarjeta_departamento(depto))
        
        texto_contador.value = f"{len(filtrados)} departamentos"
        page.update()

    def refrescar_pantalla_completa():
        """Vuelve a pedir datos a la BD y actualiza todo"""
        cargar_datos_maestros()
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
        """Navega a la vista de creación"""
        page.go("/crear_departamento")

    # --- DIÁLOGOS DE GESTIÓN ---

    def mostrar_detalle_departamento(depto):
        """Muestra el diálogo con el detalle del departamento"""
        estado = depto.get("estado", "ACTIVO")
        estado_color = COLOR_ACTIVO if estado == "ACTIVO" else (COLOR_INACTIVO if estado == "INACTIVO" else COLOR_EN_CREACION)
        
        dialog_detalle = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text(depto.get("nombre", "Sin nombre"), size=16, weight="bold", color="black"),
            content=ft.Container(
                width=300,
                bgcolor="white",
                content=ft.Column(
                    spacing=12,
                    tight=True,
                    controls=[
                        ft.Row(
                            alignment="spaceBetween",
                            controls=[
                                ft.Text(f"Código: {depto.get('codigo', 'N/A')}", size=12, color=COLOR_LABEL),
                                ft.Container(bgcolor=estado_color, border_radius=10, padding=ft.padding.symmetric(horizontal=10, vertical=3), content=ft.Text(estado, size=10, color="white", weight="bold")),
                            ]
                        ),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        ft.Column([ft.Text("Responsable", size=10, color=COLOR_LABEL), ft.Text(depto.get("responsable", "No asignado"), size=12, color="black")], spacing=2),
                        ft.Column([ft.Text("Empresa", size=10, color=COLOR_LABEL), ft.Text(depto.get("empresa", "N/A"), size=12, color="black")], spacing=2),
                        ft.Column([ft.Text("Proyecto Vinculado", size=10, color=COLOR_LABEL), ft.Text(depto.get("proyecto_asignado", "Ninguno"), size=12, color="black")], spacing=2),
                        ft.Row([
                            ft.Column([ft.Text("Ubicación", size=10, color=COLOR_LABEL), ft.Text(depto.get("ubicacion", "N/A"), size=11, color="black")], expand=True),
                            ft.Column([ft.Text("Presupuesto", size=10, color=COLOR_LABEL), ft.Text(f"{depto.get('presupuesto', 0)}€", size=11, color="black")], horizontal_alignment="end"),
                        ]),
                    ]
                ),
            ),
            actions=[
                ft.TextButton(
                    content=ft.Text("Cerrar", color="black"), 
                    on_click=lambda e: setattr(dialog_detalle, 'open', False) or page.update()
                )
            ],
        )
        page.overlay.append(dialog_detalle)
        dialog_detalle.open = True
        page.update()

    def mostrar_editar_departamento(depto):
        """Muestra el diálogo para editar TODOS los campos del departamento"""
        
        input_nom = ft.TextField(label="Nombre del Departamento", value=depto.get("nombre"), border_color=COLOR_BORDE, text_size=12)
        input_cod = ft.TextField(label="Código", value=depto.get("codigo"), border_color=COLOR_BORDE, text_size=12)
        input_resp = ft.TextField(label="Responsable", value=depto.get("responsable"), border_color=COLOR_BORDE, text_size=12)
        input_email = ft.TextField(label="Email de contacto", value=depto.get("email"), border_color=COLOR_BORDE, text_size=12)
        input_tel = ft.TextField(label="Teléfono", value=depto.get("telefono"), border_color=COLOR_BORDE, text_size=12)
        input_ubi = ft.TextField(label="Ubicación", value=depto.get("ubicacion"), border_color=COLOR_BORDE, text_size=12)
        input_pres = ft.TextField(label="Presupuesto Anual (€)", value=str(depto.get("presupuesto", 0)), border_color=COLOR_BORDE, text_size=12)
        input_desc = ft.TextField(label="Descripción", value=depto.get("descripcion"), border_color=COLOR_BORDE, text_size=12, multiline=True, min_lines=2)

        dropdown_est = ft.DropdownM2(
            label="Estado", value=depto.get("estado"), border_color=COLOR_BORDE,
            options=[ft.dropdownm2.Option(opt) for opt in ["ACTIVO", "INACTIVO", "EN CREACIÓN"]]
        )

        opciones_proy = [ft.dropdownm2.Option("Sin proyecto")]
        for p in proyectos_db:
            opciones_proy.append(ft.dropdownm2.Option(p["nombre"]))

        dropdown_proy = ft.DropdownM2(
            label="Vincular a Proyecto",
            value=depto.get("proyecto_asignado", "Sin proyecto"),
            border_color=COLOR_BORDE,
            options=opciones_proy
        )

        def guardar_cambios_click(e):
            if not input_nom.value:
                page.snack_bar = ft.SnackBar(ft.Text("❌ El nombre es obligatorio"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return

            try:
                p_val = float(input_pres.value.replace(",", "."))
            except:
                p_val = 0.0

            datos_actualizados = {
                "nombre": input_nom.value,
                "codigo": input_cod.value,
                "responsable": input_resp.value,
                "email": input_email.value,
                "telefono": input_tel.value,
                "ubicacion": input_ubi.value,
                "presupuesto": p_val,
                "descripcion": input_desc.value,
                "estado": dropdown_est.value,
                "proyecto_asignado": dropdown_proy.value
            }

            exito, msj = actualizar_departamento(depto["_id"], datos_actualizados)
            if exito:
                page.snack_bar = ft.SnackBar(ft.Text(f"✅ Departamento actualizado"), bgcolor="green")
                dialog_editar.open = False
                refrescar_pantalla_completa()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {msj}"), bgcolor="red")
            
            page.snack_bar.open = True
            page.update()

        dialog_editar = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text(f"Editar: {depto.get('nombre')}", size=16, weight="bold", color="black"),
            content=ft.Container(
                width=350, height=500,
                content=ft.Column([
                    ft.Text("Modifica los detalles del departamento:", size=11, color="#666666"),
                    input_nom, input_cod, input_resp, dropdown_proy, dropdown_est,
                    input_email, input_tel, input_ubi, input_pres, input_desc,
                ], scroll="auto", spacing=15)
            ),
            actions=[
                ft.TextButton(
                    content=ft.Text("Cancelar", color="black"), 
                    on_click=lambda e: setattr(dialog_editar, 'open', False) or page.update()
                ),
                ft.ElevatedButton(
                    content=ft.Text("Guardar Cambios", color="white", weight="bold"), 
                    bgcolor=COLOR_BTN_CREAR, 
                    on_click=guardar_cambios_click
                ),
            ],
            actions_alignment="end",
        )
        page.overlay.append(dialog_editar)
        dialog_editar.open = True
        page.update()

    def mostrar_confirmar_eliminar(depto):
        """Muestra el diálogo de confirmación corregido para eliminar departamento"""
        def confirmar_eliminar(e):
            exito, msj = eliminar_departamento(depto["_id"])
            if exito:
                page.snack_bar = ft.SnackBar(ft.Text(f"✅ Departamento eliminado"), bgcolor="green")
                dialog_confirmar.open = False
                refrescar_pantalla_completa()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {msj}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

        dialog_confirmar = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text("Eliminar departamento", size=16, weight="bold", color="black"),
            content=ft.Container(
                width=280,
                content=ft.Column([
                    ft.Text("¿Estás seguro de que deseas eliminar este departamento?", size=12, color="black"),
                    ft.Container(bgcolor="#FFF3F3", border_radius=8, padding=10, content=ft.Text(depto.get("nombre"), size=13, weight="bold", color="black")),
                    ft.Text("Esta acción no se puede deshacer.", size=11, color=COLOR_ELIMINAR, italic=True),
                ], tight=True, spacing=10)
            ),
            actions=[
                ft.TextButton(
                    content=ft.Text("Cancelar", color="black"), 
                    on_click=lambda e: setattr(dialog_confirmar, 'open', False) or page.update()
                ),
                ft.ElevatedButton(
                    content=ft.Text("Eliminar", color="white", weight="bold"), 
                    bgcolor=COLOR_ELIMINAR, 
                    on_click=confirmar_eliminar
                ),
            ],
        )
        page.overlay.append(dialog_confirmar)
        dialog_confirmar.open = True
        page.update()

    # --- DIÁLOGOS DE FILTRO ---

    def mostrar_dialog_filtros(e):
        radio_estado = ft.RadioGroup(
            value=filtro_estado_actual[0],
            content=ft.Column([ft.Radio(value=est, label=est, label_style=ft.TextStyle(color="black", size=12)) for est in FILTROS_ESTADO], spacing=2)
        )
        radio_orden = ft.RadioGroup(
            value=filtro_orden_actual[0],
            content=ft.Column([ft.Radio(value=ord, label=ord, label_style=ft.TextStyle(color="black", size=12)) for ord in FILTROS_ORDEN], spacing=2)
        )

        def aplicar_filtros(e):
            filtro_estado_actual[0] = radio_estado.value
            filtro_orden_actual[0] = radio_orden.value
            dialog_filtros.open = False
            actualizar_lista_ui()

        dialog_filtros = ft.AlertDialog(
            modal=True, bgcolor="white",
            title=ft.Text("Filtrar departamentos", size=16, weight="bold", color="black"),
            content=ft.Container(width=300, height=350, content=ft.Column([
                ft.Text("Por Estado:", size=13, weight="bold", color=COLOR_LABEL), radio_estado,
                ft.Divider(),
                ft.Text("Ordenar por:", size=13, weight="bold", color=COLOR_LABEL), radio_orden,
            ], scroll="auto")),
            actions=[
                ft.TextButton(content=ft.Text("Limpiar", color="black"), on_click=lambda e: refrescar_pantalla_completa() or (dialog_filtros.__setattr__('open', False) or page.update())),
                ft.TextButton(content=ft.Text("Aplicar", color=COLOR_LABEL), on_click=aplicar_filtros),
            ],
        )
        page.overlay.append(dialog_filtros)
        dialog_filtros.open = True
        page.update()

    # --- RENDERIZADO DE TARJETAS ---

    def crear_tarjeta_departamento(departamento):
        estado = departamento.get("estado", "ACTIVO")
        estado_color = COLOR_ACTIVO if estado == "ACTIVO" else (COLOR_INACTIVO if estado == "INACTIVO" else COLOR_EN_CREACION)
        
        return ft.Container(
            bgcolor="white", border_radius=10, padding=10, margin=ft.margin.only(bottom=8),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=4, color=COLOR_SOMBRA_TARJETAS, offset=ft.Offset(0, 2)),
            content=ft.Row(
                spacing=8,
                vertical_alignment="center",
                controls=[
                    ft.Container(
                        expand=True, on_click=lambda e, d=departamento: mostrar_detalle_departamento(d), ink=True,
                        content=ft.Column([
                            ft.Row([ft.Text(departamento.get("nombre", "Sin nombre"), size=12, color="black", weight="bold", max_lines=1, overflow="ellipsis"), ft.Container(width=10, height=10, border_radius=5, bgcolor=estado_color)], alignment="spaceBetween"),
                            ft.Row([ft.Text(departamento.get("codigo", "N/A"), size=10, color=COLOR_LABEL), ft.Text(f"Proyecto: {departamento.get('proyecto_asignado', 'Ninguno')[:12]}...", size=10, color="#666666")], alignment="spaceBetween"),
                        ], spacing=3),
                    ),
                    ft.Container(content=ft.Icon(ft.Icons.EDIT, size=18, color=COLOR_EDITAR), on_click=lambda e, d=departamento: mostrar_editar_departamento(d), ink=True, padding=5, border_radius=5),
                    ft.Container(content=ft.Icon(ft.Icons.DELETE, size=18, color=COLOR_ELIMINAR), on_click=lambda e, d=departamento: mostrar_confirmar_eliminar(d), ink=True, padding=5, border_radius=5),
                ]
            ),
        )

    # --- ESTRUCTURA DE LA PÁGINA ---

    btn_volver = ft.Container(content=ft.Text("←", size=24, color="white", weight="bold"), on_click=btn_volver_click, ink=True, padding=10)

    input_busqueda = ft.TextField(
        hint_text="Buscar por nombre...", border_color=COLOR_BORDE, border_radius=5, height=38, expand=True,
        on_submit=lambda e: actualizar_lista_ui()
    )

    btn_filtrar = ft.Container(
        content=ft.Text("Filtrar", size=11, color="black"),
        bgcolor="white", border=ft.border.all(1, COLOR_BORDE), border_radius=5,
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
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
        width=180, height=44, bgcolor=COLOR_BTN_CREAR, border_radius=22, alignment=ft.Alignment(0, 0), ink=True,
        on_click=btn_crear_departamento_click,
        content=ft.Text("Crear Departamento", color="white", weight=ft.FontWeight.BOLD, size=13),
    )

    tarjeta_blanca = ft.Container(
        width=380, bgcolor="white", border_radius=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color=COLOR_SOMBRA, offset=ft.Offset(0, 5)),
        content=ft.Container(
            padding=ft.padding.only(left=18, right=18, top=55, bottom=20),
            content=ft.Column([
                ft.Row([input_busqueda, btn_filtrar, btn_buscar], spacing=8),
                texto_contador,
                ft.Container(height=390, content=lista_departamentos),
                ft.Row([btn_crear], alignment="center"),
            ], spacing=10)
        )
    )

    header_flotante = ft.Container(
        width=320, height=50, bgcolor=COLOR_HEADER_BG, border_radius=25, alignment=ft.Alignment(0, 0),
        content=ft.Text("GESTIONAR DEPARTAMENTOS", size=17, weight="bold", color="white")
    )

    contenido_superpuesto = ft.Container(
        width=380, height=620,
        content=ft.Stack([
            ft.Container(content=tarjeta_blanca, top=30),
            ft.Container(content=header_flotante, top=0, left=30)
        ])
    )

    # --- INICIALIZACIÓN ---
    refrescar_pantalla_completa()

    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[COLOR_FONDO_TOP, COLOR_FONDO_BOT]),
        content=ft.Stack([
            ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=contenido_superpuesto),
            ft.Container(content=btn_volver, top=10, left=10)
        ])
    )

# Para probar directamente
def main(page: ft.Page):
    page.title = "App Tareas - Gestionar Departamentos"
    page.window.width = 1200
    page.window.height = 800
    page.padding = 0 
    vista = VistaGestionarDepartamentos(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)