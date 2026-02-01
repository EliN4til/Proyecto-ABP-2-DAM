import flet as ft
from modelos.crud import obtener_todos_proyectos, eliminar_proyecto, actualizar_proyecto, obtener_todos_empleados
from datetime import datetime

def VistaGestionarProyectos(page: ft.Page):
    
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
    proyectos_db = []
    empleados_maestros = []

    #opciones de filtro
    FILTROS_ESTADO = ["Todos", "ACTIVO", "PAUSADO", "INACTIVO"]
    # El filtro de clientes se llenará dinámicamente con los datos de la BD
    FILTROS_CLIENTE = ["Todos"]
    FILTROS_ORDEN = [
        "Nombre A-Z",
        "Nombre Z-A",
        "Más reciente",
        "Más antiguo",
        "Por cliente",
    ]

    filtro_estado_actual = ["Todos"]
    filtro_cliente_actual = ["Todos"]
    filtro_orden_actual = ["Nombre A-Z"]

    # --- LÓGICA DE BASE DE DATOS ---

    def cargar_datos_maestros():
        """Consulta la base de datos para traer proyectos y empleados reales"""
        nonlocal proyectos_db, empleados_maestros, FILTROS_CLIENTE
        
        exito_p, list_p = obtener_todos_proyectos()
        if exito_p: 
            proyectos_db = list_p
            # Extraemos clientes únicos para el filtro
            set_clientes = set()
            for p in proyectos_db:
                if p.get("cliente"): set_clientes.add(p.get("cliente"))
            FILTROS_CLIENTE = ["Todos"] + sorted(list(set_clientes))
        
        exito_e, list_e = obtener_todos_empleados()
        if exito_e: empleados_maestros = list_e

    def actualizar_lista_ui():
        """Aplica filtros y búsqueda sobre los datos de la memoria y repinta las tarjetas"""
        texto = input_busqueda.value.lower() if input_busqueda.value else ""
        
        filtrados = []
        for p in proyectos_db:
            nombre = p.get("nombre", "").lower()
            cliente = p.get("cliente", "").lower()
            
            # 1. Filtro búsqueda (por nombre o cliente)
            if texto and (texto not in nombre and texto not in cliente):
                continue
            
            # 2. Filtro estado
            if filtro_estado_actual[0] != "Todos" and p.get("estado") != filtro_estado_actual[0]:
                continue
            
            # 3. Filtro cliente
            if filtro_cliente_actual[0] != "Todos" and p.get("cliente") != filtro_cliente_actual[0]:
                continue
                
            filtrados.append(p)

        # 4. Ordenación
        if filtro_orden_actual[0] == "Nombre A-Z":
            filtrados.sort(key=lambda x: x.get("nombre", "").lower())
        elif filtro_orden_actual[0] == "Nombre Z-A":
            filtrados.sort(key=lambda x: x.get("nombre", "").lower(), reverse=True)

        # Limpiamos la lista y añadimos los resultados filtrados
        lista_proyectos.controls = []
        if not filtrados:
            lista_proyectos.controls.append(
                ft.Container(
                    padding=20, 
                    content=ft.Text("No se encontraron proyectos con los criterios seleccionados", color="grey", text_align="center")
                )
            )
        else:
            for proyecto in filtrados:
                lista_proyectos.controls.append(crear_tarjeta_proyecto(proyecto))
        
        texto_contador.value = f"{len(filtrados)} proyectos encontrados"
        page.update()

    def refrescar_datos_completos():
        """Sincroniza con la BD y actualiza la interfaz"""
        cargar_datos_maestros()
        actualizar_lista_ui()

    def btn_volver_click(e):
        """Acción al hacer clic en el botón volver atrás - CORREGIDO A DASHBOARD ADMIN"""
        page.go("/area_admin")

    def btn_buscar_click(e):
        """Acción al hacer clic en el botón buscar"""
        actualizar_lista_ui()
        page.snack_bar = ft.SnackBar(ft.Text(f"Buscando: {input_busqueda.value}"))
        page.snack_bar.open = True
        page.update()

    def btn_crear_proyecto_click(e):
        """Navega a la vista de creación de proyecto"""
        page.go("/crear_proyecto")

    # --- DIÁLOGOS DE GESTIÓN (CRUD REAL) ---

    #dialog detalle proyecto
    def mostrar_detalle_proyecto(proyecto):
        """Muestra el diálogo con el detalle completo del proyecto"""
        estado = proyecto.get("estado", "ACTIVO")
        estado_color = COLOR_ACTIVO if estado == "ACTIVO" else (COLOR_INACTIVO if estado == "INACTIVO" else COLOR_EN_CREACION)
        
        dialog_detalle = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text(proyecto.get("nombre", "Proyecto"), size=16, weight=ft.FontWeight.BOLD, color="black"),
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
                                ft.Text(f"Código: {proyecto.get('codigo', 'N/A')}", size=12, color=COLOR_LABEL),
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
                            ft.Text(proyecto.get("responsable", "No asignado"), size=12, color="black"),
                        ]),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Cliente / Empresa", size=11, color=COLOR_LABEL),
                            ft.Text(proyecto.get("cliente", "N/A"), size=12, color="black"),
                        ]),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Presupuesto Estimado", size=11, color=COLOR_LABEL),
                            ft.Text(f"{proyecto.get('presupuesto', '0')} €", size=12, color="black"),
                        ]),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(spacing=2, controls=[
                                    ft.Text("Fecha inicio", size=11, color=COLOR_LABEL),
                                    ft.Text(str(proyecto.get("fecha_inicio", "N/A"))[:10], size=12, color="black"),
                                ]),
                                ft.Column(spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END, controls=[
                                    ft.Text("Fecha fin", size=11, color=COLOR_LABEL),
                                    ft.Text(str(proyecto.get("fecha_fin", "N/A"))[:10], size=12, color="black"),
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

        def cerrar_dialog(dialog):
            dialog.open = False
            page.update()

        page.overlay.append(dialog_detalle)
        dialog_detalle.open = True
        page.update()

    #dialog editar proyecto
    def mostrar_editar_proyecto(proyecto):
        """Muestra el diálogo para editar TODOS los campos del proyecto de forma persistente"""
        
        # Campos de texto con los valores actuales
        input_nom = ft.TextField(label="Nombre del Proyecto", value=proyecto.get("nombre"), border_color=COLOR_BORDE, text_size=12)
        input_cli = ft.TextField(label="Cliente / Empresa", value=proyecto.get("cliente"), border_color=COLOR_BORDE, text_size=12)
        input_cod = ft.TextField(label="Código", value=proyecto.get("codigo"), border_color=COLOR_BORDE, text_size=12)
        input_pres = ft.TextField(label="Presupuesto (€)", value=str(proyecto.get("presupuesto", 0)), border_color=COLOR_BORDE, text_size=12)
        
        # Selectores
        dropdown_est = ft.DropdownM2(
            label="Estado", value=proyecto.get("estado"), border_color=COLOR_BORDE,
            options=[ft.dropdownm2.Option(opt) for opt in ["ACTIVO", "PAUSADO", "INACTIVO"]]
        )

        dropdown_resp = ft.DropdownM2(
            label="Responsable", value=proyecto.get("responsable"), border_color=COLOR_BORDE,
            options=[ft.dropdownm2.Option(f"{emp['nombre']} {emp['apellidos']}") for emp in empleados_maestros]
        )

        def guardar_cambios_click(e):
            if not input_nom.value or not input_cli.value:
                page.snack_bar = ft.SnackBar(ft.Text("❌ El nombre y el cliente son obligatorios"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return

            datos_actualizados = {
                "nombre": input_nom.value,
                "cliente": input_cli.value,
                "codigo": input_cod.value,
                "presupuesto": input_pres.value,
                "responsable": dropdown_resp.value,
                "estado": dropdown_est.value
            }

            exito, msj = actualizar_proyecto(proyecto["_id"], datos_actualizados)
            if exito:
                page.snack_bar = ft.SnackBar(ft.Text(f"✅ Proyecto actualizado correctamente"), bgcolor="green")
                dialog_editar.open = False
                refrescar_datos_completos()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error al actualizar: {msj}"), bgcolor="red")
            
            page.snack_bar.open = True
            page.update()

        dialog_editar = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text(f"Editar Proyecto", size=16, weight=ft.FontWeight.BOLD, color="black"),
            content=ft.Container(
                width=350,
                height=450,
                content=ft.Column([
                    ft.Text("Modifica los datos del proyecto:", size=11, color="#666666"),
                    input_nom,
                    input_cod,
                    input_cli,
                    dropdown_resp,
                    dropdown_est,
                    input_pres,
                ], scroll=ft.ScrollMode.AUTO, spacing=15)
            ),
            actions=[
                ft.TextButton(content=ft.Text("Cancelar", color="black"), on_click=lambda e: setattr(dialog_editar, 'open', False) or page.update()),
                ft.ElevatedButton(content=ft.Text("Guardar Cambios", color="white", weight="bold"), bgcolor=COLOR_BTN_CREAR, on_click=guardar_cambios_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_editar)
        dialog_editar.open = True
        page.update()

    #dialog confirmar eliminación
    def mostrar_confirmar_eliminar(proyecto):
        """Muestra el diálogo de confirmación para eliminar proyecto real"""
        def confirmar_eliminar(e):
            exito, msj = eliminar_proyecto(proyecto["_id"])
            if exito:
                page.snack_bar = ft.SnackBar(ft.Text(f"✅ Proyecto '{proyecto.get('nombre')}' eliminado"), bgcolor="green")
                dialog_confirmar.open = False
                refrescar_datos_completos()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error al eliminar: {msj}"), bgcolor="red")
            
            page.snack_bar.open = True
            page.update()

        dialog_confirmar = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text("Eliminar Proyecto", size=16, weight=ft.FontWeight.BOLD, color="black"),
            content=ft.Container(
                width=280,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    tight=True,
                    controls=[
                        ft.Text("¿Estás seguro de que deseas eliminar este proyecto?", size=12, color="black"),
                        ft.Container(
                            bgcolor="#FFF3F3",
                            border_radius=8,
                            padding=10,
                            content=ft.Column(
                                spacing=3,
                                controls=[
                                    ft.Text(proyecto.get("nombre"), size=13, color="black", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Cliente: {proyecto.get('cliente')}", size=11, color="#666666"),
                                ],
                            ),
                        ),
                        ft.Text("Esta acción eliminará el proyecto de la base de datos.", size=11, color=COLOR_ELIMINAR, italic=True),
                    ]
                ),
            ),
            actions=[
                ft.TextButton(content=ft.Text("Cancelar", color="black"), on_click=lambda e: setattr(dialog_confirmar, 'open', False) or page.update()),
                ft.ElevatedButton(content=ft.Text("Eliminar", color="white", weight="bold"), bgcolor=COLOR_ELIMINAR, on_click=confirmar_eliminar),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_confirmar)
        dialog_confirmar.open = True
        page.update()

    # --- DIÁLOGOS DE FILTRO ---

    def mostrar_dialog_filtros(e):
        """Muestra el diálogo de filtros principal"""
        radio_estado = ft.RadioGroup(
            value=filtro_estado_actual[0],
            content=ft.Column([ft.Radio(value=est, label=est, label_style=ft.TextStyle(color="black", size=12)) for est in FILTROS_ESTADO], spacing=2)
        )

        radio_orden = ft.RadioGroup(
            value=filtro_orden_actual[0],
            content=ft.Column([ft.Radio(value=ord, label=ord, label_style=ft.TextStyle(color="black", size=12)) for ord in FILTROS_ORDEN], spacing=2)
        )

        def aplicar_filtros_click(e):
            filtro_estado_actual[0] = radio_estado.value
            filtro_orden_actual[0] = radio_orden.value
            dialog_filtros.open = False
            actualizar_lista_ui()

        def abrir_filtro_cliente(e):
            dialog_filtros.open = False
            page.update()
            mostrar_dialog_cliente_filtro()

        dialog_filtros = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text("Filtrar proyectos", size=16, weight=ft.FontWeight.BOLD, color="black"),
            content=ft.Container(
                width=300,
                height=380,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("Por Estado:", size=13, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                        radio_estado,
                        ft.Divider(height=10, color=COLOR_BORDE),
                        ft.Text("Ordenar por:", size=13, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                        radio_orden,
                        ft.Divider(height=10, color=COLOR_BORDE),
                        ft.Container(
                            content=ft.Row([
                                ft.Text("Filtrar por Cliente", size=13, weight="bold", color=COLOR_LABEL),
                                ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=16, color=COLOR_LABEL)
                            ], alignment="spaceBetween"),
                            on_click=abrir_filtro_cliente,
                            ink=True, padding=10, border_radius=5, bgcolor="#F5F5F5",
                        ),
                    ],
                ),
            ),
            actions=[
                ft.TextButton(content=ft.Text("Limpiar", color="black"), on_click=lambda e: refrescar_datos_completos() or (dialog_filtros.__setattr__('open', False) or page.update())),
                ft.TextButton(content=ft.Text("Aplicar", color=COLOR_LABEL), on_click=aplicar_filtros_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_filtros)
        dialog_filtros.open = True
        page.update()

    def mostrar_dialog_cliente_filtro():
        """Diálogo secundario para filtrar por cliente extraído de la BD"""
        radio_cliente = ft.RadioGroup(
            value=filtro_cliente_actual[0],
            content=ft.Column([ft.Radio(value=cli, label=cli, label_style=ft.TextStyle(color="black", size=12)) for cli in FILTROS_CLIENTE], spacing=2)
        )

        def aplicar_cliente_click(e):
            filtro_cliente_actual[0] = radio_cliente.value
            dialog_cliente.open = False
            actualizar_lista_ui()

        dialog_cliente = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text("Seleccionar Cliente", size=14, weight=ft.FontWeight.BOLD, color="black"),
            content=ft.Container(width=300, height=300, content=ft.ListView(controls=[radio_cliente], spacing=5)),
            actions=[ft.TextButton("Aplicar", on_click=aplicar_cliente_click)],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_cliente)
        dialog_cliente.open = True
        page.update()

    # --- RENDERIZADO DE TARJETAS ---

    def crear_tarjeta_proyecto(proyecto):
        """Crea una tarjeta visual para cada proyecto real de la base de datos"""
        estado = proyecto.get("estado", "ACTIVO")
        estado_color = COLOR_ACTIVO if estado == "ACTIVO" else (COLOR_INACTIVO if estado == "INACTIVO" else COLOR_EN_CREACION)
        
        return ft.Container(
            bgcolor="white",
            border_radius=10,
            padding=ft.padding.all(10),
            margin=ft.margin.only(bottom=8),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=COLOR_SOMBRA_TARJETAS,
                offset=ft.Offset(0, 2),
            ),
            content=ft.Row(
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # Contenido principal clickeable (Detalle)
                    ft.Container(
                        expand=True,
                        on_click=lambda e, p=proyecto: mostrar_detalle_proyecto(p),
                        ink=True,
                        content=ft.Column(
                            spacing=3,
                            controls=[
                                # Fila 1: Nombre + Estado
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(
                                            proyecto.get("nombre", "Sin nombre"),
                                            size=12,
                                            color="black",
                                            weight=ft.FontWeight.BOLD,
                                            max_lines=1,
                                            overflow="ellipsis"
                                        ),
                                        ft.Container(
                                            width=10,
                                            height=10,
                                            border_radius=5,
                                            bgcolor=estado_color,
                                        ),
                                    ]
                                ),
                                # Fila 2: Código + Cliente
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(proyecto.get("codigo", "N/A"), size=10, color=COLOR_LABEL),
                                        ft.Text(f"Cliente: {proyecto.get('cliente', 'N/A')[:12]}...", size=10, color="#666666"),
                                    ]
                                ),
                            ]
                        ),
                    ),
                    # Botones de Acción (Editar y Borrar)
                    ft.Container(
                        content=ft.Icon(ft.Icons.EDIT, size=18, color=COLOR_EDITAR),
                        on_click=lambda e, p=proyecto: mostrar_editar_proyecto(p),
                        ink=True, padding=5, border_radius=5,
                    ),
                    ft.Container(
                        content=ft.Icon(ft.Icons.DELETE, size=18, color=COLOR_ELIMINAR),
                        on_click=lambda e, p=proyecto: mostrar_confirmar_eliminar(p),
                        ink=True, padding=5, border_radius=5,
                    ),
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
        hint_text="Buscar por nombre o cliente...",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=38,
        expand=True,
        content_padding=ft.padding.only(left=10, right=10, top=8, bottom=8),
        on_submit=lambda e: actualizar_lista_ui()
    )

    btn_filtrar = ft.Container(
        content=ft.Text("Filtrar", size=11, color="black"),
        bgcolor="white",
        border=ft.border.all(1, COLOR_BORDE),
        border_radius=5,
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        on_click=mostrar_dialog_filtros,
        ink=True,
    )

    btn_buscar = ft.Container(
        content=ft.Icon(ft.Icons.SEARCH, size=20, color="white"),
        bgcolor=COLOR_LABEL,
        border_radius=5,
        padding=8,
        on_click=btn_buscar_click,
        ink=True,
    )

    texto_contador = ft.Text("0 proyectos", size=11, color=COLOR_LABEL)

    lista_proyectos = ft.ListView(
        spacing=0,
        expand=True,
    )

    btn_crear = ft.Container(
        width=170,
        height=44,
        bgcolor=COLOR_BTN_CREAR,
        border_radius=22,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_crear_proyecto_click,
        content=ft.Text("Crear Proyecto", color="white", weight=ft.FontWeight.BOLD, size=13),
    )

    # Tarjeta blanca principal contenedora
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
                spacing=10,
                controls=[
                    ft.Row([input_busqueda, btn_filtrar, btn_buscar], spacing=8),
                    texto_contador,
                    ft.Container(
                        height=390,
                        content=lista_proyectos,
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[btn_crear],
                    ),
                ]
            )
        )
    )

    # Header flotante con el título
    header_flotante = ft.Container(
        width=280,
        height=50,
        bgcolor=COLOR_HEADER_BG,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            "GESTIONAR PROYECTOS",
            size=18,
            weight=ft.FontWeight.BOLD,
            color="white"
        )
    )

    # Layout de la vista superpuesta
    contenido_superpuesto = ft.Container(
        width=380,
        height=620,
        content=ft.Stack(
            controls=[
                ft.Container(
                    content=tarjeta_blanca,
                    top=30,
                ),
                ft.Container(
                    content=header_flotante,
                    top=0,
                    left=50,
                )
            ]
        )
    )

    # --- INICIALIZACIÓN ---
    refrescar_datos_completos()

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
    page.title = "App Tareas - Gestionar Proyectos"
    page.window.width = 1200
    page.window.height = 800
    page.padding = 0 
    vista = VistaGestionarProyectos(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)