import flet as ft
from modelos.crud import obtener_tareas_por_estado
from modelos.consultas import filtrar_y_ordenar

def VistaTareasRealizadas(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_SOMBRA_TARJETAS = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_COMPLETADO = "#4CAF50"
    COLOR_PRIORIDAD_ALTA = "#E53935"
    COLOR_PRIORIDAD_MEDIA = "#FF9800"
    COLOR_PRIORIDAD_BAJA = "#4CAF50"

    #opciones de filtro
    FILTROS_TAGS = ["Todos", "Desarrollo", "Bug Fix", "Testing", "Diseño", "Documentación", "DevOps", "Base de Datos", "API", "Frontend", "Backend"]
    FILTROS_PROYECTO = ["Todos"]
    FILTROS_PRIORIDAD = ["Todas", "Alta", "Media", "Baja"]
    FILTROS_ORDEN = [
        "Más reciente primero", 
        "Más antiguo primero", 
        "Fecha ascendente",
        "Fecha descendente",
        "Alfabético A-Z", 
        "Alfabético Z-A",
        "Por proyecto",
    ]

    filtro_tag_actual = ["Todos"]
    filtro_proyecto_actual = ["Todos"]
    filtro_prioridad_actual = ["Todas"]
    filtro_orden_actual = ["Más reciente primero"]

    #cargamos las tareas completadas de la BD
    def cargar_tareas_completadas():
        """Obtiene las tareas completadas de la base de datos"""
        exito, resultado = obtener_tareas_por_estado("completada")
        if exito:
            tareas = []
            for t in resultado:
                #formateamos la fecha de completado
                fecha_completado = ""
                if t.get("fecha_completado"):
                    fecha_completado = t["fecha_completado"].strftime("%d/%m/%y")
                elif t.get("fecha_limite"):
                    fecha_completado = t["fecha_limite"].strftime("%d/%m/%y")
                
                #obtenemos los nombres de los asignados
                asignados_nombres = []
                for asignado in t.get("asignados", []):
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
                    "emoji": t.get("icono", "📋"),
                    "proyecto": t.get("proyecto", "Sin proyecto"),
                    "departamento": "General",
                    "prioridad": t.get("prioridad", "Media"),
                    "asignados": asignados_nombres,
                    "fecha_completado": fecha_completado,
                    "requerimientos": [t.get("requisitos", "Sin requisitos")]
                }
                tareas.append(tarea)
            return tareas
        else:
            #si hay error, devolvemos lista vacía
            print(f"Error cargando tareas: {resultado}")
            return []
    
    #cargamos las tareas al inicio
    TAREAS_REALIZADAS = cargar_tareas_completadas()
    #guardamos todas las tareas para poder filtrar
    todas_las_tareas = []
    for t in TAREAS_REALIZADAS:
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
            "fecha_completado"
        )
        
        #actualizamos la lista
        lista_tareas.controls = []
        for tarea in tareas_filtradas:
            tarjeta = crear_tarjeta_tarea(tarea)
            lista_tareas.controls.append(tarjeta)
        page.update()

    def get_color_prioridad(prioridad):
        if prioridad == "Alta":
            return COLOR_PRIORIDAD_ALTA
        elif prioridad == "Media":
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
                        #completado
                        ft.Container(
                            bgcolor="#E8F5E9",
                            border_radius=8,
                            padding=ft.padding.all(8),
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("✅ Completado:", size=11, color=COLOR_COMPLETADO, weight=ft.FontWeight.BOLD),
                                    ft.Text(tarea["fecha_completado"], size=11, color=COLOR_COMPLETADO),
                                ]
                            ),
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
                            ft.Text("Realizado por", size=10, color=COLOR_LABEL),
                            ft.Text(asignados_text, size=11, color="black"),
                        ]),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        #requerimientos
                        ft.Text("Requerimientos:", size=12, color="black", weight=ft.FontWeight.BOLD),
                        ft.Container(
                            height=120,
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
            actualizar_lista_tareas()
            page.snack_bar = ft.SnackBar(ft.Text("✅ Filtros aplicados"))
            page.snack_bar.open = True
            page.update()

        def limpiar_filtros(e):
            radio_orden.value = "Más reciente primero"
            radio_prioridad.value = "Todas"
            filtro_orden_actual[0] = "Más reciente primero"
            filtro_prioridad_actual[0] = "Todas"
            filtro_tag_actual[0] = "Todos"
            filtro_proyecto_actual[0] = "Todos"
            input_busqueda.value = ""
            actualizar_lista_tareas()
            page.update()

        def abrir_filtro_tags(e):
            dialog_filtros.open = False
            page.update()
            mostrar_dialog_tags()

        def abrir_filtro_proyecto(e):
            dialog_filtros.open = False
            page.update()
            mostrar_dialog_proyecto()

        dialog_filtros = ft.AlertDialog(
            modal=True,
            title=ft.Text("Filtrar tareas", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=400,
                bgcolor="white",
                content=ft.Column(
                    spacing=8,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("Por Prioridad:", size=12, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                        radio_prioridad,
                        ft.Divider(height=8, color=COLOR_BORDE),
                        ft.Text("Ordenar por:", size=12, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                        radio_orden,
                        ft.Divider(height=8, color=COLOR_BORDE),
                        ft.Container(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Filtrar por Tag", size=12, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                                    ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=14, color=COLOR_LABEL),
                                ]
                            ),
                            on_click=abrir_filtro_tags,
                            ink=True,
                            padding=ft.padding.all(8),
                            border_radius=5,
                            bgcolor="#F5F5F5",
                        ),
                        ft.Container(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Filtrar por Proyecto", size=12, weight=ft.FontWeight.BOLD, color=COLOR_LABEL),
                                    ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=14, color=COLOR_LABEL),
                                ]
                            ),
                            on_click=abrir_filtro_proyecto,
                            ink=True,
                            padding=ft.padding.all(8),
                            border_radius=5,
                            bgcolor="#F5F5F5",
                        ),
                    ],
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

    #dialog filtro por tags
    def mostrar_dialog_tags():
        radio_tags = ft.RadioGroup(
            value=filtro_tag_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=tag, label=tag, label_style=ft.TextStyle(size=11, color="black")) 
                    for tag in FILTROS_TAGS
                ],
                spacing=2,
            ),
        )

        def aplicar_tag(e):
            filtro_tag_actual[0] = radio_tags.value
            dialog_tags.open = False
            actualizar_lista_tareas()
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ Tag: {filtro_tag_actual[0]}"))
            page.snack_bar.open = True
            page.update()

        def volver_filtros(e):
            dialog_tags.open = False
            page.update()
            mostrar_dialog_filtros(None)

        dialog_tags = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text("←", size=18, color="black", weight="bold"),
                        on_click=volver_filtros,
                        ink=True,
                        border_radius=50,
                        padding=5,
                    ),
                    ft.Text("Seleccionar Tag", size=14, weight=ft.FontWeight.BOLD, color="black"),
                ],
                spacing=10,
            ),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=350,
                bgcolor="white",
                content=ft.ListView(
                    controls=[radio_tags],
                    spacing=5,
                ),
            ),
            actions=[
                ft.TextButton("Aplicar", on_click=aplicar_tag),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_tags)
        dialog_tags.open = True
        page.update()

    #dialog filtro por proyecto
    def mostrar_dialog_proyecto():
        radio_proyecto = ft.RadioGroup(
            value=filtro_proyecto_actual[0],
            content=ft.Column(
                controls=[
                    ft.Radio(value=proy, label=proy, label_style=ft.TextStyle(size=11, color="black")) 
                    for proy in FILTROS_PROYECTO
                ],
                spacing=2,
            ),
        )

        def aplicar_proyecto(e):
            filtro_proyecto_actual[0] = radio_proyecto.value
            dialog_proyecto.open = False
            actualizar_lista_tareas()
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ Proyecto: {filtro_proyecto_actual[0]}"))
            page.snack_bar.open = True
            page.update()

        def volver_filtros(e):
            dialog_proyecto.open = False
            page.update()
            mostrar_dialog_filtros(None)

        dialog_proyecto = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text("←", size=18, color="black", weight="bold"),
                        on_click=volver_filtros,
                        ink=True,
                        border_radius=50,
                        padding=5,
                    ),
                    ft.Text("Seleccionar Proyecto", size=14, weight=ft.FontWeight.BOLD, color="black"),
                ],
                spacing=10,
            ),
            bgcolor="white",
            content=ft.Container(
                width=300,
                height=300,
                bgcolor="white",
                content=ft.ListView(
                    controls=[radio_proyecto],
                    spacing=5,
                ),
            ),
            actions=[
                ft.TextButton("Aplicar", on_click=aplicar_proyecto),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog_proyecto)
        dialog_proyecto.open = True
        page.update()

    def crear_tarjeta_tarea(tarea):
        """Crea una tarjeta para cada tarea realizada"""
        return ft.Container(
            bgcolor="white",
            border_radius=10,
            padding=ft.padding.all(10),
            margin=ft.margin.only(bottom=8),
            border=ft.border.all(1, "#C8E6C9"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=5,
                color=COLOR_SOMBRA_TARJETAS,
                offset=ft.Offset(0, 2),
            ),
            content=ft.Column(
                spacing=4,
                controls=[
                    #fila 1: Emoji + Título + Check
                    ft.Row(
                        spacing=8,
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
                            ft.Icon(ft.Icons.CHECK_CIRCLE, size=20, color=COLOR_COMPLETADO),
                        ]
                    ),
                    #fila 2: Proyecto + Tag
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(tarea["proyecto"], size=10, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                            ft.Row(
                                spacing=3,
                                controls=[
                                    ft.Text("TAG:", size=9, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                    ft.Text(tarea["tag"], size=9, color="black", weight=ft.FontWeight.W_500),
                                ]
                            ),
                        ]
                    ),
                    #fila 3: Fecha completado + Prioridad
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                f"✅ Completado: {tarea['fecha_completado']}",
                                size=10,
                                color=COLOR_COMPLETADO,
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Container(
                                bgcolor=get_color_prioridad(tarea["prioridad"]),
                                border_radius=8,
                                padding=ft.padding.only(left=6, right=6, top=1, bottom=1),
                                content=ft.Text(tarea["prioridad"], size=9, color="white", weight=ft.FontWeight.BOLD),
                            ),
                        ]
                    ),
                ]
            ),
            on_click=lambda e, t=tarea: mostrar_detalle_tarea(t),
            ink=True,
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
        controls=[crear_tarjeta_tarea(tarea) for tarea in TAREAS_REALIZADAS],
        expand=True,
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
                    content=ft.Text("TAREAS REALIZADAS", size=18, weight=ft.FontWeight.BOLD, color="white")
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


def main(page: ft.Page):
    page.title = "App Tareas - Tareas Realizadas"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 380
    page.window.min_height = 780
    page.padding = 0 
    
    vista = VistaTareasRealizadas(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)