import flet as ft
from datetime import datetime
from modelos.crud import crear_proyecto, crear_departamento, obtener_todos_empleados

def VistaCrearProyecto(page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_BTN_CREAR = "#4682B4"
    COLOR_VERDE = "#4CAF50"
    COLOR_ROJO = "#E53935"

    # Listas para almacenar datos reales de la BD
    empleados_db = []
    # Lista temporal de departamentos a crear con el proyecto
    departamentos_temp = []

    # --- LÓGICA DE DATOS Y FECHAS ---

    def cargar_datos_iniciales():
        """Carga la lista de empleados para el selector de responsables"""
        nonlocal empleados_db
        exito, resultado = obtener_todos_empleados()
        if exito:
            empleados_db = resultado
            dropdown_responsable.options = [
                ft.dropdownm2.Option(f"{emp.get('nombre', '')} {emp.get('apellidos', '')}") 
                for emp in empleados_db
            ]
            page.update()

    # Variables para almacenar las fechas seleccionadas
    fecha_inicio_val = [None]
    fecha_fin_val = [None]

    def on_fecha_inicio_change(e):
        if e.control.value:
            fecha_inicio_val[0] = e.control.value
            txt_fecha_inicio.value = e.control.value.strftime("%d/%m/%Y")
            txt_fecha_inicio.color = "black"
            page.update()

    def on_fecha_fin_change(e):
        if e.control.value:
            fecha_fin_val[0] = e.control.value
            txt_fecha_fin.value = e.control.value.strftime("%d/%m/%Y")
            txt_fecha_fin.color = "black"
            page.update()

    # Funciones para abrir los selectores de fecha
    def abrir_picker_inicio(e):
        date_picker_inicio.open = True
        page.update()

    def abrir_picker_fin(e):
        date_picker_fin.open = True
        page.update()

    # Componentes de selección de fecha
    date_picker_inicio = ft.DatePicker(
        on_change=on_fecha_inicio_change,
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
    )
    date_picker_fin = ft.DatePicker(
        on_change=on_fecha_fin_change,
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
    )
    page.overlay.append(date_picker_inicio)
    page.overlay.append(date_picker_fin)

    async def btn_volver_click(e):
        await page.push_route("/gestionar_proyectos")

    def mostrar_mensaje_dialog(page, titulo, mensaje, color):
        """Muestra un diálogo de alerta visible compatible con versiones antiguas"""
        dlg = ft.AlertDialog(
            title=ft.Text(titulo, color="black", weight="bold"),
            content=ft.Text(mensaje, color="black", size=14),
            bgcolor="white",
            actions=[
                ft.TextButton("Entendido", on_click=lambda e: setattr(dlg, "open", False) or page.update())
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # ============================================
    # GESTIÓN DE DEPARTAMENTOS TEMPORALES
    # ============================================
    
    lista_deptos_visual = ft.Column(spacing=8)
    
    def actualizar_lista_deptos_visual():
        """Actualiza la visualización de los departamentos añadidos"""
        lista_deptos_visual.controls.clear()
        
        if not departamentos_temp:
            lista_deptos_visual.controls.append(
                ft.Container(
                    padding=15,
                    content=ft.Text("No hay departamentos añadidos", size=11, color="#999999", italic=True, text_align="center"),
                )
            )
        else:
            for i, depto in enumerate(departamentos_temp):
                n_miembros = len(depto.get("miembros", []))
                miembros_txt = f"{n_miembros} miembro{'s' if n_miembros != 1 else ''}"
                
                # Mostrar nombres de algunos miembros
                nombres_preview = ", ".join([m.get("nombre", "") for m in depto.get("miembros", [])[:2]])
                if n_miembros > 2:
                    nombres_preview += f" +{n_miembros - 2}"
                
                lista_deptos_visual.controls.append(
                    ft.Container(
                        bgcolor="#F8F9FA",
                        border_radius=8,
                        border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)),
                        padding=10,
                        content=ft.Row([
                            ft.Column([
                                ft.Text(depto["nombre"], size=12, color="black", weight="bold"),
                                ft.Text(f"{miembros_txt}: {nombres_preview}" if nombres_preview else miembros_txt, 
                                       size=10, color="#666666", max_lines=1, overflow="ellipsis"),
                            ], spacing=2, expand=True),
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_size=18,
                                icon_color=COLOR_LABEL,
                                tooltip="Editar departamento",
                                on_click=lambda e, idx=i: abrir_editar_departamento(idx),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_size=18,
                                icon_color=COLOR_ROJO,
                                tooltip="Eliminar departamento",
                                on_click=lambda e, idx=i: eliminar_departamento_temp(idx),
                            ),
                        ]),
                    )
                )
        page.update()
    
    def eliminar_departamento_temp(idx):
        """Elimina un departamento de la lista temporal"""
        if 0 <= idx < len(departamentos_temp):
            nombre = departamentos_temp[idx]["nombre"]
            departamentos_temp.pop(idx)
            actualizar_lista_deptos_visual()
            actualizar_lista_deptos_visual()
            mostrar_mensaje_dialog(page, "🗑️ Eliminado", f"Departamento '{nombre}' eliminado", COLOR_ROJO)
            page.update()
    
    def abrir_dialog_nuevo_departamento(e):
        """Abre el diálogo para crear un nuevo departamento"""
        input_nombre_depto = ft.TextField(
            hint_text="Nombre del departamento",
            border_color=COLOR_BORDE,
            text_style=ft.TextStyle(size=12, color="black"),
            height=42,
            content_padding=ft.Padding(left=10, right=10, top=8, bottom=8),
        )
        
        miembros_seleccionados = []
        
        def crear_checkboxes_empleados():
            chks = []
            for emp in empleados_db:
                nombre = emp.get('nombre', '')
                apellidos = emp.get('apellidos', '')
                identificador = emp.get('identificador', '')
                label = f"{nombre} {apellidos} ({identificador})"
                
                def on_check(ev, empleado=emp):
                    if ev.control.value:
                        if empleado not in miembros_seleccionados:
                            miembros_seleccionados.append(empleado)
                    else:
                        if empleado in miembros_seleccionados:
                            miembros_seleccionados.remove(empleado)
                
                chks.append(ft.Checkbox(
                    label=label,
                    value=False,
                    on_change=on_check,
                    label_style=ft.TextStyle(size=10, color="black"),
                ))
            return chks
        
        lista_empleados = ft.Column(
            controls=crear_checkboxes_empleados(),
            spacing=2,
            scroll=ft.ScrollMode.AUTO,
        )
        
        def guardar_departamento(e):
            if not input_nombre_depto.value or not input_nombre_depto.value.strip():
                mostrar_mensaje_dialog(page, "⚠️ Campos obligatorios", "❌ El nombre del departamento es obligatorio", "red")
                page.update()
                return
            
            # Verificar que no exista ya un departamento con ese nombre
            for d in departamentos_temp:
                if d["nombre"].lower() == input_nombre_depto.value.strip().lower():
                    mostrar_mensaje_dialog(page, "⚠️ Duplicado", "❌ Ya existe un departamento con ese nombre", "red")
                    page.update()
                    return
            
            departamentos_temp.append({
                "nombre": input_nombre_depto.value.strip(),
                "miembros": list(miembros_seleccionados)
            })
            
            dialog_nuevo_depto.open = False
            actualizar_lista_deptos_visual()
            mostrar_mensaje_dialog(page, "✅ Éxito", f"✅ Departamento '{input_nombre_depto.value}' añadido", COLOR_VERDE)
            page.update()
        
        def cancelar(e):
            dialog_nuevo_depto.open = False
            page.update()
        
        dialog_nuevo_depto = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.ADD_BUSINESS, color=COLOR_LABEL, size=22),
                ft.Text("Nuevo Departamento", size=15, weight="bold", color="black"),
            ], spacing=8),
            bgcolor="white",
            content=ft.Container(
                width=340,
                height=380,
                content=ft.Column([
                    ft.Column([
                        ft.Row([
                            ft.Text("Nombre del departamento", size=11, color=COLOR_LABEL, weight="bold"),
                            ft.Text("*", size=11, color=COLOR_ROJO, weight="bold"),
                        ], spacing=2),
                        input_nombre_depto,
                    ], spacing=3),
                    ft.Container(height=8),
                    ft.Text("Asignar miembros al departamento", size=11, color=COLOR_LABEL, weight="bold"),
                    ft.Container(
                        border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)),
                        border_radius=8,
                        padding=10,
                        height=250,
                        content=lista_empleados if empleados_db else ft.Text("No hay empleados registrados", color="#999999"),
                    ),
                ], spacing=5, tight=True),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.FilledButton("Añadir Departamento", on_click=guardar_departamento, bgcolor=COLOR_VERDE, color="white"),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.overlay.append(dialog_nuevo_depto)
        dialog_nuevo_depto.open = True
        page.update()
    
    def abrir_editar_departamento(idx):
        """Abre el diálogo para editar un departamento existente"""
        depto = departamentos_temp[idx]
        
        input_nombre_depto_edit = ft.TextField(
            value=depto["nombre"],
            border_color=COLOR_BORDE,
            text_style=ft.TextStyle(size=12, color="black"),
            height=42,
            content_padding=ft.Padding(left=10, right=10, top=8, bottom=8),
        )
        
        miembros_actuales = list(depto.get("miembros", []))
        
        def crear_checkboxes_edit():
            chks = []
            for emp in empleados_db:
                nombre = emp.get('nombre', '')
                apellidos = emp.get('apellidos', '')
                identificador = emp.get('identificador', '')
                label = f"{nombre} {apellidos} ({identificador})"
                
                # Verificar si ya está seleccionado
                esta_sel = any(str(m.get("_id")) == str(emp.get("_id")) for m in miembros_actuales)
                
                def on_check(ev, empleado=emp):
                    if ev.control.value:
                        if not any(str(m.get("_id")) == str(empleado.get("_id")) for m in miembros_actuales):
                            miembros_actuales.append(empleado)
                    else:
                        miembros_actuales[:] = [m for m in miembros_actuales if str(m.get("_id")) != str(empleado.get("_id"))]
                
                chks.append(ft.Checkbox(
                    label=label,
                    value=esta_sel,
                    on_change=on_check,
                    label_style=ft.TextStyle(size=10, color="black"),
                ))
            return chks
        
        lista_empleados_edit = ft.Column(
            controls=crear_checkboxes_edit(),
            spacing=2,
            scroll=ft.ScrollMode.AUTO,
        )
        
        def guardar_edicion(e):
            if not input_nombre_depto_edit.value or not input_nombre_depto_edit.value.strip():
                mostrar_mensaje_dialog(page, "⚠️ Campos obligatorios", "❌ El nombre es obligatorio", "red")
                page.update()
                return
            
            # Verificar duplicados (excluyendo el actual)
            nuevo_nombre = input_nombre_depto_edit.value.strip()
            for i, d in enumerate(departamentos_temp):
                if i != idx and d["nombre"].lower() == nuevo_nombre.lower():
                    mostrar_mensaje_dialog(page, "⚠️ Duplicado", "❌ Ya existe otro departamento con ese nombre", "red")
                    page.update()
                    return
            
            departamentos_temp[idx] = {
                "nombre": nuevo_nombre,
                "miembros": list(miembros_actuales)
            }
            
            dialog_edit_depto.open = False
            actualizar_lista_deptos_visual()
            mostrar_mensaje_dialog(page, "✅ Éxito", f"✅ Departamento actualizado", COLOR_VERDE)
            page.update()
        
        def cancelar(e):
            dialog_edit_depto.open = False
            page.update()
        
        dialog_edit_depto = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.EDIT, color=COLOR_LABEL, size=22),
                ft.Text(f"Editar: {depto['nombre']}", size=15, weight="bold", color="black"),
            ], spacing=8),
            bgcolor="white",
            content=ft.Container(
                width=340,
                height=380,
                content=ft.Column([
                    ft.Column([
                        ft.Row([
                            ft.Text("Nombre del departamento", size=11, color=COLOR_LABEL, weight="bold"),
                            ft.Text("*", size=11, color=COLOR_ROJO, weight="bold"),
                        ], spacing=2),
                        input_nombre_depto_edit,
                    ], spacing=3),
                    ft.Container(height=8),
                    ft.Text("Miembros asignados", size=11, color=COLOR_LABEL, weight="bold"),
                    ft.Container(
                        border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)),
                        border_radius=8,
                        padding=10,
                        height=250,
                        content=lista_empleados_edit,
                    ),
                ], spacing=5, tight=True),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.FilledButton("Guardar Cambios", on_click=guardar_edicion, bgcolor=COLOR_LABEL, color="white"),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.overlay.append(dialog_edit_depto)
        dialog_edit_depto.open = True
        page.update()

    # ============================================
    # CREAR PROYECTO CON DEPARTAMENTOS
    # ============================================

    async def btn_crear_click(e):
        """Valida y guarda el nuevo proyecto con sus departamentos en la base de datos"""
        
        # 1. Validaciones
        if not input_nombre.value or not input_cliente.value:
            mostrar_mensaje_dialog(page, "⚠️ Campos obligatorios", "❌ El nombre y el cliente son obligatorios", "red")
            page.update()
            return

        if not fecha_inicio_val[0] or not fecha_fin_val[0]:
            mostrar_mensaje_dialog(page, "⚠️ Campos obligatorios", "❌ Debes seleccionar las fechas del proyecto", "red")
            page.update()
            return

        if fecha_fin_val[0] < fecha_inicio_val[0]:
            mostrar_mensaje_dialog(page, "📅 Error en Fechas", "❌ La fecha de fin no puede ser anterior a la fecha de inicio", "red")
            page.update()
            return

        # 2. Procesar Presupuesto
        presupuesto_val = 0.0
        if input_presupuesto.value:
            try:
                # Limpiar cualquier símbolo o espacio y convertir a float
                limpio = input_presupuesto.value.replace("€", "").replace(",", ".").strip()
                if limpio:
                    presupuesto_val = float(limpio)
            except ValueError:
                 mostrar_mensaje_dialog(page, "❌ Error de Formato", "El presupuesto debe ser un número válido", "red")
                 page.update()
                 return

        # 3. Preparar datos para MongoDB
        nombre_proyecto = input_nombre.value.strip()
        
        nuevo_proyecto = {
            "nombre": nombre_proyecto,
            "codigo": input_codigo.value if input_codigo.value else f"PRY-{datetime.now().strftime('%H%M')}",
            "responsable": dropdown_responsable.value if dropdown_responsable.value else "Admin",
            "cliente": input_cliente.value,
            "presupuesto": presupuesto_val,
            "estado": dropdown_estado.value if dropdown_estado.value else "ACTIVO",
            "fecha_inicio": fecha_inicio_val[0],
            "fecha_fin": fecha_fin_val[0],
            "descripcion": input_descripcion.value if input_descripcion.value else "",
            "fecha_creacion": datetime.now(),
        }

        # Limpiar errores previos
        input_nombre.error_text = None
        input_codigo.error_text = None
        input_cliente.error_text = None
        input_presupuesto.error_text = None
        page.update()

        # 4. Crear el proyecto
        exito, resultado = crear_proyecto(nuevo_proyecto)

        if not exito:
            if isinstance(resultado, list):
                errores_texto = []
                for err in resultado:
                    campo = err["loc"][0]
                    msg = err["msg"]
                    
                    if campo == "nombre": input_nombre.error_text = msg
                    elif campo == "codigo": input_codigo.error_text = msg
                    elif campo == "cliente": input_cliente.error_text = msg
                    elif campo == "presupuesto": input_presupuesto.error_text = msg
                    else:
                        errores_texto.append(f"{campo}: {msg}")
                
                page.update()
                
                if errores_texto:
                    mostrar_mensaje_dialog(page, "❌ Error de Validación", f"❌ Error: {', '.join(errores_texto)}", "red")
                    page.update()
            else:
                mostrar_mensaje_dialog(page, "❌ Error de Sistema", f"❌ Error al guardar proyecto: {resultado}", "red")
                page.update()
            return

        # 5. Crear los departamentos asociados al proyecto
        deptos_creados = 0
        for depto in departamentos_temp:
            # Formatear miembros
            miembros_formato = []
            for m in depto.get("miembros", []):
                miembros_formato.append({
                    "id_usuario": str(m.get("_id")),
                    "nombre": m.get("nombre", ""),
                    "apellidos": m.get("apellidos", ""),
                    "identificador": m.get("identificador", ""),
                })
            
            datos_depto = {
                "nombre": depto["nombre"],
                "proyecto_asignado": nombre_proyecto,
                "miembros": miembros_formato,
                "fecha_creacion": datetime.now(),
            }
            
            exito_d, _ = crear_departamento(datos_depto)
            if exito_d:
                deptos_creados += 1

        # 6. Mensaje de éxito
        msg = f"✅ Proyecto '{nombre_proyecto}' creado"
        if deptos_creados > 0:
            msg += f" con {deptos_creados} departamento{'s' if deptos_creados > 1 else ''}"
        
        mostrar_mensaje_dialog(page, "✅ Éxito", msg, "green")
        await page.push_route("/gestionar_proyectos")
        page.update()

    # --- HELPERS DE INTERFAZ ---

    def crear_label(texto, obligatorio: bool = False):
        if obligatorio:
            return ft.Row([
                ft.Text(texto, size=11, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                ft.Text("*", size=11, color=COLOR_ROJO, weight=ft.FontWeight.BOLD),
            ], spacing=2)
        return ft.Text(texto, size=11, color=COLOR_LABEL, weight=ft.FontWeight.W_500)

    # Botón volver
    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight=ft.FontWeight.BOLD),
        on_click=btn_volver_click,
        ink=True,
        padding=10,
    )

    # --- CONTROLES DEL FORMULARIO ---
    input_nombre = ft.TextField(
        hint_text="Nombre del proyecto",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=40,
        content_padding=ft.Padding(left=10, right=10, top=8, bottom=8),
    )

    input_codigo = ft.TextField(
        hint_text="Ej: PRY-001",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=40,
        content_padding=ft.Padding(left=10, right=10, top=8, bottom=8),
    )

    input_cliente = ft.TextField(
        hint_text="Nombre de la empresa cliente",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=40,
        content_padding=ft.Padding(left=10, right=10, top=8, bottom=8),
    )

    input_presupuesto = ft.TextField(
        hint_text="0.00",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=40,
        content_padding=ft.Padding(left=10, right=10, top=8, bottom=8),
        suffix=ft.Text("€", color=COLOR_LABEL),
        keyboard_type=ft.KeyboardType.NUMBER
    )

    input_descripcion = ft.TextField(
        hint_text="Descripción breve del proyecto...",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        multiline=True,
        min_lines=2,
        max_lines=2,
        content_padding=10,
    )

    dropdown_responsable = ft.DropdownM2(
        hint_text="Selecciona responsable...",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        bgcolor="white",
        border_color=COLOR_BORDE,
        border_radius=5,
        height=40,
        expand=True,
        content_padding=ft.Padding(left=10, right=10),
        options=[]
    )

    dropdown_estado = ft.DropdownM2(
        hint_text="Estado...",
        value="ACTIVO",
        text_style=ft.TextStyle(size=12, color="black"),
        bgcolor="white",
        border_color=COLOR_BORDE,
        border_radius=5,
        height=40,
        expand=True,
        content_padding=ft.Padding(left=10, right=10),
        options=[
            ft.dropdownm2.Option("ACTIVO"),
            ft.dropdownm2.Option("PAUSADO"),
            ft.dropdownm2.Option("INACTIVO"),
        ]
    )

    # Componentes visuales para las fechas
    txt_fecha_inicio = ft.Text("Seleccionar...", size=11, color="#999999")
    txt_fecha_fin = ft.Text("Seleccionar...", size=11, color="#999999")

    # Inicializar lista visual de departamentos
    actualizar_lista_deptos_visual()

    # Sección de departamentos
    seccion_departamentos = ft.Container(
        border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)),
        border_radius=8,
        padding=10,
        content=ft.Column([
            ft.Row([
                ft.Text("Departamentos del Proyecto", size=12, color="black", weight="bold"),
                ft.Container(expand=True),
                ft.FilledButton(
                    "+ Añadir",
                    on_click=abrir_dialog_nuevo_departamento,
                    bgcolor=COLOR_LABEL,
                    color="white",
                    height=30,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=6),
                        text_style=ft.TextStyle(size=10),
                    ),
                ),
            ], alignment="spaceBetween"),
            ft.Container(
                height=120,
                content=ft.Column([lista_deptos_visual], scroll=ft.ScrollMode.AUTO),
            ),
        ], spacing=8),
    )

    # Contenedor del formulario con Scroll
    formulario = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Column([crear_label("Nombre del Proyecto", True), input_nombre], spacing=3),
            ft.Column([crear_label("Cliente / Empresa", True), input_cliente], spacing=3),
            
            ft.Row([
                ft.Column([crear_label("Código"), input_codigo], spacing=3, expand=True),
                ft.Column([crear_label("Presupuesto"), input_presupuesto], spacing=3, expand=True),
            ], spacing=10),

            ft.Column([crear_label("Responsable del Proyecto"), dropdown_responsable], spacing=3),
            
            ft.Row([
                ft.Column([
                    crear_label("Fecha Inicio", True),
                    ft.Container(
                        content=ft.Row([ft.Icon(ft.Icons.CALENDAR_MONTH, size=14, color=COLOR_LABEL), txt_fecha_inicio], spacing=5),
                        on_click=abrir_picker_inicio,
                        padding=ft.Padding(left=10, right=10, top=8, bottom=8), 
                        border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)), 
                        border_radius=5,
                        height=40,
                    )
                ], expand=True, spacing=3),
                ft.Column([
                    crear_label("Fecha Fin", True),
                    ft.Container(
                        content=ft.Row([ft.Icon(ft.Icons.CALENDAR_MONTH, size=14, color=COLOR_LABEL), txt_fecha_fin], spacing=5),
                        on_click=abrir_picker_fin,
                        padding=ft.Padding(left=10, right=10, top=8, bottom=8), 
                        border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)), 
                        border_radius=5,
                        height=40,
                    )
                ], expand=True, spacing=3),
            ], spacing=10),

            ft.Row([
                ft.Column([crear_label("Estado"), dropdown_estado], spacing=3, expand=True),
            ]),
            
            ft.Column([crear_label("Descripción"), input_descripcion], spacing=3),
            
            # Sección de departamentos
            seccion_departamentos,
            
            # Leyenda
            ft.Row([
                ft.Text("*", size=10, color=COLOR_ROJO, weight="bold"),
                ft.Text("Campos obligatorios", size=9, color="#666666", italic=True),
            ], spacing=2),
        ]
    )

    # Botón Crear
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

    # Tarjeta Blanca Principal
    tarjeta_blanca = ft.Container(
        width=380,
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color=COLOR_SOMBRA, offset=ft.Offset(0, 5)),
        content=ft.Container(
            padding=ft.Padding(left=18, right=18, top=55, bottom=15),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Container(height=520, content=formulario),
                    ft.Row([btn_crear], alignment=ft.MainAxisAlignment.CENTER),
                ]
            )
        )
    )

    # Header flotante
    header_flotante = ft.Container(
        width=220,
        height=50,
        bgcolor=COLOR_HEADER_BG,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text("CREAR PROYECTO", size=18, weight=ft.FontWeight.BOLD, color="white")
    )

    # Layout de la vista
    contenido_superpuesto = ft.Container(
        width=380,
        height=680,
        content=ft.Stack(
            controls=[
                ft.Container(content=tarjeta_blanca, top=30),
                ft.Container(content=header_flotante, top=0, left=80)
            ]
        )
    )

    # --- INICIALIZACIÓN ---
    cargar_datos_iniciales()

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

# Para probar directamente
def main(page):
    page.title = "App Tareas - Crear Proyecto"
    page.window.width = 420
    page.window.height = 800
    page.padding = 0 
    vista = VistaCrearProyecto(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)