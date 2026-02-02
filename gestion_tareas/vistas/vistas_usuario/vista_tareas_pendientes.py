import flet as ft
from datetime import datetime
from modelos.crud import obtener_tareas_por_estado, eliminar_tarea, completar_tarea, actualizar_tarea, obtener_todos_proyectos, obtener_todos_empleados, obtener_todos_departamentos, obtener_tareas_pendientes_usuario
from modelos.consultas import filtrar_y_ordenar
from servicios.sesion_service import obtener_usuario

def VistaTareasPendientes(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_SOMBRA_TARJETAS = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_ELIMINAR = "#E53935"
    COLOR_BTN_ANADIR = "#4682B4"
    COLOR_PRIORIDAD_ALTA = "#E53935"
    COLOR_PRIORIDAD_MEDIA = "#FF9800"
    COLOR_PRIORIDAD_BAJA = "#4CAF50"
    COLOR_COMPLETADO = "#4CAF50"
    COLOR_EDITAR = "#1976D2"

    TAGS_EMOJIS = {
        "Desarrollo": "👨‍💻", "Bug Fix": "🐛", "Testing": "🧪", "Diseño": "🎨",
        "Documentación": "📝", "DevOps": "⚙️", "Base de Datos": "🗄️",
        "API": "🔌", "Frontend": "🖥️", "Backend": "🔧",
    }

    #opciones de filtro
    FILTROS_TAGS = ["Todos", "Desarrollo", "Bug Fix", "Testing", "Diseño", "Documentación", "DevOps", "Base de Datos", "API", "Frontend", "Backend"]
    FILTROS_PROYECTO = ["Todos", "App Móvil v2.0", "Portal Web Cliente", "API REST Services", "Dashboard Analytics", "Sistema de Pagos", "CRM Interno", "Migración Cloud"]
    FILTROS_PRIORIDAD = ["Todas", "Alta", "Media", "Baja"]
    FILTROS_ORDEN = [
        "Más reciente primero", 
        "Más antiguo primero", 
        "Fecha ascendente",
        "Fecha descendente",
        "Alfabético A-Z", 
        "Alfabético Z-A",
        "Por prioridad alta",
        "Por prioridad baja",
        "Por proyecto",
    ]

    filtro_tag_actual = ["Todos"]
    filtro_proyecto_actual = ["Todos"]
    filtro_prioridad_actual = ["Todas"]
    filtro_orden_actual = ["Más reciente primero"]

    # Datos maestros para el diálogo de edición
    proyectos_db = []
    empleados_db = []
    departamentos_db = []
    usuario_actual = obtener_usuario()

    def cargar_datos_maestros():
        nonlocal proyectos_db, empleados_db, departamentos_db
        ex_p, lp = obtener_todos_proyectos()
        if ex_p: proyectos_db = lp
        ex_e, le = obtener_todos_empleados()
        if ex_e: empleados_db = le
        ex_d, ld = obtener_todos_departamentos()
        if ex_d: departamentos_db = ld

    cargar_datos_maestros()

    #cargamos las tareas pendientes de la BD
    def cargar_tareas_pendientes():
        """Obtiene las tareas pendientes del usuario (creadas por él o asignadas a él)"""
        # Obtenemos ID y nombre del usuario logueado
        id_usuario = str(usuario_actual.get("_id")) if usuario_actual else ""
        nombre_usuario = usuario_actual.get("nombre", "") if usuario_actual else ""
        
        # Usamos la nueva función que filtra por usuario
        exito, resultado = obtener_tareas_pendientes_usuario(id_usuario, nombre_usuario)
        
        if exito:
            tareas = []
            for t in resultado:
                #formateamos las fechas
                fecha_inicio = ""
                fecha_inicio_obj = None
                if t.get("fecha_inicio"):
                    fecha_inicio = t["fecha_inicio"].strftime("%d/%m/%y")
                    fecha_inicio_obj = t["fecha_inicio"]
                
                fecha_fin = ""
                fecha_fin_obj = None
                if t.get("fecha_limite"):
                    fecha_fin = t["fecha_limite"].strftime("%d/%m/%y")
                    fecha_fin_obj = t["fecha_limite"]
                
                #obtenemos los nombres de los asignados
                asignados_nombres = []
                asignados_obj = t.get("asignados", [])
                for asignado in asignados_obj:
                    if isinstance(asignado, dict):
                        asignados_nombres.append(asignado.get("nombre", "Sin nombre"))
                    else:
                        asignados_nombres.append(str(asignado))
                
                #obtenemos el primer tag o lo dejamos vacío
                tags = t.get("tags", [])
                tag = tags[0] if tags else "General"
                
                #creamos el diccionario de la tarea
                tarea = {
                    "_id": t.get("_id"),
                    "titulo": t.get("titulo", "Sin título"),
                    "tag": tag,
                    "tags": tags,  # Guardamos todos los tags
                    "emoji": t.get("icono", "📋"),
                    "proyecto": t.get("proyecto", "Sin proyecto"),
                    "id_proyecto": t.get("id_proyecto"),
                    "departamento": t.get("departamento", "General"),
                    "prioridad": t.get("prioridad", "Media"),
                    "asignados": asignados_nombres,
                    "asignados_obj": asignados_obj,  # Guardamos objetos completos
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin,
                    "fecha_inicio_obj": fecha_inicio_obj,
                    "fecha_fin_obj": fecha_fin_obj,
                    "requerimientos": [t.get("requisitos", "Sin requisitos")],
                    "requisitos_raw": t.get("requisitos", "Sin requisitos"),
                }
                tareas.append(tarea)
            return tareas
        else:
            #si hay error, devolvemos lista vacía
            print(f"Error cargando tareas: {resultado}")
            return []
    
    #cargamos las tareas al inicio
    TAREAS_PENDIENTES = cargar_tareas_pendientes()
    #guardamos todas las tareas para poder filtrar
    todas_las_tareas = []
    for t in TAREAS_PENDIENTES:
        todas_las_tareas.append(t.copy())
    
    def actualizar_lista_tareas():
        """Actualiza la lista de tareas en pantalla"""
        #preparamos los filtros
        filtros = {
            "prioridad": filtro_prioridad_actual[0],
            "tag": filtro_tag_actual[0],
            "proyecto": filtro_proyecto_actual[0]
        }
        
        #obtenemos el texto de búsqueda
        texto = ""
        if hasattr(input_busqueda, 'value'):
            texto = input_busqueda.value
        
        #filtramos y ordenamos usando la función importada
        tareas_filtradas = filtrar_y_ordenar(
            todas_las_tareas, 
            filtros, 
            texto, 
            filtro_orden_actual[0],
            "fecha_fin"
        )
        
        #actualizamos la lista
        lista_tareas.controls = []
        for tarea in tareas_filtradas:
            tarjeta = crear_tarjeta_tarea(tarea)
            lista_tareas.controls.append(tarjeta)
        page.update()

    def handle_completar_tarea(e, tarea):
        """Marca la tarea como completada en la BD y la quita de la lista de pendientes"""
        id_tarea = tarea.get("_id")
        if not id_tarea: return

        exito, resultado = completar_tarea(id_tarea)
        if exito:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"✅ Tarea '{tarea['titulo']}' marcada como realizada"),
                bgcolor=COLOR_COMPLETADO
            )
            # Volvemos a cargar de la BD y refrescamos la UI
            nonlocal todas_las_tareas
            todas_las_tareas = cargar_tareas_pendientes()
            actualizar_lista_tareas()
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error al completar: {resultado}"), bgcolor=COLOR_ELIMINAR)
        
        page.snack_bar.open = True
        page.update()

    def get_color_prioridad(prioridad):
        p = prioridad.lower()
        if p == "alta":
            return COLOR_PRIORIDAD_ALTA
        elif p == "media":
            return COLOR_PRIORIDAD_MEDIA
        else:
            return COLOR_PRIORIDAD_BAJA

    def btn_volver_click(e):
        page.go("/area_personal")

    def btn_buscar_click(e):
        #aplicamos el filtro de búsqueda
        actualizar_lista_tareas()
        page.snack_bar = ft.SnackBar(ft.Text(f"Buscando: {input_busqueda.value}"))
        page.snack_bar.open = True
        page.update()

    def btn_anadir_click(e):
        page.go("/nueva_tarea")

    # ============================================
    # DIÁLOGO DE EDICIÓN DE TAREA
    # ============================================
    def mostrar_dialog_editar(tarea):
        """Muestra un diálogo completo para editar todos los datos de la tarea"""
        
        # Estados temporales para la edición
        edit_tags_seleccionados = list(tarea.get("tags", []))
        edit_personas_seleccionadas = []
        
        # Reconstruir objetos de personas desde asignados_obj
        for asig in tarea.get("asignados_obj", []):
            if isinstance(asig, dict):
                # Buscar en empleados_db el objeto completo
                for emp in empleados_db:
                    if str(emp.get("_id")) == str(asig.get("id_usuario")):
                        edit_personas_seleccionadas.append(emp)
                        break
        
        edit_proyecto_obj = [None]
        # Buscar proyecto actual
        for p in proyectos_db:
            if p.get("nombre") == tarea.get("proyecto"):
                edit_proyecto_obj[0] = p
                break
        
        edit_departamento = [tarea.get("departamento")]
        edit_prioridad = [tarea.get("prioridad", "Media").capitalize()]
        edit_emoji = [tarea.get("emoji", "📋")]
        
        # Campos de texto
        input_titulo_edit = ft.TextField(
            value=tarea.get("titulo", ""),
            hint_text="Título de la tarea",
            border_color=COLOR_BORDE,
            text_style=ft.TextStyle(size=12, color="black"),
            height=40,
            content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
        )
        
        input_requisitos_edit = ft.TextField(
            value=tarea.get("requisitos_raw", ""),
            hint_text="Requerimientos...",
            border_color=COLOR_BORDE,
            text_style=ft.TextStyle(size=12, color="black"),
            multiline=True,
            min_lines=3,
            max_lines=5,
            content_padding=ft.padding.all(10),
        )
        
        # Textos de visualización
        txt_proyecto_edit = ft.Text(
            edit_proyecto_obj[0]["nombre"] if edit_proyecto_obj[0] else "Selecciona...",
            size=11,
            color="black" if edit_proyecto_obj[0] else "#999999",
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        txt_departamento_edit = ft.Text(
            edit_departamento[0] if edit_departamento[0] and edit_departamento[0] != "General" else "Selecciona...",
            size=11,
            color="black" if edit_departamento[0] and edit_departamento[0] != "General" else "#999999",
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        def get_texto_personas():
            if len(edit_personas_seleccionadas) == 0:
                return "Selecciona..."
            elif len(edit_personas_seleccionadas) == 1:
                return edit_personas_seleccionadas[0].get("nombre", "Usuario")
            else:
                return f"{edit_personas_seleccionadas[0].get('nombre')} (+{len(edit_personas_seleccionadas)-1})"
        
        txt_personas_edit = ft.Text(
            get_texto_personas(),
            size=11,
            color="black" if edit_personas_seleccionadas else "#999999",
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        def get_texto_tags():
            if len(edit_tags_seleccionados) == 0:
                return "Selecciona..."
            elif len(edit_tags_seleccionados) == 1:
                return edit_tags_seleccionados[0]
            else:
                return f"{len(edit_tags_seleccionados)} tags"
        
        txt_tags_edit = ft.Text(
            get_texto_tags(),
            size=11,
            color="black" if edit_tags_seleccionados else "#999999",
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        emoji_display = ft.Text(edit_emoji[0], size=30)
        
        # Date pickers
        txt_fecha_inicio = ft.Text(
            tarea.get("fecha_inicio") or "DD/MM/AA",
            size=11,
            color="black" if tarea.get("fecha_inicio") else "#999999",
        )
        txt_fecha_fin = ft.Text(
            tarea.get("fecha_fin") or "DD/MM/AA",
            size=11,
            color="black" if tarea.get("fecha_fin") else "#999999",
        )
        
        edit_fecha_inicio_val = [tarea.get("fecha_inicio_obj")]
        edit_fecha_fin_val = [tarea.get("fecha_fin_obj")]
        
        def on_fecha_inicio_change(e):
            if e.control.value:
                edit_fecha_inicio_val[0] = e.control.value
                txt_fecha_inicio.value = e.control.value.strftime("%d/%m/%y")
                txt_fecha_inicio.color = "black"
                page.update()
        
        def on_fecha_fin_change(e):
            if e.control.value:
                edit_fecha_fin_val[0] = e.control.value
                txt_fecha_fin.value = e.control.value.strftime("%d/%m/%y")
                txt_fecha_fin.color = "black"
                page.update()
        
        dp_inicio = ft.DatePicker(on_change=on_fecha_inicio_change)
        dp_fin = ft.DatePicker(on_change=on_fecha_fin_change)
        page.overlay.extend([dp_inicio, dp_fin])
        
        # Dropdown prioridad
        def on_prioridad_change(e):
            edit_prioridad[0] = e.control.value
        
        dropdown_prioridad_edit = ft.DropdownM2(
            value=edit_prioridad[0],
            options=[
                ft.dropdownm2.Option("Alta"),
                ft.dropdownm2.Option("Media"),
                ft.dropdownm2.Option("Baja"),
            ],
            width=100,
            height=40,
            text_style=ft.TextStyle(size=11, color="black"),
            border_color=COLOR_BORDE,
            content_padding=ft.padding.only(left=10),
            on_change=on_prioridad_change,
        )
        
        # --- Sub-diálogos de selección ---
        def abrir_sel_proyecto_edit(e):
            radio_p = ft.RadioGroup(
                value=edit_proyecto_obj[0]["nombre"] if edit_proyecto_obj[0] else None,
                content=ft.Column([
                    ft.Radio(value=p["nombre"], label=p["nombre"], label_style=ft.TextStyle(size=11, color="black"))
                    for p in proyectos_db
                ], spacing=2)
            )
            def ok_click(e):
                if radio_p.value:
                    for p in proyectos_db:
                        if p["nombre"] == radio_p.value:
                            edit_proyecto_obj[0] = p
                            break
                    txt_proyecto_edit.value = edit_proyecto_obj[0]["nombre"]
                    txt_proyecto_edit.color = "black"
                    # Reset departamento
                    edit_departamento[0] = None
                    txt_departamento_edit.value = "Selecciona..."
                    txt_departamento_edit.color = "#999999"
                dg.open = False
                page.update()
            dg = ft.AlertDialog(
                title=ft.Text("Proyecto", size=14, weight="bold", color="black"),
                content=ft.Container(width=280, height=200, content=ft.ListView([radio_p])),
                actions=[ft.TextButton("Ok", on_click=ok_click)],
                bgcolor="white"
            )
            page.overlay.append(dg)
            dg.open = True
            page.update()
        
        def abrir_sel_departamento_edit(e):
            if not edit_proyecto_obj[0]:
                page.snack_bar = ft.SnackBar(ft.Text("⚠️ Selecciona un proyecto primero"), bgcolor="orange")
                page.snack_bar.open = True
                page.update()
                return
            filt = [d for d in departamentos_db if d.get("proyecto_asignado") == edit_proyecto_obj[0]["nombre"]]
            radio_d = ft.RadioGroup(
                value=edit_departamento[0],
                content=ft.Column([
                    ft.Radio(value=d["nombre"], label=d["nombre"], label_style=ft.TextStyle(size=11, color="black"))
                    for d in filt
                ], spacing=2)
            )
            def ok_click(e):
                if radio_d.value:
                    edit_departamento[0] = radio_d.value
                    txt_departamento_edit.value = radio_d.value
                    txt_departamento_edit.color = "black"
                dg.open = False
                page.update()
            content = ft.ListView([radio_d]) if filt else ft.Text("No hay departamentos vinculados", size=11, color="red")
            dg = ft.AlertDialog(
                title=ft.Text("Departamento", size=14, weight="bold", color="black"),
                content=ft.Container(width=280, height=200, content=content),
                actions=[ft.TextButton("Ok", on_click=ok_click)],
                bgcolor="white"
            )
            page.overlay.append(dg)
            dg.open = True
            page.update()
        
        def abrir_sel_personas_edit(e):
            mi_id = str(usuario_actual.get("_id")) if usuario_actual else ""
            def on_c(ev):
                emp = ev.control.data
                if ev.control.value:
                    if emp not in edit_personas_seleccionadas:
                        edit_personas_seleccionadas.append(emp)
                else:
                    if emp in edit_personas_seleccionadas:
                        edit_personas_seleccionadas.remove(emp)
            chks = []
            for emp in empleados_db:
                esta_sel = any(str(s.get("_id")) == str(emp.get("_id")) for s in edit_personas_seleccionadas)
                es_yo = str(emp.get("_id")) == mi_id
                # Formato: Nombre Apellido (identificador)
                nombre = emp.get('nombre', '')
                apellidos = emp.get('apellidos', '')
                identificador = emp.get('identificador', '')
                label_texto = f"{nombre} {apellidos} ({identificador})"
                if es_yo:
                    label_texto += " - Tú"
                chks.append(ft.Checkbox(
                    label=label_texto,
                    value=esta_sel,
                    data=emp,
                    on_change=on_c,
                    label_style=ft.TextStyle(size=10, color="black")
                ))
            def ok_click(e):
                txt_personas_edit.value = get_texto_personas()
                txt_personas_edit.color = "black" if edit_personas_seleccionadas else "#999999"
                dg.open = False
                page.update()
            dg = ft.AlertDialog(
                title=ft.Text("Asignar a", size=14, weight="bold", color="black"),
                content=ft.Container(width=320, height=280, content=ft.ListView(chks)),
                actions=[ft.TextButton("Ok", on_click=ok_click)],
                bgcolor="white"
            )
            page.overlay.append(dg)
            dg.open = True
            page.update()
        
        def abrir_sel_tags_edit(e):
            def on_t(ev):
                tag = ev.control.data
                if ev.control.value:
                    if tag not in edit_tags_seleccionados:
                        edit_tags_seleccionados.append(tag)
                else:
                    if tag in edit_tags_seleccionados:
                        edit_tags_seleccionados.remove(tag)
            chks = [
                ft.Checkbox(
                    label=f"{TAGS_EMOJIS[t]} {t}",
                    value=t in edit_tags_seleccionados,
                    data=t,
                    on_change=on_t,
                    label_style=ft.TextStyle(size=11, color="black")
                )
                for t in TAGS_EMOJIS.keys()
            ]
            def ok_click(e):
                txt_tags_edit.value = get_texto_tags()
                txt_tags_edit.color = "black" if edit_tags_seleccionados else "#999999"
                if edit_tags_seleccionados:
                    edit_emoji[0] = TAGS_EMOJIS[edit_tags_seleccionados[0]]
                    emoji_display.value = edit_emoji[0]
                dg.open = False
                page.update()
            dg = ft.AlertDialog(
                title=ft.Text("Tags", size=14, weight="bold", color="black"),
                content=ft.Container(width=280, height=300, content=ft.ListView(chks)),
                actions=[ft.TextButton("Ok", on_click=ok_click)],
                bgcolor="white"
            )
            page.overlay.append(dg)
            dg.open = True
            page.update()
        
        # --- Guardar cambios ---
        def guardar_edicion(e):
            # Validaciones
            if not input_titulo_edit.value or not input_titulo_edit.value.strip():
                page.snack_bar = ft.SnackBar(ft.Text("❌ El título es obligatorio"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return
            
            if not edit_proyecto_obj[0]:
                page.snack_bar = ft.SnackBar(ft.Text("❌ Selecciona un proyecto"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return
            
            # Preparar datos actualizados
            asignados_fmt = [
                {"id_usuario": str(p.get("_id")), "nombre": p.get("nombre")}
                for p in edit_personas_seleccionadas
            ]
            
            datos_actualizados = {
                "titulo": input_titulo_edit.value.strip(),
                "requisitos": input_requisitos_edit.value if input_requisitos_edit.value else "Sin requisitos",
                "tags": edit_tags_seleccionados,
                "icono": edit_emoji[0],
                "id_proyecto": str(edit_proyecto_obj[0].get("_id")),
                "proyecto": edit_proyecto_obj[0].get("nombre"),
                "departamento": edit_departamento[0] if edit_departamento[0] else "General",
                "prioridad": edit_prioridad[0].lower(),
                "asignados": asignados_fmt,
                "fecha_inicio": edit_fecha_inicio_val[0] if edit_fecha_inicio_val[0] else datetime.now(),
                "fecha_limite": edit_fecha_fin_val[0],
            }
            
            # Llamar a actualizar_tarea
            exito, resultado = actualizar_tarea(tarea.get("_id"), datos_actualizados)
            
            dialog_editar.open = False
            
            if exito:
                page.snack_bar = ft.SnackBar(ft.Text(f"✅ Tarea actualizada correctamente"), bgcolor=COLOR_COMPLETADO)
                page.snack_bar.open = True
                # Recargar tareas
                nonlocal todas_las_tareas
                todas_las_tareas = cargar_tareas_pendientes()
                actualizar_lista_tareas()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {resultado}"), bgcolor=COLOR_ELIMINAR)
                page.snack_bar.open = True
            
            page.update()
        
        def cancelar_edicion(e):
            dialog_editar.open = False
            page.update()
        
        # --- Contenido del diálogo ---
        contenido_edicion = ft.Container(
            width=340,
            height=480,
            content=ft.Column(
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    # Emoji + Título
                    ft.Row([
                        emoji_display,
                        ft.Column([
                            ft.Row([
                                ft.Text("Título", size=10, color=COLOR_LABEL, weight="bold"),
                                ft.Text("*", size=10, color="#D32F2F", weight="bold"),
                            ], spacing=2),
                            input_titulo_edit,
                        ], expand=True, spacing=2),
                    ], spacing=10, vertical_alignment="start"),
                    
                    # Proyecto + Departamento
                    ft.Row([
                        ft.Column([
                            ft.Row([
                                ft.Text("Proyecto", size=10, color=COLOR_LABEL, weight="bold"),
                                ft.Text("*", size=10, color="#D32F2F", weight="bold"),
                            ], spacing=2),
                            ft.Container(
                                content=txt_proyecto_edit,
                                border=ft.border.all(1, COLOR_BORDE),
                                border_radius=5,
                                padding=ft.padding.symmetric(horizontal=10, vertical=8),
                                height=38,
                                on_click=abrir_sel_proyecto_edit,
                                ink=True,
                            ),
                        ], expand=True, spacing=2),
                        ft.Column([
                            ft.Text("Departamento", size=10, color=COLOR_LABEL, weight="bold"),
                            ft.Container(
                                content=txt_departamento_edit,
                                border=ft.border.all(1, COLOR_BORDE),
                                border_radius=5,
                                padding=ft.padding.symmetric(horizontal=10, vertical=8),
                                height=38,
                                on_click=abrir_sel_departamento_edit,
                                ink=True,
                            ),
                        ], expand=True, spacing=2),
                    ], spacing=10),
                    
                    # Asignados
                    ft.Column([
                        ft.Text("Asignar a", size=10, color=COLOR_LABEL, weight="bold"),
                        ft.Container(
                            content=txt_personas_edit,
                            border=ft.border.all(1, COLOR_BORDE),
                            border_radius=5,
                            padding=ft.padding.symmetric(horizontal=10, vertical=8),
                            height=38,
                            on_click=abrir_sel_personas_edit,
                            ink=True,
                        ),
                    ], spacing=2),
                    
                    # Tags + Prioridad
                    ft.Row([
                        ft.Column([
                            ft.Text("Tags", size=10, color=COLOR_LABEL, weight="bold"),
                            ft.Container(
                                content=txt_tags_edit,
                                border=ft.border.all(1, COLOR_BORDE),
                                border_radius=5,
                                padding=ft.padding.symmetric(horizontal=10, vertical=8),
                                height=38,
                                width=120,
                                on_click=abrir_sel_tags_edit,
                                ink=True,
                            ),
                        ], spacing=2),
                        ft.Column([
                            ft.Text("Prioridad", size=10, color=COLOR_LABEL, weight="bold"),
                            dropdown_prioridad_edit,
                        ], spacing=2),
                    ], spacing=10, alignment="spaceBetween"),
                    
                    # Fechas
                    ft.Row([
                        ft.Column([
                            ft.Text("Fecha Inicio", size=10, color=COLOR_LABEL, weight="bold"),
                            ft.Container(
                                content=txt_fecha_inicio,
                                border=ft.border.all(1, COLOR_BORDE),
                                border_radius=5,
                                padding=ft.padding.symmetric(horizontal=10, vertical=8),
                                height=38,
                                on_click=lambda _: setattr(dp_inicio, "open", True) or page.update(),
                                ink=True,
                            ),
                        ], expand=True, spacing=2),
                        ft.Column([
                            ft.Text("Fecha Límite", size=10, color=COLOR_LABEL, weight="bold"),
                            ft.Container(
                                content=txt_fecha_fin,
                                border=ft.border.all(1, COLOR_BORDE),
                                border_radius=5,
                                padding=ft.padding.symmetric(horizontal=10, vertical=8),
                                height=38,
                                on_click=lambda _: setattr(dp_fin, "open", True) or page.update(),
                                ink=True,
                            ),
                        ], expand=True, spacing=2),
                    ], spacing=10),
                    
                    # Requerimientos
                    ft.Column([
                        ft.Text("Requerimientos", size=10, color=COLOR_LABEL, weight="bold"),
                        input_requisitos_edit,
                    ], spacing=2),
                    
                    # Leyenda
                    ft.Row([
                        ft.Text("*", size=10, color="#D32F2F", weight="bold"),
                        ft.Text("Campos obligatorios", size=9, color="#666666", italic=True),
                    ], spacing=2),
                ]
            )
        )
        
        dialog_editar = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.EDIT, color=COLOR_EDITAR, size=22),
                ft.Text("Editar Tarea", size=16, weight="bold", color="black"),
            ], spacing=8),
            bgcolor="white",
            content=contenido_edicion,
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_edicion),
                ft.ElevatedButton(
                    "Guardar",
                    on_click=guardar_edicion,
                    bgcolor=COLOR_EDITAR,
                    color="white",
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.overlay.append(dialog_editar)
        dialog_editar.open = True
        page.update()

    #dialog detalle tarea
    def mostrar_detalle_tarea(tarea):
        requerimientos_list = ft.Column(
            spacing=6,
            controls=[
                ft.Text(f"• {req}", size=11, color="black")
                for req in tarea["requerimientos"]
            ]
        )

        asignados_text = ", ".join(tarea["asignados"]) if tarea["asignados"] else "Sin asignar"

        dialog_detalle = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Text(tarea["emoji"], size=26),
                    ft.Container(
                        expand=True,
                        content=ft.Text(tarea["titulo"], size=13, weight=ft.FontWeight.BOLD, color="black"),
                    ),
                ],
                spacing=8,
            ),
            bgcolor="white",
            content=ft.Container(
                width=320,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    tight=True,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        #info básica
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Container(
                                    bgcolor=get_color_prioridad(tarea["prioridad"]),
                                    border_radius=10,
                                    padding=ft.padding.only(left=8, right=8, top=2, bottom=2),
                                    content=ft.Text(tarea["prioridad"], size=10, color="white", weight=ft.FontWeight.BOLD),
                                ),
                                ft.Row(
                                    spacing=3,
                                    controls=[
                                        ft.Text("TAG:", size=10, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                        ft.Text(tarea["tag"], size=10, color="black", weight=ft.FontWeight.W_500),
                                    ]
                                ),
                            ]
                        ),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        #proyecto y departamento
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(spacing=2, controls=[
                                    ft.Text("Proyecto", size=10, color=COLOR_LABEL),
                                    ft.Text(tarea["proyecto"], size=11, color="black", weight=ft.FontWeight.W_500),
                                ]),
                                ft.Column(spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END, controls=[
                                    ft.Text("Departamento", size=10, color=COLOR_LABEL),
                                    ft.Text(tarea["departamento"], size=11, color="black", weight=ft.FontWeight.W_500),
                                ]),
                            ]
                        ),
                        #asignados
                        ft.Column(spacing=2, controls=[
                            ft.Text("Asignados", size=10, color=COLOR_LABEL),
                            ft.Text(asignados_text, size=11, color="black"),
                        ]),
                        #fechas
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(
                                    spacing=3,
                                    controls=[
                                        ft.Text("Inicio:", size=10, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                        ft.Text(tarea["fecha_inicio"], size=10, color="black", weight=ft.FontWeight.W_500),
                                    ]
                                ),
                                ft.Row(
                                    spacing=3,
                                    controls=[
                                        ft.Text("Fin:", size=10, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                        ft.Text(tarea["fecha_fin"], size=10, color="black", weight=ft.FontWeight.W_500),
                                    ]
                                ),
                            ]
                        ),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        #requerimientos
                        ft.Text("Requerimientos:", size=12, color="black", weight=ft.FontWeight.BOLD),
                        ft.Container(
                            height=140,
                            content=ft.ListView(
                                controls=[requerimientos_list],
                                spacing=5,
                            ),
                        ),
                    ]
                ),
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog(dialog_detalle)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        def cerrar_dialog(dialog):
            dialog.open = False
            page.update()

        page.overlay.append(dialog_detalle)
        dialog_detalle.open = True
        page.update()

    #dialog confirmar eliminar
    def mostrar_confirmar_eliminar(tarea):
        def confirmar_eliminar(e):
            dialog_confirmar.open = False
            
            #eliminamos la tarea de la BD
            id_tarea = tarea.get("_id")
            if id_tarea:
                exito, resultado = eliminar_tarea(id_tarea)
                if exito:
                    page.snack_bar = ft.SnackBar(ft.Text(f"✅ Tarea '{tarea['titulo']}' eliminada"))
                    page.snack_bar.open = True
                    #recargamos la lista de tareas
                    nonlocal todas_las_tareas
                    todas_las_tareas = cargar_tareas_pendientes()
                    actualizar_lista_tareas()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error al eliminar: {resultado}"))
                    page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(ft.Text("❌ Error: No se pudo identificar la tarea"))
                page.snack_bar.open = True
            
            page.update()

        def cancelar_eliminar(e):
            dialog_confirmar.open = False
            page.update()

        dialog_confirmar = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar tarea", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=280,
                bgcolor="white",
                content=ft.Column(
                    spacing=10,
                    tight=True,
                    controls=[
                        ft.Text("¿Estás seguro de que deseas eliminar esta tarea?", size=12, color="black"),
                        ft.Container(
                            bgcolor="#FFF3F3",
                            border_radius=8,
                            padding=10,
                            content=ft.Column(
                                spacing=3,
                                controls=[
                                    ft.Row(
                                        spacing=5,
                                        controls=[
                                            ft.Text(tarea["emoji"], size=16),
                                            ft.Text(tarea["titulo"], size=12, color="black", weight=ft.FontWeight.BOLD, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                        ]
                                    ),
                                    ft.Text(f"Proyecto: {tarea['proyecto']}", size=10, color="#666666"),
                                ],
                            ),
                        ),
                        ft.Text("Esta acción no se puede deshacer.", size=11, color=COLOR_ELIMINAR, italic=True),
                    ]
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_eliminar),
                ft.TextButton("Eliminar", on_click=confirmar_eliminar, style=ft.ButtonStyle(color=COLOR_ELIMINAR)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_confirmar)
        dialog_confirmar.open = True
        page.update()

    #dialog filtros
    def mostrar_dialog_filtros(e):
        radio_orden = ft.RadioGroup(
            value=filtro_orden_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=orden, label=orden, label_style=ft.TextStyle(size=11, color="black")) 
                    for orden in FILTROS_ORDEN
                ],
                spacing=2,
            ),
        )

        radio_prioridad = ft.RadioGroup(
            value=filtro_prioridad_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=prio, label=prio, label_style=ft.TextStyle(size=11, color="black")) 
                    for prio in FILTROS_PRIORIDAD
                ],
                spacing=2,
            ),
        )

        def aplicar_filtros(e):
            filtro_orden_actual[0] = radio_orden.value
            filtro_prioridad_actual[0] = radio_prioridad.value
            dialog_filtros.open = False
            #actualizamos la lista con los nuevos filtros
            actualizar_lista_tareas()
            page.snack_bar = ft.SnackBar(ft.Text("✅ Filtros aplicados"))
            page.snack_bar.open = True
            page.update()

        def limpiar_filtros(e):
            radio_orden.value = "Más reciente primero"
            radio_prioridad.value = "Todas"
            filtro_orden_actual[0] = "Más reciente primero"
            filtro_prioridad_actual[0] = "Todas"
            page.update()

        dialog_filtros = ft.AlertDialog(
            modal=True,
            title=ft.Text("Filtros y Orden", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=400,
                bgcolor="white",
                content=ft.Column(
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("Ordenar por:", size=12, color=COLOR_LABEL, weight=ft.FontWeight.BOLD),
                        radio_orden,
                        ft.Divider(height=1, color=COLOR_BORDE),
                        ft.Text("Filtrar por prioridad:", size=12, color=COLOR_LABEL, weight=ft.FontWeight.BOLD),
                        radio_prioridad,
                    ]
                ),
            ),
            actions=[
                ft.TextButton("Limpiar", on_click=limpiar_filtros),
                ft.TextButton("Aplicar", on_click=aplicar_filtros),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_filtros)
        dialog_filtros.open = True
        page.update()

    def crear_tarjeta_tarea(tarea):
        """Crea una tarjeta para cada tarea pendiente con botones de editar, eliminar y completar"""
        return ft.Container(
            bgcolor="white",
            border_radius=10,
            padding=ft.padding.all(12),
            margin=ft.margin.only(bottom=10),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=5,
                color=COLOR_SOMBRA_TARJETAS,
                offset=ft.Offset(0, 2),
            ),
            content=ft.Column(
                spacing=8,
                controls=[
                    # Fila 1: Emoji + Título + Botón Editar + Botón Eliminar
                    ft.Row(
                        spacing=6,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(tarea["emoji"], size=22),
                            ft.Text(
                                tarea["titulo"],
                                size=12,
                                color="black",
                                weight=ft.FontWeight.BOLD,
                                expand=True,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            # BOTÓN EDITAR
                            ft.Container(
                                content=ft.Icon(ft.Icons.EDIT, size=16, color=COLOR_EDITAR),
                                on_click=lambda e, t=tarea: mostrar_dialog_editar(t),
                                ink=True,
                                padding=ft.padding.all(6),
                                border_radius=5,
                                tooltip="Editar tarea",
                            ),
                            # BOTÓN ELIMINAR
                            ft.Container(
                                content=ft.Text("X", size=14, color=COLOR_ELIMINAR, weight=ft.FontWeight.BOLD),
                                on_click=lambda e, t=tarea: mostrar_confirmar_eliminar(t),
                                ink=True,
                                padding=ft.padding.all(6),
                                border_radius=5,
                                tooltip="Eliminar tarea",
                            ),
                        ]
                    ),
                    # Fila 2: Proyecto + Prioridad (Badge)
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(tarea["proyecto"], size=10, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                            ft.Container(
                                bgcolor=get_color_prioridad(tarea["prioridad"]),
                                border_radius=8,
                                padding=ft.padding.only(left=6, right=6, top=1, bottom=1),
                                content=ft.Text(tarea["prioridad"], size=9, color="white", weight=ft.FontWeight.BOLD),
                            ),
                        ]
                    ),
                    # Fila 3: Tag + Fecha rango
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=3,
                                controls=[
                                    ft.Text("TAG:", size=9, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                    ft.Text(tarea["tag"], size=9, color="black", weight=ft.FontWeight.W_500),
                                ]
                            ),
                            ft.Text(
                                f"{tarea['fecha_inicio']} - {tarea['fecha_fin']}" if tarea['fecha_fin'] else f"{tarea['fecha_inicio']} - Sin fecha",
                                size=9,
                                color="#666666",
                            ),
                        ]
                    ),
                    ft.Divider(height=1, color="#F0F0F0"),
                    # Fila 4: Botones de Acción
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.TextButton(
                                "Ver detalles",
                                icon=ft.Icons.INFO_OUTLINE,
                                on_click=lambda e, t=tarea: mostrar_detalle_tarea(t),
                                style=ft.ButtonStyle(color=COLOR_LABEL, text_style=ft.TextStyle(size=10))
                            ),
                            ft.ElevatedButton(
                                "Marcar completada",
                                icon=ft.Icons.CHECK_CIRCLE,
                                bgcolor=COLOR_COMPLETADO,
                                color="white",
                                height=34,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    text_style=ft.TextStyle(size=11, weight="bold")
                                ),
                                on_click=lambda e, t=tarea: handle_completar_tarea(e, t)
                            )
                        ]
                    )
                ]
            ),
        )

    #campo de búsqueda
    input_busqueda = ft.TextField(
        hint_text="Buscar por palabras clave...",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=38,
        expand=True,
        content_padding=ft.padding.only(left=10, right=10, top=8, bottom=8),
    )

    #botón filtrar
    btn_filtrar = ft.Container(
        content=ft.Text("Filtrar", size=11, color="black"),
        bgcolor="white",
        border=ft.border.all(1, COLOR_BORDE),
        border_radius=5,
        padding=ft.padding.only(left=12, right=12, top=8, bottom=8),
        on_click=mostrar_dialog_filtros,
        ink=True,
    )

    #botón buscar (icono lupa)
    btn_buscar = ft.Container(
        content=ft.Icon(ft.Icons.SEARCH, size=20, color="white"),
        bgcolor=COLOR_LABEL,
        border_radius=5,
        padding=ft.padding.all(8),
        on_click=btn_buscar_click,
        ink=True,
    )

    #fila de búsqueda y filtros
    fila_busqueda = ft.Row(
        spacing=8,
        controls=[
            input_busqueda,
            btn_filtrar,
            btn_buscar,
        ]
    )

    #lista de tareas
    lista_tareas = ft.ListView(
        spacing=0,
        controls=[crear_tarjeta_tarea(tarea) for tarea in TAREAS_PENDIENTES],
        expand=True,
    )

    #botón añadir tarea
    btn_anadir = ft.Container(
        width=160,
        height=44,
        bgcolor=COLOR_BTN_ANADIR,
        border_radius=22,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_anadir_click,
        content=ft.Text("Añadir Tarea", color="white", weight=ft.FontWeight.BOLD, size=14),
    )

    #tarjeta blanca principal
    tarjeta_blanca = ft.Container(
        width=400,
        height=720,
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=COLOR_SOMBRA),
        content=ft.Column(
            spacing=0,
            controls=[
                #flecha de retroceso
                ft.Container(
                    padding=ft.padding.only(left=15, top=10, bottom=5),
                    alignment=ft.Alignment(-1, 0),
                    content=ft.Container(
                        content=ft.Text("←", size=26, color="black", weight="bold"),
                        on_click=btn_volver_click,
                        ink=True,
                        border_radius=50,
                        padding=3,
                    ),
                ),

                #header azul
                ft.Container(
                    height=55,
                    width=400,
                    bgcolor=COLOR_HEADER_BG,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("TAREAS PENDIENTES", size=18, weight=ft.FontWeight.BOLD, color="white")
                ),
                
                #contenido
                ft.Container(
                    padding=ft.padding.only(left=18, right=18, top=15, bottom=15),
                    expand=True,
                    content=ft.Column(
                        spacing=12,
                        expand=True,
                        controls=[
                            fila_busqueda,
                            lista_tareas,
                            #botón añadir centrado
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[btn_anadir]
                            ),
                        ]
                    )
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
        alignment=ft.Alignment(0, 0), 
        content=tarjeta_blanca
    )