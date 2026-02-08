import flet as ft
from datetime import datetime
from modelos.crud import crear_tarea, obtener_todos_proyectos, obtener_todos_empleados, obtener_todos_departamentos
from servicios.sesion_service import obtener_usuario

def VistaNuevaTarea(page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_SOMBRA_TARJETAS = "#40000000"
    COLOR_BTN_CREAR = "#4682B4"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"

    TAGS_EMOJIS = {
        "Desarrollo": "👨‍💻",
        "Bug Fix": "🐛",
        "Testing": "🧪",
        "Diseño": "🎨",
        "Documentación": "📝",
        "DevOps": "⚙️",
        "Base de Datos": "🗄️",
        "API": "🔌",
        "Frontend": "🖥️",
        "Backend": "🔧",
    }

    # --- VARIABLES DE ESTADO Y DATOS REALES ---
    proyectos_db = []
    empleados_db = []
    departamentos_db = []

    # AÑADIDO: obtener usuario de sesión para autoasignación
    usuario_creador = obtener_usuario()

    tags_seleccionados = []
    # MODIFICADO: preseleccionar al usuario creador
    personas_seleccionadas = [usuario_creador] if usuario_creador else []
    emoji_index_actual = [0]
    proyecto_seleccionado_obj = [None]
    departamento_seleccionado_nombre = [None]
    prioridad_seleccionada = ["Media"]

    # --- CARGAR DATOS DE LA BD ---
    def cargar_datos_iniciales():
        nonlocal proyectos_db, empleados_db, departamentos_db
        
        exito_p, proys = obtener_todos_proyectos()
        if exito_p: proyectos_db = proys
        
        exito_e, emps = obtener_todos_empleados()
        if exito_e: empleados_db = emps

        exito_d, deptos = obtener_todos_departamentos()
        if exito_d: departamentos_db = deptos

    cargar_datos_iniciales()

    # --- COMPONENTES DE FECHA ---
    # MODIFICADO: fecha inicio por defecto a hoy
    fecha_inicio_texto = ft.Text(
        datetime.now().strftime("%d/%m/%y"), 
        size=12, 
        color="black", 
        weight=ft.FontWeight.W_500
    )
    fecha_fin_texto = ft.Text("DD/MM/AA", size=12, color="black", weight=ft.FontWeight.W_500)

    emoji_text = ft.Text("📋", size=35)

    # MODIFICADO: mostrar nombre del usuario creador por defecto
    nombre_usuario_creador = usuario_creador.get("nombre", "Usuario") if usuario_creador else "Usuario"
    texto_personas_seleccionadas = ft.Text(
        nombre_usuario_creador, 
        size=11, 
        color="black",  # MODIFICADO: color negro porque hay selección
        overflow=ft.TextOverflow.ELLIPSIS,
        max_lines=1,
    )
    
    texto_tags_seleccionados = ft.Text(
        "Selecciona...", 
        size=11, 
        color="#999999",
        overflow=ft.TextOverflow.ELLIPSIS,
        max_lines=1,
    )

    texto_proyecto_seleccionado = ft.Text(
        "Selecciona proyecto...", 
        size=11, 
        color="#999999",
        overflow=ft.TextOverflow.ELLIPSIS,
        max_lines=1,
    )

    texto_departamento_seleccionado = ft.Text(
        "Selecciona departamento...", 
        size=11, 
        color="#999999",
        overflow=ft.TextOverflow.ELLIPSIS,
        max_lines=1,
    )

    def on_fecha_inicio_change(e):
        if e.control.value:
            fecha_inicio_texto.value = e.control.value.strftime("%d/%m/%y")
            page.update()

    def on_fecha_fin_change(e):
        if e.control.value:
            fecha_fin_texto.value = e.control.value.strftime("%d/%m/%y")
            page.update()

    date_picker_inicio = ft.DatePicker(
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
        on_change=on_fecha_inicio_change,
    )

    date_picker_fin = ft.DatePicker(
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
        on_change=on_fecha_fin_change,
    )

    page.overlay.append(date_picker_inicio)
    page.overlay.append(date_picker_fin)

    # --- LÓGICA DE GUARDADO REAL ---
    async def ejecutar_creacion_tarea():
        """Función que ejecuta la creación real de la tarea"""
        asignados_formateados = []
        for p in personas_seleccionadas:
            asignados_formateados.append({
                "id_usuario": str(p.get("_id")),
                "nombre": p.get("nombre", "Usuario")
            })

        nueva_tarea_data = {
            "titulo": input_titulo.value,
            "requisitos": texto_requerimientos.value if texto_requerimientos.value else "Sin requisitos",
            "estado": "pendiente",
            "tags": tags_seleccionados,
            "icono": emoji_text.value,
            "id_proyecto": str(proyecto_seleccionado_obj[0].get("_id")),
            "proyecto": proyecto_seleccionado_obj[0].get("nombre"),
            "prioridad": prioridad_seleccionada[0].lower(),
            "asignados": asignados_formateados,
            "compartido_por": nombre_usuario_creador,
            "fecha_inicio": date_picker_inicio.value if date_picker_inicio.value else datetime.now(),
            "fecha_limite": date_picker_fin.value,  # Puede ser None
            "atrasado": False
        }

        exito, resultado = crear_tarea(nueva_tarea_data)
        if exito:
            mostrar_mensaje_dialog(page, "✅ Éxito", f"Tarea creada correctamente", "green")
            await page.push_route("/tareas_pendientes")
        else:
            mostrar_mensaje_dialog(page, "❌ Error", f"Error: {resultado}", "red")
        
        page.update()

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

    def mostrar_dialog_campos_faltantes(campos_faltantes):
        """Muestra popup con los campos obligatorios que faltan"""
        lista_campos = ft.Column(
            controls=[
                ft.Row([
                    ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color="#E65100", size=18),
                    ft.Text(campo, size=13, color="black")
                ], spacing=8)
                for campo in campos_faltantes
            ],
            spacing=8
        )
        
        def cerrar_dialog(e):
            dialog_faltantes.open = False
            page.update()
        
        dialog_faltantes = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.ERROR_OUTLINE, color="#D32F2F", size=24),
                ft.Text("Campos obligatorios", size=16, weight=ft.FontWeight.BOLD, color="#D32F2F")
            ], spacing=10),
            bgcolor="white",
            content=ft.Container(
                width=280,
                content=ft.Column([
                    ft.Text("Por favor, completa los siguientes campos:", size=12, color="#666666"),
                    ft.Container(height=10),
                    lista_campos,
                ], spacing=5, tight=True)
            ),
            actions=[
                ft.TextButton("Entendido", on_click=cerrar_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.overlay.append(dialog_faltantes)
        dialog_faltantes.open = True
        page.update()

    def mostrar_dialog_confirmar_sin_fecha():
        """Muestra popup de confirmación cuando no hay fecha límite"""
        def cancelar(e):
            dialog_confirmar.open = False
            page.update()
        
        async def confirmar_creacion(e):
            dialog_confirmar.open = False
            page.update()
            await ejecutar_creacion_tarea()
        
        dialog_confirmar = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.HELP_OUTLINE, color="#FF9800", size=24),
                ft.Text("Sin fecha límite", size=16, weight=ft.FontWeight.BOLD, color="#E65100")
            ], spacing=10),
            bgcolor="white",
            content=ft.Container(
                width=300,
                content=ft.Column([
                    ft.Text(
                        "No has establecido una fecha límite para esta tarea.",
                        size=13,
                        color="black"
                    ),
                    ft.Container(height=5),
                    ft.Text(
                        "Las tareas sin fecha límite no aparecerán en recordatorios ni alertas de vencimiento.",
                        size=11,
                        color="#666666",
                        italic=True
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "¿Deseas crear la tarea de todas formas?",
                        size=13,
                        color="black",
                        weight=ft.FontWeight.W_500
                    ),
                ], spacing=2, tight=True)
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                 ft.FilledButton(
                    "Crear sin fecha",
                    on_click=confirmar_creacion,
                    bgcolor="#FF9800",
                    color="white"
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.overlay.append(dialog_confirmar)
        dialog_confirmar.open = True
        page.update()

    async def btn_crear_click(e):
        # 1. Validar campos obligatorios
        campos_faltantes = []
        
        if not input_titulo.value or not input_titulo.value.strip():
            campos_faltantes.append("Título de la tarea")
        
        if not proyecto_seleccionado_obj[0]:
            campos_faltantes.append("Proyecto asignado")
        
        # Si hay campos faltantes, mostrar popup y salir
        if campos_faltantes:
            mostrar_dialog_campos_faltantes(campos_faltantes)
            return
        
        if date_picker_fin.value and date_picker_inicio.value and date_picker_fin.value < date_picker_inicio.value:
            mostrar_mensaje_dialog(page, "📅 Error en Fechas", "❌ La fecha de entrega no puede ser anterior a la fecha de inicio", "red")
            return

        # 2. Si no hay fecha límite, pedir confirmación
        if not date_picker_fin.value:
            mostrar_dialog_confirmar_sin_fecha()
            return
        
        # 3. Si todo está completo, crear la tarea directamente
        await ejecutar_creacion_tarea()

    # --- FUNCIONES DE LA INTERFAZ ---
    async def btn_volver_click(e):
        await page.push_route("/area_personal")

    def abrir_fecha_inicio(e):
        date_picker_inicio.open = True
        page.update()

    def abrir_fecha_fin(e):
        date_picker_fin.open = True
        page.update()

    def cambiar_emoji(e):
        if len(tags_seleccionados) > 1:
            emoji_index_actual[0] = (emoji_index_actual[0] + 1) % len(tags_seleccionados)
            tag_actual = tags_seleccionados[emoji_index_actual[0]]
            emoji_text.value = TAGS_EMOJIS[tag_actual]
            page.update()

    def actualizar_emoji():
        if len(tags_seleccionados) == 0:
            emoji_text.value = "📋"
            emoji_index_actual[0] = 0
        elif len(tags_seleccionados) == 1:
            emoji_text.value = TAGS_EMOJIS[tags_seleccionados[0]]
            emoji_index_actual[0] = 0
        else:
            emoji_index_actual[0] = 0
            emoji_text.value = TAGS_EMOJIS[tags_seleccionados[0]]

    # Dialog seleccionar proyecto
    def crear_dialog_proyecto():
        radio_proyecto = ft.RadioGroup(
            value=proyecto_seleccionado_obj[0].get("nombre") if proyecto_seleccionado_obj[0] else None,
            content=ft.Column(
                controls=[
                    ft.Radio(value=proy["nombre"], label=proy["nombre"], label_style=ft.TextStyle(size=12, color="black"), data=proy) 
                    for proy in proyectos_db
                ],
                spacing=2,
            ),
        )
        
        def cerrar_dialog(e):
            # MODIFICADO: validación para evitar error con None
            if not radio_proyecto.value:
                dialog_proyecto.open = False
                page.update()
                return
                
            # Buscamos el objeto proyecto que corresponde al nombre seleccionado
            nombre_sel = radio_proyecto.value
            for p in proyectos_db:
                if p["nombre"] == nombre_sel:
                    proyecto_seleccionado_obj[0] = p
                    break
            
            dialog_proyecto.open = False
            if proyecto_seleccionado_obj[0]:
                texto_proyecto_seleccionado.value = proyecto_seleccionado_obj[0]["nombre"]
                texto_proyecto_seleccionado.color = "black"
                
            # AÑADIDO: resetear departamento al cambiar de proyecto
            departamento_seleccionado_nombre[0] = None
            texto_departamento_seleccionado.value = "Selecciona departamento..."
            texto_departamento_seleccionado.color = "#999999"
            
            page.update()
        
        dialog_proyecto = ft.AlertDialog(
            modal=True,
            title=ft.Text("Seleccionar Proyecto", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=280,
                bgcolor="white",
                content=ft.ListView(
                    controls=[radio_proyecto] if proyectos_db else [ft.Text("No hay proyectos en la BD", color="red")],
                    spacing=5,
                ),
            ),
            actions=[
                ft.TextButton("Aceptar", on_click=cerrar_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return dialog_proyecto

    def abrir_dialog_proyecto(e):
        dialog = crear_dialog_proyecto()
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # Dialog seleccionar departamento - MODIFICADO: filtrado por proyecto
    def crear_dialog_departamento():
        # AÑADIDO: filtrar departamentos por proyecto seleccionado
        if not proyecto_seleccionado_obj[0]:
            mostrar_mensaje_dialog(page, "⚠️ Requisito Previo", "Selecciona un proyecto primero antes de elegir un departamento", "orange")
            return None
        
        proyecto_nombre = proyecto_seleccionado_obj[0].get("nombre")
        departamentos_filtrados = [
            dep for dep in departamentos_db 
            if dep.get("proyecto_asignado") == proyecto_nombre
        ]
        
        radio_departamento = ft.RadioGroup(
            value=departamento_seleccionado_nombre[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=dep["nombre"], label=dep["nombre"], label_style=ft.TextStyle(size=12, color="black")) 
                    for dep in departamentos_filtrados
                ],
                spacing=2,
            ),
        )
        
        def cerrar_dialog(e):
            # MODIFICADO: validación para evitar error con None
            if radio_departamento.value:
                departamento_seleccionado_nombre[0] = radio_departamento.value
                texto_departamento_seleccionado.value = departamento_seleccionado_nombre[0]
                texto_departamento_seleccionado.color = "black"
            dialog_departamento.open = False
            page.update()
        
        # MODIFICADO: mensaje cuando no hay departamentos vinculados
        contenido_lista = [radio_departamento] if departamentos_filtrados else [
            ft.Text("No hay departamentos vinculados a este proyecto", size=12, color="red")
        ]
        
        dialog_departamento = ft.AlertDialog(
            modal=True,
            title=ft.Text("Seleccionar Departamento", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=300,
                bgcolor="white",
                content=ft.ListView(
                    controls=contenido_lista,
                    spacing=5,
                ),
            ),
            actions=[
                ft.TextButton("Aceptar", on_click=cerrar_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return dialog_departamento

    def abrir_dialog_departamento(e):
        dialog = crear_dialog_departamento()
        if dialog:  # AÑADIDO: verificar que el diálogo se creó correctamente
            page.overlay.append(dialog)
            dialog.open = True
            page.update()

    # Dialog seleccionar personas (con checkbox) - MODIFICADO: usuario creador no puede deseleccionarse
    def crear_dialog_personas():
        checkboxes_personas = []
        
        # AÑADIDO: obtener ID del usuario creador para comparación
        id_usuario_creador = str(usuario_creador.get("_id")) if usuario_creador else ""
        
        def on_checkbox_change(e):
            persona = e.control.data
            if e.control.value:
                if persona not in personas_seleccionadas:
                    personas_seleccionadas.append(persona)
            else:
                if persona in personas_seleccionadas:
                    personas_seleccionadas.remove(persona)
        
        for persona in empleados_db:
            id_persona = str(persona.get("_id"))
            es_creador = id_persona == id_usuario_creador
            
            # MODIFICADO: añadir indicador "(Tú)" y deshabilitar checkbox del creador
            label_text = f"{persona.get('nombre')} {persona.get('apellidos', '')}"
            if es_creador:
                label_text += " (Tú)"
            
            # Verificar si está seleccionado comparando IDs como strings
            esta_seleccionado = any(
                str(s.get("_id")) == id_persona for s in personas_seleccionadas
            )
            
            cb = ft.Checkbox(
                label=label_text,
                value=esta_seleccionado,
                data=persona,
                on_change=on_checkbox_change,
                disabled=es_creador,  # AÑADIDO: creador no puede deseleccionarse
                label_style=ft.TextStyle(size=11, color="black"),
            )
            checkboxes_personas.append(cb)
        
        def cerrar_dialog(e):
            dialog_personas.open = False
            if len(personas_seleccionadas) == 0:
                texto_personas_seleccionadas.value = "Selecciona personas..."
                texto_personas_seleccionadas.color = "#999999"
            elif len(personas_seleccionadas) == 1:
                texto_personas_seleccionadas.value = personas_seleccionadas[0]["nombre"]
                texto_personas_seleccionadas.color = "black"
            else:
                # MODIFICADO: formato mejorado para múltiples selecciones
                texto_personas_seleccionadas.value = f"{personas_seleccionadas[0]['nombre']} (+{len(personas_seleccionadas)-1})"
                texto_personas_seleccionadas.color = "black"
            page.update()
        
        dialog_personas = ft.AlertDialog(
            modal=True,
            title=ft.Text("Asignar a", size=14, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=320,
                height=300,
                bgcolor="white",
                content=ft.ListView(
                    controls=checkboxes_personas if checkboxes_personas else [ft.Text("No hay trabajadores registrados", size=12, color="#999999")],
                    spacing=5,
                ),
            ),
            actions=[
                ft.TextButton("Aceptar", on_click=cerrar_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return dialog_personas

    def abrir_dialog_personas(e):
        dialog = crear_dialog_personas()
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # Dialog seleccionar tags
    def crear_dialog_tags():
        checkboxes_tags = []
        
        def on_checkbox_change(e):
            tag = e.control.data
            if e.control.value:
                if tag not in tags_seleccionados:
                    tags_seleccionados.append(tag)
            else:
                if tag in tags_seleccionados:
                    tags_seleccionados.remove(tag)
        
        for tag in TAGS_EMOJIS.keys():
            cb = ft.Checkbox(
                label=f"{TAGS_EMOJIS[tag]} {tag}",
                value=tag in tags_seleccionados,
                data=tag,
                on_change=on_checkbox_change,
                label_style=ft.TextStyle(size=12, color="black"),
            )
            checkboxes_tags.append(cb)
        
        def cerrar_dialog(e):
            dialog_tags.open = False
            if len(tags_seleccionados) == 0:
                texto_tags_seleccionados.value = "Selecciona..."
                texto_tags_seleccionados.color = "#999999"
            elif len(tags_seleccionados) == 1:
                texto_tags_seleccionados.value = tags_seleccionados[0]
                texto_tags_seleccionados.color = "black"
            else:
                texto_tags_seleccionados.value = f"{len(tags_seleccionados)} tags"
                texto_tags_seleccionados.color = "black"
            actualizar_emoji()
            page.update()
        
        dialog_tags = ft.AlertDialog(
            modal=True,
            title=ft.Text("Seleccionar Tags", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=350,
                bgcolor="white",
                content=ft.ListView(
                    controls=checkboxes_tags,
                    spacing=5,
                ),
            ),
            actions=[
                ft.TextButton("Aceptar", on_click=cerrar_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return dialog_tags

    def abrir_dialog_tags(e):
        dialog = crear_dialog_tags()
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # Selector de proyecto
    selector_proyecto = ft.Container(
        content=ft.Row(
            spacing=5,
            controls=[
                ft.Icon(ft.Icons.FOLDER_OUTLINED, size=16, color=COLOR_LABEL),
                texto_proyecto_seleccionado,
                ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=16, color=COLOR_LABEL),
            ],
        ),
        bgcolor="white",
        border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)),
        border_radius=5,
        padding=ft.Padding(left=10, right=5, top=8, bottom=8),
        on_click=abrir_dialog_proyecto,
        ink=True,
    )

    # Selector de departamento
    selector_departamento = ft.Container(
        content=ft.Row(
            spacing=5,
            controls=[
                ft.Icon(ft.Icons.BUSINESS_OUTLINED, size=16, color=COLOR_LABEL),
                texto_departamento_seleccionado,
                ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=16, color=COLOR_LABEL),
            ],
        ),
        bgcolor="white",
        border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)),
        border_radius=5,
        padding=ft.Padding(left=10, right=5, top=8, bottom=8),
        on_click=abrir_dialog_departamento,
        ink=True,
    )

    # Selector de personas
    selector_personas = ft.Container(
        content=ft.Row(
            spacing=5,
            controls=[
                ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=16, color=COLOR_LABEL),
                texto_personas_seleccionadas,
                ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=16, color=COLOR_LABEL),
            ],
        ),
        bgcolor="white",
        border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)),
        border_radius=5,
        padding=ft.Padding(left=10, right=5, top=8, bottom=8),
        expand=True,
        on_click=abrir_dialog_personas,
        ink=True,
    )

    # Selector de tags
    selector_tags = ft.Container(
        content=ft.Row(
            spacing=5,
            controls=[
                texto_tags_seleccionados,
                ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=16, color=COLOR_LABEL),
            ],
        ),
        bgcolor="white",
        border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)),
        border_radius=5,
        padding=ft.Padding(left=10, right=5, top=8, bottom=8),
        width=120,
        on_click=abrir_dialog_tags,
        ink=True,
    )

    # Dropdown prioridad
    dropdown_prioridad = ft.DropdownM2(
        value="Media",
        text_style=ft.TextStyle(size=11, color="black"),
        bgcolor="white",
        fill_color="white",
        border_color=COLOR_BORDE,
        border_radius=5,
        height=38,
        width=100,
        content_padding=ft.Padding(left=10, right=5),
        options=[
            ft.dropdownm2.Option("Alta"),
            ft.dropdownm2.Option("Media"),
            ft.dropdownm2.Option("Baja"),
        ],
        on_change=lambda e: prioridad_seleccionada.__setitem__(0, e.control.value),
    )

    input_titulo = ft.TextField(
        hint_text="Escribe el título de la tarea",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        height=38,
        content_padding=ft.Padding(left=10, right=10, top=8, bottom=8),
    )

    seccion_superior = ft.Container(
        bgcolor="white",
        border_radius=10,
        padding=12,
        border=ft.Border(top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=COLOR_SOMBRA_TARJETAS,
            offset=ft.Offset(0, 3),
        ),
        content=ft.Column(
            spacing=10,
            controls=[
                # Fila 1: Emoji + Título
                ft.Row(
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        emoji_container := ft.Container(
                            content=emoji_text,
                            padding=ft.Padding(top=12),
                            on_click=cambiar_emoji,
                            tooltip="Click para cambiar emoji",
                        ),
                        ft.Column(
                            spacing=3,
                            expand=True,
                            controls=[
                                ft.Row([
                                    ft.Text("Título", size=11, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                    ft.Text("*", size=11, color="#D32F2F", weight=ft.FontWeight.BOLD),
                                ], spacing=2),
                                input_titulo,
                            ]
                        ),
                    ]
                ),
                # Fila 2: Proyecto + Departamento
                ft.Row(
                    spacing=8,
                    controls=[
                        ft.Column(
                            spacing=3,
                            expand=True,
                            controls=[
                                ft.Row([
                                    ft.Text("Proyecto", size=11, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                    ft.Text("*", size=11, color="#D32F2F", weight=ft.FontWeight.BOLD),
                                ], spacing=2),
                                selector_proyecto,
                            ]
                        ),
                        ft.Column(
                            spacing=3,
                            expand=True,
                            controls=[
                                ft.Text("Departamento", size=11, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                selector_departamento,
                            ]
                        ),
                    ]
                ),
                # Fila 3: Asignar a
                ft.Column(
                    spacing=3,
                    controls=[
                        ft.Text("Asignar a", size=11, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                        selector_personas,
                    ]
                ),
                # Fila 4: Tags + Prioridad + Fechas
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.Column(
                            spacing=3,
                            controls=[
                                ft.Text("Tag(s)", size=11, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                selector_tags,
                            ]
                        ),
                        ft.Column(
                            spacing=3,
                            controls=[
                                ft.Text("Prioridad", size=11, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                dropdown_prioridad,
                            ]
                        ),
                        ft.Column(
                            spacing=4,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        spacing=5,
                                        controls=[
                                            ft.Text("Inicio:", size=11, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                            fecha_inicio_texto,
                                        ]
                                    ),
                                    on_click=abrir_fecha_inicio,
                                    ink=True,
                                    border_radius=5,
                                    padding=3,
                                ),
                                ft.Container(
                                    content=ft.Row(
                                        spacing=5,
                                        controls=[
                                            ft.Text("Fin:", size=11, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                            fecha_fin_texto,
                                        ]
                                    ),
                                    on_click=abrir_fecha_fin,
                                    ink=True,
                                    border_radius=5,
                                    padding=3,
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        )
    )

    texto_requerimientos = ft.TextField(
        hint_text="Escribe aquí los requerimientos...",
        hint_style=ft.TextStyle(size=12, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE,
        border_radius=5,
        multiline=True,
        min_lines=6,
        max_lines=6,
        expand=True,
        content_padding=10,
    )

    seccion_requerimientos = ft.Container(
        bgcolor="white",
        border_radius=10,
        padding=12,
        border=ft.Border(
            top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), 
            left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)
        ),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=COLOR_SOMBRA_TARJETAS,
            offset=ft.Offset(0, 3),
        ),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    "Requerimientos de la tarea",
                    size=12,
                    color="black",
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Row(
                    controls=[texto_requerimientos],
                ),
            ]
        )
    )

    btn_crear = ft.Container(
        width=160,
        height=44,
        bgcolor=COLOR_BTN_CREAR,
        border_radius=22,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_crear_click,
        content=ft.Text("Crear Tarea", color="white", weight=ft.FontWeight.BOLD, size=14),
    )

    # Leyenda de campos obligatorios
    leyenda_obligatorios = ft.Container(
        content=ft.Row([
            ft.Text("*", size=11, color="#D32F2F", weight=ft.FontWeight.BOLD),
            ft.Text("Campos obligatorios", size=10, color="#666666", italic=True),
        ], spacing=3),
        alignment=ft.Alignment(-1, 0),
    )

    fila_boton = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[btn_crear]
    )

    tarjeta_blanca = ft.Container(
        width=400,
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=COLOR_SOMBRA),
        content=ft.Column(
            spacing=0,
            tight=True,
            controls=[
                ft.Container(
                    padding=ft.Padding(left=15, top=10, bottom=5),
                    alignment=ft.Alignment(-1, 0),
                    content=ft.Container(
                        content=ft.Text("←", size=26, color="black", weight="bold"),
                        on_click=btn_volver_click,
                        ink=True,
                        border_radius=50,
                        padding=3,
                    ),
                ),

                ft.Container(
                    height=55,
                    width=400,
                    bgcolor=COLOR_HEADER_BG,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("NUEVA TAREA", size=18, weight=ft.FontWeight.BOLD, color="white")
                ),
                
                ft.Container(
                    padding=ft.Padding(left=18, right=18, top=15, bottom=20),
                    content=ft.Column(
                        spacing=12,
                        tight=True,
                        controls=[
                            seccion_superior,
                            seccion_requerimientos,
                            leyenda_obligatorios,
                            fila_boton,
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