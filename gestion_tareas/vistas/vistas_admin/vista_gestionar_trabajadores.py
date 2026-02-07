import flet as ft
from modelos.crud import obtener_todos_empleados, eliminar_empleado, actualizar_empleado, obtener_todos_proyectos, obtener_todos_departamentos

def VistaGestionarTrabajadores(page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_SOMBRA_TARJETAS = "#30000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_ACTIVO = "#4CAF50"
    COLOR_INACTIVO = "#F44336"
    COLOR_PENDIENTE = "#FF9800"
    COLOR_EDITAR = "#2196F3"
    COLOR_ELIMINAR = "#E53935"
    COLOR_BTN_CREAR = "#4682B4"

    #opciones de filtro
    FILTROS_ESTADO = ["Todos", "ACTIVO", "INACTIVO", "PENDIENTE"]
    # El filtro de proyectos lo inicializamos con "Todos", pero se llenará con la BD
    FILTROS_PROYECTO = ["Todos"]
    FILTROS_ORDEN = [
        "Nombre A-Z",
        "Nombre Z-A",
        "Más reciente",
        "Más antiguo",
        "Por proyecto",
    ]

    filtro_estado_actual = ["Todos"]
    filtro_proyecto_actual = ["Todos"]
    filtro_orden_actual = ["Nombre A-Z"]

    # Variables globales de la vista para almacenar datos de la BD
    trabajadores_db = []
    proyectos_maestros = []
    departamentos_maestros = []

    # --- LÓGICA DE BASE DE DATOS ---

    def cargar_datos_maestros():
        """Consulta la base de datos para traer trabajadores, proyectos y departamentos"""
        nonlocal trabajadores_db, proyectos_maestros, departamentos_maestros, FILTROS_PROYECTO
        
        exito_t, list_t = obtener_todos_empleados()
        if exito_t: trabajadores_db = list_t
        
        exito_p, list_p = obtener_todos_proyectos()
        if exito_p: 
            proyectos_maestros = list_p
            FILTROS_PROYECTO = ["Todos"] + [p["nombre"] for p in proyectos_maestros]
        
        exito_d, list_d = obtener_todos_departamentos()
        if exito_d: departamentos_maestros = list_d

    def actualizar_lista_ui():
        """Aplica los filtros de búsqueda, estado y proyecto sobre los datos de la memoria"""
        texto = input_busqueda.value.lower() if input_busqueda.value else ""
        
        filtrados = []
        for t in trabajadores_db:
            nombre_completo = f"{t.get('nombre', '')} {t.get('apellidos', '')}".lower()
            id_emp = t.get("id_empleado", "").lower()
            
            # 1. Filtro de búsqueda
            if texto and (texto not in nombre_completo and texto not in id_emp):
                continue
            
            # 2. Filtro de estado
            if filtro_estado_actual[0] != "Todos" and t.get("estado") != filtro_estado_actual[0]:
                continue
            
            # 3. Filtro de proyecto
            if filtro_proyecto_actual[0] != "Todos":
                proys_trabajador = t.get("proyecto") or []
                if isinstance(proys_trabajador, str): proys_trabajador = [proys_trabajador]
                if filtro_proyecto_actual[0] not in proys_trabajador:
                    continue
                    
            filtrados.append(t)

        # 4. Ordenación
        if filtro_orden_actual[0] == "Nombre A-Z":
            filtrados.sort(key=lambda x: x.get("nombre", "").lower())
        elif filtro_orden_actual[0] == "Nombre Z-A":
            filtrados.sort(key=lambda x: x.get("nombre", "").lower(), reverse=True)

        # Limpiamos y repintamos la lista
        lista_trabajadores.controls = []
        if not filtrados:
            lista_trabajadores.controls.append(
                ft.Container(padding=20, content=ft.Text("No se encontraron trabajadores", color="grey", text_align="center"))
            )
        else:
            for trabajador in filtrados:
                lista_trabajadores.controls.append(crear_tarjeta_trabajador(trabajador))
        
        contador_trabajadores.value = f"{len(filtrados)} trabajadores"
        page.update()

    def refrescar_todo():
        """Recarga de BD y refresca UI"""
        cargar_datos_maestros()
        actualizar_lista_ui()

    def btn_volver_click(e):
        """Vuelve al Dashboard de Admin"""
        page.go("/area_admin")

    def btn_buscar_click(e):
        """Acción al hacer clic en el botón buscar"""
        actualizar_lista_ui()
        page.snack_bar = ft.SnackBar(ft.Text(f"Buscando: {input_busqueda.value}"))
        page.snack_bar.open = True
        page.update()

    def btn_crear_trabajador_click(e):
        """Navega a la vista de creación"""
        page.go("/crear_trabajador")

    def btn_gestionar_roles_click(e):
        """Navega a la vista de roles"""
        page.go("/gestionar_roles")

    # --- DIÁLOGOS DE GESTIÓN (DETALLE / EDITAR / ELIMINAR) ---

    def mostrar_detalle_trabajador(trabajador):
        """Muestra el diálogo con el detalle del trabajador"""
        estado = trabajador.get("estado", "ACTIVO")
        estado_color = COLOR_ACTIVO if estado == "ACTIVO" else (COLOR_INACTIVO if estado == "INACTIVO" else COLOR_PENDIENTE)
        
        proys = trabajador.get("proyecto") or []
        if isinstance(proys, str): proys = [proys]
        
        depts = trabajador.get("departamento") or []
        nombres_depts = []
        if isinstance(depts, list):
            for d in depts:
                if isinstance(d, dict): nombres_depts.append(d.get("nombre", "N/A"))
                else: nombres_depts.append(str(d))
        elif isinstance(depts, dict):
            nombres_depts = [depts.get("nombre", "N/A")]

        dialog_detalle = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text(f"{trabajador.get('nombre')} {trabajador.get('apellidos')}", size=16, weight=ft.FontWeight.BOLD, color="black"),
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
                                ft.Text(f"ID: {trabajador.get('id_empleado', 'N/A')}", size=12, color=COLOR_LABEL),
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
                            ft.Text("Email", size=11, color=COLOR_LABEL),
                            ft.Text(trabajador.get("email", "N/A"), size=12, color="black"),
                        ]),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Proyectos", size=11, color=COLOR_LABEL),
                            ft.Text(", ".join(proys) if proys else "Ninguno", size=12, color="black"),
                        ]),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Departamentos", size=11, color=COLOR_LABEL),
                            ft.Text(", ".join(nombres_depts) if nombres_depts else "Ninguno", size=12, color="black"),
                        ]),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Cargo", size=11, color=COLOR_LABEL),
                            ft.Text(trabajador.get("cargo", "N/A"), size=12, color="black"),
                        ]),
                        ft.Column(spacing=2, controls=[
                            ft.Text("Fecha de alta", size=11, color=COLOR_LABEL),
                            ft.Text(str(trabajador.get("fecha_incorporacion", "N/A"))[:10], size=12, color="black"),
                        ]),
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

    def mostrar_editar_trabajador(t):
        """Muestra el diálogo para editar TODOS los campos con seguridad NoneType"""
        
        proyectos_sel = t.get("proyecto") or []
        if isinstance(proyectos_sel, str): proyectos_sel = [proyectos_sel]
        
        deptos_raw = t.get("departamento") or []
        deptos_sel = []
        if isinstance(deptos_raw, list):
            for d in deptos_raw:
                if isinstance(d, dict): deptos_sel.append(d.get("nombre"))
                else: deptos_sel.append(str(d))
        elif isinstance(deptos_raw, dict):
            deptos_sel = [deptos_raw.get("nombre")]

        input_nom = ft.TextField(label="Nombre", value=t.get("nombre"), border_color=COLOR_BORDE, text_size=12)
        input_ape = ft.TextField(label="Apellidos", value=t.get("apellidos"), border_color=COLOR_BORDE, text_size=12)
        input_cargo = ft.TextField(label="Cargo", value=t.get("cargo"), border_color=COLOR_BORDE, text_size=12)
        input_email = ft.TextField(label="Email", value=t.get("email"), border_color=COLOR_BORDE, text_size=12)
        input_tel = ft.TextField(label="Teléfono", value=t.get("telefono"), border_color=COLOR_BORDE, text_size=12)
        input_dni = ft.TextField(label="Identificador (DNI)", value=t.get("identificador"), border_color=COLOR_BORDE, text_size=12)
        input_ubi = ft.TextField(label="Ubicación", value=t.get("ubicacion"), border_color=COLOR_BORDE, text_size=12)

        lista_empresas = sorted(list(set([d.get("empresa") for d in departamentos_maestros if d.get("empresa")])))
        if not lista_empresas: lista_empresas = [t.get("empresa", "Empresa General")]

        dropdown_emp = ft.DropdownM2(
            label="Empresa", value=t.get("empresa"), border_color=COLOR_BORDE,
            options=[ft.dropdownm2.Option(opt) for opt in lista_empresas]
        )
        dropdown_est = ft.DropdownM2(
            label="Estado", value=t.get("estado"), border_color=COLOR_BORDE,
            options=[ft.dropdownm2.Option(opt) for opt in ["ACTIVO", "INACTIVO", "PENDIENTE"]]
        )

        txt_proy_resumen = ft.Text(f"{len(proyectos_sel)} proyectos", size=11, color=COLOR_LABEL)
        txt_dept_resumen = ft.Text(f"{len(deptos_sel)} departamentos", size=11, color=COLOR_LABEL)

        def abrir_selector_proyectos(e):
            if not dropdown_emp.value: return
            opciones = [p["nombre"] for p in proyectos_maestros if p.get("cliente") == dropdown_emp.value]
            checks = [ft.Checkbox(label=opt, value=opt in proyectos_sel, data=opt) for opt in opciones]
            
            def confirmar_p(e):
                nonlocal proyectos_sel
                proyectos_sel = [c.data for c in checks if c.value]
                txt_proy_resumen.value = f"{len(proyectos_sel)} proyectos"
                sel_dialog.open = False
                page.update()

            sel_dialog = ft.AlertDialog(
                title=ft.Text("Proyectos", color="black"),
                content=ft.Container(height=300, content=ft.ListView(controls=checks)),
                actions=[ft.TextButton("Aceptar", on_click=confirmar_p)],
                bgcolor="white"
            )
            page.overlay.append(sel_dialog)
            sel_dialog.open = True
            page.update()

        def abrir_selector_deptos(e):
            if not dropdown_emp.value: return
            opciones = [d["nombre"] for d in departamentos_maestros if d.get("empresa") == dropdown_emp.value]
            checks = [ft.Checkbox(label=opt, value=opt in deptos_sel, data=opt) for opt in opciones]
            
            def confirmar_d(e):
                nonlocal deptos_sel
                deptos_sel = [c.data for c in checks if c.value]
                txt_dept_resumen.value = f"{len(deptos_sel)} departamentos"
                sel_dialog.open = False
                page.update()

            sel_dialog = ft.AlertDialog(
                title=ft.Text("Departamentos", color="black"),
                content=ft.Container(height=300, content=ft.ListView(controls=checks)),
                actions=[ft.TextButton("Aceptar", on_click=confirmar_d)],
                bgcolor="white"
            )
            page.overlay.append(sel_dialog)
            sel_dialog.open = True
            page.update()

        def guardar_cambios(e):
            datos_nuevos = {
                "nombre": input_nom.value,
                "apellidos": input_ape.value,
                "email": input_email.value,
                "cargo": input_cargo.value,
                "telefono": input_tel.value,
                "identificador": input_dni.value,
                "ubicacion": input_ubi.value,
                "empresa": dropdown_emp.value,
                "estado": dropdown_est.value,
                "proyecto": proyectos_sel,
                "departamento": deptos_sel
            }
            exito, msj = actualizar_empleado(t["_id"], datos_nuevos)
            if exito:
                page.snack_bar = ft.SnackBar(ft.Text("✅ Actualizado"), bgcolor="green")
                dialog_editar.open = False
                refrescar_todo()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {msj}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

        dialog_editar = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text(f"Editar Trabajador", size=16, weight="bold", color="black"),
            content=ft.Container(
                width=350, height=500,
                content=ft.Column([
                    input_nom, input_ape, input_email, input_cargo, dropdown_emp,
                    ft.Divider(),
                    ft.Text("Asignaciones múltiples:", size=11, weight="bold", color=COLOR_LABEL),
                    ft.Row([txt_proy_resumen, ft.IconButton(ft.Icons.ADD_LINK, on_click=abrir_selector_proyectos)], alignment="spaceBetween"),
                    ft.Row([txt_dept_resumen, ft.IconButton(ft.Icons.ADD_LINK, on_click=abrir_selector_deptos)], alignment="spaceBetween"),
                    ft.Divider(),
                    input_dni, input_tel, input_ubi, dropdown_est
                ], scroll="auto", spacing=12)
            ),
            actions=[
                ft.TextButton(content=ft.Text("Cancelar", color="black"), on_click=lambda e: cerrar_dialog(dialog_editar)),
                ft.ElevatedButton(content=ft.Text("Guardar", color="white"), bgcolor=COLOR_BTN_CREAR, on_click=guardar_cambios),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_editar)
        dialog_editar.open = True
        page.update()

    def mostrar_confirmar_eliminar(trabajador):
        def confirmar_eliminar(e):
            exito, msj = eliminar_empleado(trabajador["_id"])
            if exito:
                page.snack_bar = ft.SnackBar(ft.Text(f"✅ Trabajador eliminado"), bgcolor="green")
                dialog_confirmar.open = False
                refrescar_todo()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {msj}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

        dialog_confirmar = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text("Eliminar trabajador", size=16, weight=ft.FontWeight.BOLD, color="black"),
            content=ft.Container(
                width=280,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    tight=True,
                    controls=[
                        ft.Text("¿Estás seguro de eliminar a este trabajador?", size=12, color="black"),
                        ft.Container(
                            bgcolor="#FFF3F3",
                            border_radius=8,
                            padding=10,
                            content=ft.Column(
                                spacing=3,
                                controls=[
                                    ft.Text(f"{trabajador.get('nombre')} {trabajador.get('apellidos')}", size=13, color="black", weight="bold"),
                                    ft.Text(f"ID: {trabajador.get('id_empleado')}", size=11, color="#666666"),
                                ],
                            ),
                        ),
                    ]
                ),
            ),
            actions=[
                ft.TextButton(content=ft.Text("Cancelar", color="black"), on_click=lambda e: cerrar_dialog(dialog_confirmar)),
                ft.ElevatedButton(content=ft.Text("Eliminar", color="white"), bgcolor=COLOR_ELIMINAR, on_click=confirmar_eliminar),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_confirmar)
        dialog_confirmar.open = True
        page.update()

    def cerrar_dialog(dialog):
        dialog.open = False
        page.update()

    # --- RENDERIZADO DE TARJETAS ---

    def crear_tarjeta_trabajador(t):
        estado = t.get("estado", "ACTIVO")
        estado_color = COLOR_ACTIVO if estado == "ACTIVO" else (COLOR_INACTIVO if estado == "INACTIVO" else COLOR_PENDIENTE)
        
        proys = t.get("proyecto") or []
        if isinstance(proys, str): proys = [proys]
        num_proy = len(proys)
        
        depts = t.get("departamento") or []
        if isinstance(depts, dict): num_dept = 1
        else: num_dept = len(depts)

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
                    ft.Container(
                        expand=True,
                        on_click=lambda e, worker=t: mostrar_detalle_trabajador(worker),
                        ink=True,
                        content=ft.Column(
                            spacing=3,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(f"{t.get('nombre')} {t.get('apellidos')}", size=12, color="black", weight=ft.FontWeight.BOLD, max_lines=1, overflow="ellipsis"),
                                        ft.Container(width=10, height=10, border_radius=5, bgcolor=estado_color),
                                    ]
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(f"ID: {t.get('id_empleado', 'N/A')}", size=10, color=COLOR_LABEL),
                                        ft.Text(f"{num_proy} Proy | {num_dept} Dept", size=10, color="#666666"),
                                    ]
                                ),
                            ]
                        ),
                    ),
                    ft.Container(content=ft.Icon(ft.Icons.EDIT, size=18, color=COLOR_EDITAR), on_click=lambda e, worker=t: mostrar_editar_trabajador(worker), ink=True, padding=5, border_radius=5),
                    ft.Container(content=ft.Icon(ft.Icons.DELETE, size=18, color=COLOR_ELIMINAR), on_click=lambda e, worker=t: mostrar_confirmar_eliminar(worker), ink=True, padding=5, border_radius=5),
                ]
            ),
        )

    # --- ELEMENTOS DE LA PÁGINA ---

    btn_volver = ft.Container(content=ft.Text("←", size=24, color="white", weight=ft.FontWeight.BOLD), on_click=btn_volver_click, ink=True, padding=10)

    input_busqueda = ft.TextField(
        hint_text="Buscar por nombre o ID...",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=38,
        expand=True,
        content_padding=ft.padding.only(left=10, right=10, top=8, bottom=8),
        on_submit=lambda e: actualizar_lista_ui()
    )

    btn_buscar = ft.Container(
        content=ft.Icon(ft.Icons.SEARCH, size=20, color="white"),
        bgcolor=COLOR_LABEL, border_radius=5, padding=8,
        on_click=btn_buscar_click, ink=True,
    )

    contador_trabajadores = ft.Text("0 trabajadores", size=11, color=COLOR_LABEL)
    lista_trabajadores = ft.ListView(spacing=0, expand=True)

    btn_crear = ft.Container(
        width=160, height=40, bgcolor=COLOR_BTN_CREAR, border_radius=20, alignment=ft.Alignment(0, 0), ink=True,
        on_click=btn_crear_trabajador_click,
        content=ft.Text("Crear Trabajador", color="white", weight=ft.FontWeight.BOLD, size=12),
    )

    btn_roles = ft.Container(
        width=140, height=40, bgcolor="#6A5ACD", border_radius=20, alignment=ft.Alignment(0, 0), ink=True,
        on_click=btn_gestionar_roles_click,
        content=ft.Text("Gestionar Roles", color="white", weight=ft.FontWeight.BOLD, size=12),
    )

    tarjeta_blanca = ft.Container(
        width=380, bgcolor="white", border_radius=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color=COLOR_SOMBRA, offset=ft.Offset(0, 5)),
        content=ft.Container(
            padding=ft.padding.only(left=18, right=18, top=55, bottom=20),
            content=ft.Column([
                ft.Row([input_busqueda, btn_buscar], spacing=8),
                contador_trabajadores,
                ft.Container(height=380, content=lista_trabajadores),
                ft.Row([btn_crear, btn_roles], alignment="center", spacing=10),
            ], spacing=10)
        )
    )

    header_flotante = ft.Container(
        width=300, height=50, bgcolor=COLOR_HEADER_BG, border_radius=25, alignment=ft.Alignment(0, 0),
        content=ft.Text("GESTIONAR TRABAJADORES", size=18, weight=ft.FontWeight.BOLD, color="white")
    )

    contenido_superpuesto = ft.Container(
        width=380, height=620,
        content=ft.Stack([
            ft.Container(content=tarjeta_blanca, top=30),
            ft.Container(content=header_flotante, top=0, left=40)
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