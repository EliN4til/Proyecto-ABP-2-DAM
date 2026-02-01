import flet as ft
from modelos.crud import obtener_todos_proyectos, obtener_tareas_por_usuario
from servicios.sesion_service import obtener_id_usuario, obtener_usuario
from datetime import datetime

def VistaMisProyectos(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_SOMBRA_TARJETAS = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_BADGE_DEP = "#E3F2FD"
    COLOR_TEXT_DEP = "#1565C0"
    
    #colores para estados de tareas
    COLOR_PENDIENTE = "#FF9800"
    COLOR_REALIZADA = "#4CAF50"
    COLOR_ATRASADA = "#E53935"

    #opciones de filtro
    FILTROS_ESTADO = ["Todos", "ACTIVO", "PAUSADO", "Finalizado"]
    FILTROS_ORDEN = ["Nombre A-Z", "Nombre Z-A"]

    filtro_estado_actual = ["Todos"]
    filtro_orden_actual = ["Nombre A-Z"]

    #variable para almacenar los proyectos procesados de la BD
    proyectos_procesados = []

    #LÓGICA DE CARGA DE DATOS REALES (FILTRADO POR USUARIO)

    def cargar_proyectos_reales():
        """
        Consulta la BD para traer SOLO los proyectos donde el usuario
        actual es responsable o tiene tareas asignadas.
        """
        nonlocal proyectos_procesados
        
        id_usuario = obtener_id_usuario()
        usuario_actual = obtener_usuario()
        
        if not id_usuario or not usuario_actual:
            return []

        #obtiene TODOS los proyectos para filtrar después
        exito_p, lista_proyectos_total = obtener_todos_proyectos()
        #obtiene TODAS las tareas asignadas específicamente a este usuario
        exito_t, lista_tareas_user = obtener_tareas_por_usuario(id_usuario)

        if not exito_p:
            return []

        #crea un set con los IDs de proyectos donde el usuario tiene tareas
        ids_proyectos_con_tareas = set()
        if exito_t:
            for t in lista_tareas_user:
                id_p = t.get("id_proyecto")
                if id_p:
                    ids_proyectos_con_tareas.add(str(id_p))

        proyectos_del_usuario = []
        ahora = datetime.now()

        #filtra la lista global de proyectos
        for p in lista_proyectos_total:
            id_p_str = str(p.get("_id"))
            nombre_responsable = p.get("responsable", "")
            
            # CRITERIO: El usuario lo ve si es el responsable O si tiene tareas en él
            es_responsable = (nombre_responsable == usuario_actual.get("nombre"))
            tiene_tareas = (id_p_str in ids_proyectos_con_tareas)

            if es_responsable or tiene_tareas:
                #si cumple, procesamos sus tareas para el desglose interno
                pendientes_count = 0
                tareas_para_ui = []
                
                # Filtramos tareas de este usuario que pertenecen a ESTE proyecto
                tareas_mi_proyecto = [t for t in lista_tareas_user if str(t.get("id_proyecto")) == id_p_str]
                
                for t in tareas_mi_proyecto:
                    est = t.get("estado", "pendiente")
                    ui_est = "Pendiente"
                    if est == "completada":
                        ui_est = "Realizada"
                    elif t.get("fecha_limite") and t.get("fecha_limite") < ahora:
                        ui_est = "Atrasada"
                    
                    if ui_est != "Realizada":
                        pendientes_count += 1
                    
                    tareas_para_ui.append({
                        "titulo": t.get("titulo", "Sin título"),
                        "estado": ui_est,
                        "prioridad": t.get("prioridad", "media").capitalize()
                    })

                #creamos el objeto para la interfaz
                proyectos_del_usuario.append({
                    "id": id_p_str,
                    "nombre": p.get("nombre", "Sin nombre"),
                    "descripcion": p.get("cliente", "Proyecto corporativo"),
                    "mis_departamentos": [usuario_actual.get("departamento", {}).get("nombre", "General")],
                    "rol": "Responsable" if es_responsable else "Colaborador",
                    "estado": p.get("estado", "ACTIVO"),
                    "tareas_pendientes": pendientes_count,
                    "equipo": [nombre_responsable] if nombre_responsable else ["Admin"],
                    "fecha_inicio": p.get("fecha_inicio").strftime("%d/%m/%y") if p.get("fecha_inicio") else "N/A",
                    "fecha_fin": p.get("fecha_fin").strftime("%d/%m/%y") if p.get("fecha_fin") else "N/A",
                    "emoji": "📁",
                    "lista_tareas": tareas_para_ui
                })
        
        proyectos_procesados = proyectos_del_usuario
        return proyectos_del_usuario

    def actualizar_lista_ui():
        """Aplica filtros de búsqueda y estado sobre la lista en memoria"""
        texto = input_busqueda.value.lower() if input_busqueda.value else ""
        
        filtrados = []
        for p in proyectos_procesados:
            # Filtro texto
            if texto and texto not in p["nombre"].lower():
                continue
            # Filtro estado (ACTIVO, PAUSADO...)
            if filtro_estado_actual[0] != "Todos" and p["estado"] != filtro_estado_actual[0]:
                continue
            filtrados.append(p)

        # Ordenación
        if filtro_orden_actual[0] == "Nombre A-Z":
            filtrados.sort(key=lambda x: x["nombre"])
        else:
            filtrados.sort(key=lambda x: x["nombre"], reverse=True)

        lista_proyectos.controls = []
        if not filtrados:
            lista_proyectos.controls.append(
                ft.Container(
                    padding=40,
                    content=ft.Text("No tienes proyectos asignados actualmente.", color="grey", text_align="center")
                )
            )
        else:
            for p in filtrados:
                lista_proyectos.controls.append(crear_tarjeta_proyecto(p))
        page.update()

    #EVENTOS

    def btn_volver_click(e):
        page.go("/area_personal")

    def btn_buscar_click(e):
        actualizar_lista_ui()
        page.snack_bar = ft.SnackBar(ft.Text(f"Buscando: {input_busqueda.value}"))
        page.snack_bar.open = True
        page.update()

    #diálogo para ver las tareas específicas del proyecto
    def mostrar_tareas_del_proyecto(proyecto):
        
        def get_icon_color(estado):
            if estado == "Realizada": return COLOR_REALIZADA
            if estado == "Atrasada": return COLOR_ATRASADA
            return COLOR_PENDIENTE

        def get_icon(estado):
            if estado == "Realizada": return ft.Icons.CHECK_CIRCLE
            if estado == "Atrasada": return ft.Icons.WARNING_AMBER
            return ft.Icons.ACCESS_TIME_FILLED

        items_tareas = []
        if not proyecto["lista_tareas"]:
            items_tareas.append(ft.Container(padding=20, content=ft.Text("No tienes tareas individuales asignadas.", size=12, color="grey")))
        else:
            for tarea in proyecto["lista_tareas"]:
                item = ft.Container(
                    padding=10,
                    border=ft.border.only(bottom=ft.border.BorderSide(1, "#F0F0F0")),
                    content=ft.Row(
                        controls=[
                            ft.Icon(get_icon(tarea["estado"]), size=18, color=get_icon_color(tarea["estado"])),
                            ft.Column(
                                spacing=2,
                                expand=True,
                                controls=[
                                    ft.Text(tarea["titulo"], size=12, weight=ft.FontWeight.W_500, color="black"),
                                    ft.Text(f"Estado: {tarea['estado']} • Prioridad: {tarea['prioridad']}", size=10, color="grey"),
                                ]
                            )
                        ]
                    )
                )
                items_tareas.append(item)

        dialog_tareas = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Mis tareas en {proyecto['nombre']}", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=350,
                height=400,
                bgcolor="white",
                content=ft.ListView(
                    controls=items_tareas,
                    spacing=0,
                )
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog_tareas(dialog_tareas)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        def cerrar_dialog_tareas(dlg):
            dlg.open = False
            page.update()

        page.overlay.append(dialog_tareas)
        dialog_tareas.open = True
        page.update()

    #dialog detalle proyecto
    def mostrar_detalle_proyecto(proyecto):
        
        avatares_equipo = ft.Row(
            spacing=-10, 
            controls=[
                ft.Container(
                    width=30, height=30, bgcolor="#BBDEFB", border_radius=15,
                    border=ft.border.all(2, "white"),
                    alignment=ft.Alignment(0,0),
                    content=ft.Text(miembro[0], size=12, color="black", weight="bold"),
                    tooltip=miembro
                ) for miembro in proyecto["equipo"]
            ]
        )

        mis_deptos_chips = ft.Row(
            wrap=True,
            spacing=5,
            run_spacing=5,
            controls=[
                ft.Container(
                    bgcolor=COLOR_BADGE_DEP,
                    border_radius=15,
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                    content=ft.Text(dep, size=10, color=COLOR_TEXT_DEP, weight=ft.FontWeight.W_500),
                ) for dep in proyecto["mis_departamentos"]
            ]
        )

        def abrir_tareas_desde_detalle(e):
            mostrar_tareas_del_proyecto(proyecto)

        def cerrar_dialog(dialog):
            dialog.open = False
            page.update()

        dialog_detalle = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Text(proyecto["emoji"], size=28),
                    ft.Text(proyecto["nombre"], size=16, weight=ft.FontWeight.BOLD, color="black", expand=True),
                ],
                spacing=10,
            ),
            bgcolor="white",
            content=ft.Container(
                width=320,
                bgcolor="white",
                content=ft.Column(
                    spacing=15,
                    tight=True,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        #estado y fechas
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Container(
                                    bgcolor="#E8F5E9" if proyecto["estado"] == "ACTIVO" else "#FFF3E0",
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                    border_radius=8,
                                    content=ft.Text(proyecto["estado"], size=10, color="black", weight="bold")
                                ),
                                ft.Text(f"{proyecto['fecha_inicio']} - {proyecto['fecha_fin']}", size=10, color="#666666")
                            ]
                        ),
                        #descripcion
                        ft.Text(proyecto["descripcion"], size=12, color="black"),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        
                        #seccion mi rol
                        ft.Text("Mi participación:", size=11, color=COLOR_LABEL, weight="bold"),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(spacing=2, controls=[
                                    ft.Text("Rol", size=10, color="#666666"),
                                    ft.Text(proyecto["rol"], size=11, color="black", weight="bold"),
                                ]),
                                ft.Column(spacing=2, controls=[
                                    ft.Text("Departamentos", size=10, color="#666666"),
                                    mis_deptos_chips,
                                ]),
                            ]
                        ),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        
                        #seccion equipo
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Responsable:", size=11, color=COLOR_LABEL, weight="bold"),
                                avatares_equipo
                            ]
                        ),
                    ]
                ),
            ),
            actions=[
                ft.TextButton("Ver mis tareas", on_click=abrir_tareas_desde_detalle),
                ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog(dialog_detalle)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_detalle)
        dialog_detalle.open = True
        page.update()

    # Diálogo de filtros
    def mostrar_dialog_filtros(e):
        radio_orden = ft.RadioGroup(
            value=filtro_orden_actual[0],
            content=ft.Column([ft.Radio(value=o, label=o, label_style=ft.TextStyle(size=11, color="black")) for o in FILTROS_ORDEN])
        )
        radio_estado = ft.RadioGroup(
            value=filtro_estado_actual[0],
            content=ft.Column([ft.Radio(value=est, label=est, label_style=ft.TextStyle(size=11, color="black")) for est in FILTROS_ESTADO])
        )

        def aplicar_filtros(e):
            filtro_orden_actual[0] = radio_orden.value
            filtro_estado_actual[0] = radio_estado.value
            dialog_filtros.open = False
            actualizar_lista_ui()

        dialog_filtros = ft.AlertDialog(
            modal=True,
            title=ft.Text("Filtrar proyectos", size=16, weight=ft.FontWeight.BOLD, color="black"),
            content=ft.Container(
                width=300, height=350,
                content=ft.Column([
                    ft.Text("Estado:", size=12, weight="bold", color=COLOR_LABEL), radio_estado,
                    ft.Divider(),
                    ft.Text("Orden:", size=12, weight="bold", color=COLOR_LABEL), radio_orden,
                ], scroll="auto")
            ),
            actions=[ft.TextButton("Aplicar", on_click=aplicar_filtros)],
        )

        page.overlay.append(dialog_filtros)
        dialog_filtros.open = True
        page.update()

    def crear_tarjeta_proyecto(proyecto):
        """Crea una tarjeta visual para cada proyecto real del usuario"""
        
        chips_deptos = ft.Row(
            wrap=True, spacing=4,
            controls=[
                ft.Container(
                    bgcolor=COLOR_BADGE_DEP, border_radius=10,
                    padding=ft.padding.symmetric(horizontal=6, vertical=2),
                    content=ft.Text(dep, size=9, color=COLOR_TEXT_DEP, weight=ft.FontWeight.BOLD),
                ) for dep in proyecto["mis_departamentos"]
            ]
        )

        return ft.Container(
            bgcolor="white", border_radius=12, padding=12, margin=ft.margin.only(bottom=10),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color=COLOR_SOMBRA_TARJETAS, offset=ft.Offset(0, 2)),
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Row(
                        spacing=10,
                        vertical_alignment="center",
                        controls=[
                            ft.Container(width=40, height=40, bgcolor="#F5F5F5", border_radius=8, alignment=ft.Alignment(0,0), content=ft.Text(proyecto["emoji"], size=20)),
                            ft.Column(
                                spacing=0, expand=True,
                                controls=[
                                    ft.Text(proyecto["nombre"], size=13, weight="bold", color="black"),
                                    ft.Text(proyecto["rol"], size=10, color="#666666"),
                                ]
                            ),
                            ft.Container(width=10, height=10, border_radius=5, bgcolor="#4CAF50" if proyecto["estado"] == "ACTIVO" else "#FFC107")
                        ]
                    ),
                    ft.Divider(height=1, color="#F0F0F0"),
                    ft.Column([ft.Text("Departamento:", size=9, color=COLOR_LABEL, weight="bold"), chips_deptos]),
                    ft.Row(
                        alignment="end",
                        controls=[
                            ft.Container(
                                padding=ft.padding.symmetric(horizontal=8, vertical=4), bgcolor="#F5F5F8", border_radius=12,
                                content=ft.Row([
                                    ft.Icon(ft.Icons.LIST_ALT, size=12, color=COLOR_LABEL),
                                    ft.Text(f"{proyecto['tareas_pendientes']} pendientes", size=10, color=COLOR_LABEL, weight="bold"),
                                ])
                            )
                        ]
                    )
                ]
            ),
            on_click=lambda e, p=proyecto: mostrar_detalle_proyecto(p),
            ink=True,
        )

    # --- ELEMENTOS DE PÁGINA ---

    input_busqueda = ft.TextField(
        hint_text="Buscar mis proyectos...",
        hint_style=ft.TextStyle(size=11, color="#999999"),
        text_style=ft.TextStyle(size=12, color="black"),
        border_color=COLOR_BORDE, border_radius=5, height=38, expand=True,
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

    lista_proyectos = ft.ListView(spacing=0, expand=True, padding=ft.padding.only(bottom=20))

    tarjeta_blanca = ft.Container(
        width=400, height=720, bgcolor="white", border_radius=25,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=COLOR_SOMBRA),
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Container(padding=ft.padding.only(left=15, top=10, bottom=5), content=ft.Container(content=ft.Text("←", size=26, color="black", weight="bold"), on_click=btn_volver_click, ink=True, border_radius=50, padding=3)),
                ft.Container(height=55, width=400, bgcolor=COLOR_HEADER_BG, alignment=ft.Alignment(0, 0), content=ft.Text("MIS PROYECTOS", size=18, weight="bold", color="white")),
                ft.Container(
                    padding=18, expand=True,
                    content=ft.Column(spacing=12, expand=True, controls=[ft.Row([input_busqueda, btn_filtrar, btn_buscar]), lista_proyectos])
                )
            ]
        )
    )

    #INICIALIZACIÓN
    proyectos_procesados = cargar_proyectos_reales()
    actualizar_lista_ui()

    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[COLOR_FONDO_TOP, COLOR_FONDO_BOT]),
        alignment=ft.Alignment(0, 0), 
        content=tarjeta_blanca
    )

def main(page: ft.Page):
    page.title = "App Tareas - Mis Proyectos"
    page.window.width = 400
    page.window.height = 800
    page.padding = 0 
    vista = VistaMisProyectos(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)