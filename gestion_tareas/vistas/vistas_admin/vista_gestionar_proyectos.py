import flet as ft
from modelos.crud import obtener_todos_proyectos, eliminar_proyecto, actualizar_proyecto, obtener_todos_empleados, obtener_todos_departamentos, crear_departamento, actualizar_departamento, eliminar_departamento
from datetime import datetime

def VistaGestionarProyectos(page):
    
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
    COLOR_VERDE = "#4CAF50"

    # Variables para almacenar datos reales de la base de datos
    proyectos_db = []
    empleados_maestros = []
    departamentos_maestros = []

    #opciones de filtro
    FILTROS_ESTADO = ["Todos", "ACTIVO", "PAUSADO", "INACTIVO"]
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
        """Consulta la base de datos para traer proyectos, empleados y departamentos"""
        nonlocal proyectos_db, empleados_maestros, departamentos_maestros, FILTROS_CLIENTE
        
        exito_p, list_p = obtener_todos_proyectos()
        if exito_p: 
            proyectos_db = list_p
            set_clientes = set()
            for p in proyectos_db:
                if p.get("cliente"): set_clientes.add(p.get("cliente"))
            FILTROS_CLIENTE = ["Todos"] + sorted(list(set_clientes))
        
        exito_e, list_e = obtener_todos_empleados()
        if exito_e: empleados_maestros = list_e
        
        exito_d, list_d = obtener_todos_departamentos()
        if exito_d: departamentos_maestros = list_d

    def actualizar_lista_ui():
        """Aplica filtros y búsqueda sobre los datos de la memoria y repinta las tarjetas"""
        texto = input_busqueda.value.lower() if input_busqueda.value else ""
        
        filtrados = []
        for p in proyectos_db:
            nombre = p.get("nombre", "").lower()
            cliente = p.get("cliente", "").lower()
            
            if texto and (texto not in nombre and texto not in cliente):
                continue
            
            if filtro_estado_actual[0] != "Todos" and p.get("estado") != filtro_estado_actual[0]:
                continue
            
            if filtro_cliente_actual[0] != "Todos" and p.get("cliente") != filtro_cliente_actual[0]:
                continue
                
            filtrados.append(p)

        if filtro_orden_actual[0] == "Nombre A-Z":
            filtrados.sort(key=lambda x: x.get("nombre", "").lower())
        elif filtro_orden_actual[0] == "Nombre Z-A":
            filtrados.sort(key=lambda x: x.get("nombre", "").lower(), reverse=True)

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

    async def btn_volver_click(e):
        await page.push_route("/area_admin")

    def btn_buscar_click(e):
        actualizar_lista_ui()
        page.snack_bar = ft.SnackBar(ft.Text(f"Buscando: {input_busqueda.value}"))
        page.snack_bar.open = True
        page.update()

    async def btn_crear_proyecto_click(e):
        await page.push_route("/crear_proyecto")

    # --- DIÁLOGOS DE GESTIÓN (CRUD REAL) ---

    def mostrar_detalle_proyecto(proyecto):
        """Muestra el diálogo con el detalle completo del proyecto"""
        estado = proyecto.get("estado", "ACTIVO")
        estado_color = COLOR_ACTIVO if estado == "ACTIVO" else (COLOR_INACTIVO if estado == "INACTIVO" else COLOR_EN_CREACION)
        
        # Obtener departamentos del proyecto
        deptos_proyecto = [d for d in departamentos_maestros if d.get("proyecto_asignado") == proyecto.get("nombre")]
        
        deptos_chips = ft.Row(
            wrap=True, spacing=5, run_spacing=5,
            controls=[
                ft.Container(
                    bgcolor="#E3F2FD",
                    border_radius=12,
                    padding=ft.Padding(left=8, right=8, top=4, bottom=4),
                    content=ft.Text(d.get("nombre", ""), size=10, color="#1565C0", weight="bold"),
                ) for d in deptos_proyecto
            ] if deptos_proyecto else [ft.Text("Sin departamentos asignados", size=11, color="#999999", italic=True)]
        )
        
        dialog_detalle = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text(proyecto.get("nombre", "Proyecto"), size=16, weight=ft.FontWeight.BOLD, color="black"),
            content=ft.Container(
                width=320,
                bgcolor="white",
                content=ft.Column(
                    spacing=12,
                    tight=True,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"Código: {proyecto.get('codigo', 'N/A')}", size=12, color=COLOR_LABEL),
                                ft.Container(
                                    bgcolor=estado_color,
                                    border_radius=10,
                                    padding=ft.Padding(left=10, right=10, top=3, bottom=3),
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
                        ft.Divider(height=1, color=COLOR_BORDE),
                        ft.Column(spacing=4, controls=[
                            ft.Text("Departamentos", size=11, color=COLOR_LABEL, weight="bold"),
                            deptos_chips,
                        ]),
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

    # ============================================
    # DIÁLOGO EDITAR PROYECTO CON DEPARTAMENTOS
    # ============================================
    def mostrar_editar_proyecto(proyecto):
        """Muestra el diálogo para editar proyecto con gestión de departamentos"""
        
        # Obtener departamentos actuales del proyecto
        deptos_proyecto_actuales = [d for d in departamentos_maestros if d.get("proyecto_asignado") == proyecto.get("nombre")]
        # Copia local para edición (incluye departamentos existentes y nuevos)
        deptos_edicion = []
        for d in deptos_proyecto_actuales:
            deptos_edicion.append({
                "_id": d.get("_id"),
                "nombre": d.get("nombre"),
                "miembros": d.get("miembros", []),
                "es_nuevo": False,
                "eliminado": False,
            })
        
        # Campos de texto con los valores actuales - TEXTO EN NEGRO
        input_nom = ft.TextField(
            label="Nombre del Proyecto",
            value=proyecto.get("nombre"),
            border_color=COLOR_BORDE,
            text_style=ft.TextStyle(size=12, color="black"),
            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
        )
        input_cli = ft.TextField(
            label="Cliente / Empresa",
            value=proyecto.get("cliente"),
            border_color=COLOR_BORDE,
            text_style=ft.TextStyle(size=12, color="black"),
            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
        )
        input_cod = ft.TextField(
            label="Código",
            value=proyecto.get("codigo"),
            border_color=COLOR_BORDE,
            text_style=ft.TextStyle(size=12, color="black"),
            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
        )
        input_pres = ft.TextField(
            label="Presupuesto (€)",
            value=str(proyecto.get("presupuesto", 0)).replace(" €", "").replace("€", ""),
            border_color=COLOR_BORDE,
            text_style=ft.TextStyle(size=12, color="black"),
            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
        )
        
        # Selectores con texto negro
        dropdown_est = ft.DropdownM2(
            label="Estado",
            value=proyecto.get("estado"),
            border_color=COLOR_BORDE,
            text_style=ft.TextStyle(size=12, color="black"),
            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
            options=[ft.dropdownm2.Option(opt) for opt in ["ACTIVO", "PAUSADO", "INACTIVO"]]
        )

        dropdown_resp = ft.DropdownM2(
            label="Responsable",
            value=proyecto.get("responsable"),
            border_color=COLOR_BORDE,
            text_style=ft.TextStyle(size=12, color="black"),
            label_style=ft.TextStyle(size=11, color=COLOR_LABEL),
            options=[ft.dropdownm2.Option(f"{emp['nombre']} {emp['apellidos']}") for emp in empleados_maestros]
        )
        
        # Lista visual de departamentos
        lista_deptos_edit = ft.Column(spacing=6)
        
        def actualizar_lista_deptos_edit():
            lista_deptos_edit.controls.clear()
            deptos_visibles = [d for d in deptos_edicion if not d.get("eliminado")]
            
            if not deptos_visibles:
                lista_deptos_edit.controls.append(
                    ft.Text("Sin departamentos", size=11, color="#999999", italic=True)
                )
            else:
                for i, depto in enumerate(deptos_edicion):
                    if depto.get("eliminado"):
                        continue
                    
                    n_miembros = len(depto.get("miembros", []))
                    es_nuevo = depto.get("es_nuevo", False)
                    
                    lista_deptos_edit.controls.append(
                        ft.Container(
                            bgcolor="#F5F8FA" if not es_nuevo else "#E8F5E9",
                            border_radius=6,
                            padding=8,
                            content=ft.Row([
                                ft.Column([
                                    ft.Row([
                                        ft.Text(depto["nombre"], size=11, color="black", weight="bold"),
                                        ft.Text("(nuevo)" if es_nuevo else "", size=9, color=COLOR_VERDE, italic=True),
                                    ], spacing=5),
                                    ft.Text(f"{n_miembros} miembro{'s' if n_miembros != 1 else ''}", size=9, color="#666666"),
                                ], spacing=1, expand=True),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_size=16,
                                    icon_color=COLOR_LABEL,
                                    tooltip="Editar",
                                    on_click=lambda e, idx=i: abrir_editar_depto_en_proyecto(idx),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_size=16,
                                    icon_color=COLOR_ELIMINAR,
                                    tooltip="Eliminar",
                                    on_click=lambda e, idx=i: marcar_depto_eliminado(idx),
                                ),
                            ]),
                        )
                    )
            page.update()
        
        def marcar_depto_eliminado(idx):
            if 0 <= idx < len(deptos_edicion):
                depto = deptos_edicion[idx]
                
                def confirmar_eliminar(e):
                    deptos_edicion[idx]["eliminado"] = True
                    dlg_confirm.open = False
                    actualizar_lista_deptos_edit()
                
                def cancelar(e):
                    dlg_confirm.open = False
                    page.update()
                
                dlg_confirm = ft.AlertDialog(
                    modal=True,
                    title=ft.Row([
                        ft.Icon(ft.Icons.WARNING_AMBER, color=COLOR_ELIMINAR, size=22),
                        ft.Text("Eliminar Departamento", size=14, weight="bold", color="black"),
                    ], spacing=8),
                    bgcolor="white",
                    content=ft.Container(
                        width=280,
                        content=ft.Column([
                            ft.Text("¿Estás seguro de que deseas eliminar este departamento?", size=12, color="black"),
                            ft.Container(
                                bgcolor="#FFF3F3",
                                border_radius=8,
                                padding=10,
                                content=ft.Column([
                                    ft.Text(depto["nombre"], size=12, color="black", weight="bold"),
                                    ft.Text(f"{len(depto.get('miembros', []))} miembros asignados", size=10, color="#666666"),
                                ], spacing=2),
                            ),
                            ft.Text("El departamento se eliminará al guardar los cambios.", size=10, color=COLOR_ELIMINAR, italic=True),
                        ], spacing=10, tight=True),
                    ),
                    actions=[
                        ft.TextButton("Cancelar", on_click=cancelar),
                        ft.FilledButton("Eliminar", on_click=confirmar_eliminar, bgcolor=COLOR_ELIMINAR, color="white"),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                
                page.overlay.append(dlg_confirm)
                dlg_confirm.open = True
                page.update()
        
        def abrir_nuevo_depto_en_proyecto(e):
            """Añadir nuevo departamento al proyecto"""
            input_nombre_nuevo = ft.TextField(
                hint_text="Nombre del departamento",
                border_color=COLOR_BORDE,
                text_style=ft.TextStyle(size=12, color="black"),
                height=42,
            )
            
            miembros_sel = []
            
            def crear_chks():
                chks = []
                for emp in empleados_maestros:
                    nombre = emp.get('nombre', '')
                    apellidos = emp.get('apellidos', '')
                    identificador = emp.get('identificador', '')
                    label = f"{nombre} {apellidos} ({identificador})"
                    
                    def on_chk(ev, empleado=emp):
                        if ev.control.value:
                            if empleado not in miembros_sel:
                                miembros_sel.append(empleado)
                        else:
                            if empleado in miembros_sel:
                                miembros_sel.remove(empleado)
                    
                    chks.append(ft.Checkbox(label=label, value=False, on_change=on_chk, label_style=ft.TextStyle(size=10, color="black")))
                return chks
            
            lista_emps = ft.Column(controls=crear_chks(), spacing=2, scroll=ft.ScrollMode.AUTO, height=180)
            
            def guardar_nuevo(e):
                if not input_nombre_nuevo.value or not input_nombre_nuevo.value.strip():
                    page.snack_bar = ft.SnackBar(ft.Text("❌ Nombre obligatorio"), bgcolor="red")
                    page.snack_bar.open = True
                    page.update()
                    return
                
                # Formatear miembros
                miembros_fmt = []
                for m in miembros_sel:
                    miembros_fmt.append({
                        "id_usuario": str(m.get("_id")),
                        "nombre": m.get("nombre", ""),
                        "apellidos": m.get("apellidos", ""),
                        "identificador": m.get("identificador", ""),
                    })
                
                deptos_edicion.append({
                    "_id": None,
                    "nombre": input_nombre_nuevo.value.strip(),
                    "miembros": miembros_fmt,
                    "es_nuevo": True,
                    "eliminado": False,
                })
                
                dlg_nuevo.open = False
                actualizar_lista_deptos_edit()
            
            def cancelar(e):
                dlg_nuevo.open = False
                page.update()
            
            dlg_nuevo = ft.AlertDialog(
                modal=True,
                title=ft.Text("Nuevo Departamento", size=14, weight="bold", color="black"),
                bgcolor="white",
                content=ft.Container(
                    width=300,
                    content=ft.Column([
                        ft.Text("Nombre", size=10, color=COLOR_LABEL, weight="bold"),
                        input_nombre_nuevo,
                        ft.Container(height=5),
                        ft.Text("Asignar miembros", size=10, color=COLOR_LABEL, weight="bold"),
                        ft.Container(border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)), border_radius=5, padding=8, height=200, content=lista_emps),
                    ], spacing=5, tight=True),
                ),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancelar),
                    ft.FilledButton("Añadir", on_click=guardar_nuevo, bgcolor=COLOR_VERDE, color="white"),
                ],
            )
            
            page.overlay.append(dlg_nuevo)
            dlg_nuevo.open = True
            page.update()
        
        def abrir_editar_depto_en_proyecto(idx):
            """Editar departamento existente o nuevo"""
            depto = deptos_edicion[idx]
            
            input_nombre_edit = ft.TextField(
                value=depto["nombre"],
                border_color=COLOR_BORDE,
                text_style=ft.TextStyle(size=12, color="black"),
                height=42,
            )
            
            miembros_actuales = list(depto.get("miembros", []))
            
            def crear_chks_edit():
                chks = []
                for emp in empleados_maestros:
                    nombre = emp.get('nombre', '')
                    apellidos = emp.get('apellidos', '')
                    identificador = emp.get('identificador', '')
                    label = f"{nombre} {apellidos} ({identificador})"
                    
                    # Verificar si está seleccionado (comparar por id_usuario o _id)
                    esta_sel = any(
                        str(m.get("id_usuario", m.get("_id"))) == str(emp.get("_id")) 
                        for m in miembros_actuales
                    )
                    
                    def on_chk(ev, empleado=emp):
                        emp_id = str(empleado.get("_id"))
                        if ev.control.value:
                            if not any(str(m.get("id_usuario", m.get("_id"))) == emp_id for m in miembros_actuales):
                                miembros_actuales.append({
                                    "id_usuario": emp_id,
                                    "nombre": empleado.get("nombre", ""),
                                    "apellidos": empleado.get("apellidos", ""),
                                    "identificador": empleado.get("identificador", ""),
                                })
                        else:
                            miembros_actuales[:] = [m for m in miembros_actuales if str(m.get("id_usuario", m.get("_id"))) != emp_id]
                    
                    chks.append(ft.Checkbox(label=label, value=esta_sel, on_change=on_chk, label_style=ft.TextStyle(size=10, color="black")))
                return chks
            
            lista_emps_edit = ft.Column(controls=crear_chks_edit(), spacing=2, scroll=ft.ScrollMode.AUTO, height=180)
            
            def guardar_edit(e):
                if not input_nombre_edit.value or not input_nombre_edit.value.strip():
                    page.snack_bar = ft.SnackBar(ft.Text("❌ Nombre obligatorio"), bgcolor="red")
                    page.snack_bar.open = True
                    page.update()
                    return
                
                deptos_edicion[idx]["nombre"] = input_nombre_edit.value.strip()
                deptos_edicion[idx]["miembros"] = list(miembros_actuales)
                
                dlg_edit.open = False
                actualizar_lista_deptos_edit()
            
            def cancelar(e):
                dlg_edit.open = False
                page.update()
            
            dlg_edit = ft.AlertDialog(
                modal=True,
                title=ft.Text(f"Editar: {depto['nombre']}", size=14, weight="bold", color="black"),
                bgcolor="white",
                content=ft.Container(
                    width=300,
                    content=ft.Column([
                        ft.Text("Nombre", size=10, color=COLOR_LABEL, weight="bold"),
                        input_nombre_edit,
                        ft.Container(height=5),
                        ft.Text("Miembros", size=10, color=COLOR_LABEL, weight="bold"),
                        ft.Container(border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)), border_radius=5, padding=8, height=200, content=lista_emps_edit),
                    ], spacing=5, tight=True),
                ),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancelar),
                    ft.FilledButton("Guardar", on_click=guardar_edit, bgcolor=COLOR_LABEL, color="white"),
                ],
            )
            
            page.overlay.append(dlg_edit)
            dlg_edit.open = True
            page.update()

        def guardar_cambios_click(e):
            if not input_nom.value or not input_cli.value:
                page.snack_bar = ft.SnackBar(ft.Text("❌ El nombre y el cliente son obligatorios"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return

            nombre_proyecto_nuevo = input_nom.value.strip()
            nombre_proyecto_anterior = proyecto.get("nombre")

            # 1. Actualizar datos del proyecto
            datos_actualizados = {
                "nombre": nombre_proyecto_nuevo,
                "cliente": input_cli.value,
                "codigo": input_cod.value,
                "presupuesto": f"{input_pres.value} €",
                "responsable": dropdown_resp.value,
                "estado": dropdown_est.value
            }

            exito, msj = actualizar_proyecto(proyecto["_id"], datos_actualizados)
            if not exito:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error al actualizar proyecto: {msj}"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return

            # 2. Procesar departamentos
            for depto in deptos_edicion:
                if depto.get("eliminado"):
                    # Eliminar de la BD si existe
                    if depto.get("_id"):
                        eliminar_departamento(str(depto["_id"]))
                elif depto.get("es_nuevo"):
                    # Crear nuevo departamento
                    crear_departamento({
                        "nombre": depto["nombre"],
                        "proyecto_asignado": nombre_proyecto_nuevo,
                        "miembros": depto.get("miembros", []),
                        "fecha_creacion": datetime.now(),
                    })
                else:
                    # Actualizar existente
                    if depto.get("_id"):
                        actualizar_departamento(str(depto["_id"]), {
                            "nombre": depto["nombre"],
                            "proyecto_asignado": nombre_proyecto_nuevo,
                            "miembros": depto.get("miembros", []),
                        })

            page.snack_bar = ft.SnackBar(ft.Text(f"✅ Proyecto actualizado correctamente"), bgcolor="green")
            dialog_editar.open = False
            refrescar_datos_completos()
            page.snack_bar.open = True
            page.update()

        # Inicializar lista visual
        actualizar_lista_deptos_edit()

        dialog_editar = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Row([
                ft.Icon(ft.Icons.EDIT, color=COLOR_EDITAR, size=22),
                ft.Text("Editar Proyecto", size=16, weight=ft.FontWeight.BOLD, color="black"),
            ], spacing=8),
            content=ft.Container(
                width=360,
                height=520,
                content=ft.Column([
                    input_nom,
                    input_cod,
                    input_cli,
                    dropdown_resp,
                    input_pres,
                    dropdown_est,
                    ft.Divider(height=1, color=COLOR_BORDE),
                    # Sección departamentos
                    ft.Row([
                        ft.Text("Departamentos", size=12, color="black", weight="bold"),
                        ft.Container(expand=True),
                        ft.FilledButton(
                            "+ Añadir",
                            on_click=abrir_nuevo_depto_en_proyecto,
                            bgcolor=COLOR_LABEL,
                            color="white",
                            height=28,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5), text_style=ft.TextStyle(size=10)),
                        ),
                    ]),
                    ft.Container(
                        border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)),
                        border_radius=6,
                        padding=8,
                        height=140,
                        content=ft.Column([lista_deptos_edit], scroll=ft.ScrollMode.AUTO),
                    ),
                ], scroll=ft.ScrollMode.AUTO, spacing=12)
            ),
            actions=[
                ft.TextButton(content=ft.Text("Cancelar", color="black"), on_click=lambda e: setattr(dialog_editar, 'open', False) or page.update()),
                ft.FilledButton(content=ft.Text("Guardar Cambios", color="white", weight="bold"), bgcolor=COLOR_BTN_CREAR, on_click=guardar_cambios_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_editar)
        dialog_editar.open = True
        page.update()

    #dialog confirmar eliminación
    def mostrar_confirmar_eliminar(proyecto):
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
                ft.FilledButton(content=ft.Text("Eliminar", color="white", weight="bold"), bgcolor=COLOR_ELIMINAR, on_click=confirmar_eliminar),
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

        dialog_filtros = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text("Filtros y Orden", size=16, weight="bold", color="black"),
            content=ft.Container(
                width=280,
                height=350,
                content=ft.Column([
                    ft.Text("Estado:", size=12, weight="bold", color=COLOR_LABEL),
                    radio_estado,
                    ft.Divider(),
                    ft.Text("Orden:", size=12, weight="bold", color=COLOR_LABEL),
                    radio_orden,
                ], scroll=ft.ScrollMode.AUTO, spacing=8),
            ),
            actions=[
                ft.TextButton("Aplicar", on_click=aplicar_filtros_click),
            ],
        )

        page.overlay.append(dialog_filtros)
        dialog_filtros.open = True
        page.update()

    def crear_tarjeta_proyecto(proyecto):
        estado = proyecto.get("estado", "ACTIVO")
        estado_color = COLOR_ACTIVO if estado == "ACTIVO" else (COLOR_INACTIVO if estado == "INACTIVO" else COLOR_EN_CREACION)

        return ft.Container(
            bgcolor="white",
            border_radius=10,
            padding=12,
            margin=ft.Margin(bottom=8, left=0, right=0, top=0),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=4, color=COLOR_SOMBRA_TARJETAS, offset=ft.Offset(0, 2)),
            on_click=lambda e, p=proyecto: mostrar_detalle_proyecto(p),
            ink=True,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            spacing=4,
                            controls=[
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
        content_padding=ft.Padding(left=10, right=10, top=8, bottom=8),
        on_submit=lambda e: actualizar_lista_ui()
    )

    btn_filtrar = ft.Container(
        content=ft.Text("Filtrar", size=11, color="black"),
        bgcolor="white",
        border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)),
        border_radius=5,
        padding=ft.Padding(left=12, right=12, top=8, bottom=8),
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

    tarjeta_blanca = ft.Container(
        width=380,
        bgcolor="white",
        border_radius=25,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color=COLOR_SOMBRA,
            offset=ft.Offset(0, 5),
        ),
        content=ft.Container(
            padding=ft.Padding(left=18, right=18, top=55, bottom=20),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row([input_busqueda, btn_filtrar, btn_buscar], spacing=8),
                    texto_contador,
                    ft.Container(
                        height=360,
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