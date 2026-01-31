import flet as ft

def VistaCompartidoConmigo(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_SOMBRA_TARJETAS = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_ATRASADO = "#E53935"
    COLOR_PRIORIDAD_ALTA = "#E53935"
    COLOR_PRIORIDAD_MEDIA = "#FF9800"
    COLOR_PRIORIDAD_BAJA = "#4CAF50"

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

    #datos demo de tareas compartidas conmigo
    TAREAS_COMPARTIDAS = [
        {
            "titulo": "Arreglar bug linea 287 fichero UpdateDate.py",
            "tag": "Desarrollo",
            "emoji": "👨‍💻",
            "proyecto": "App Móvil v2.0",
            "departamento": "Desarrollo",
            "prioridad": "Alta",
            "compartido_por": "Ana García",
            "fecha": "25/12/25",
            "atrasado": True,
            "requerimientos": [
                "Identificar el error en la línea 287 del fichero UpdateDate.py",
                "El bucle debe iterar correctamente sobre la lista de fechas",
                "Validar que no se produzcan excepciones de tipo IndexError",
                "Añadir logs para seguimiento del proceso",
                "Realizar pruebas con datos de producción simulados",
            ]
        },
        {
            "titulo": "Diseñar mockups para dashboard",
            "tag": "Diseño",
            "emoji": "🎨",
            "proyecto": "Dashboard Analytics",
            "departamento": "Diseño",
            "prioridad": "Media",
            "compartido_por": "Carlos López",
            "fecha": "28/12/25",
            "atrasado": True,
            "requerimientos": [
                "Crear diseño responsive para desktop y móvil",
                "Incluir gráficos de rendimiento y métricas KPI",
                "Usar la paleta de colores corporativa",
                "Diseñar estados vacíos y de error",
                "Exportar en formato Figma y PNG",
            ]
        },
        {
            "titulo": "Escribir tests unitarios módulo Auth",
            "tag": "Testing",
            "emoji": "🧪",
            "proyecto": "API REST Services",
            "departamento": "QA",
            "prioridad": "Media",
            "compartido_por": "María Rodríguez",
            "fecha": "30/12/25",
            "atrasado": False,
            "requerimientos": [
                "Cobertura mínima del 80% en el módulo de autenticación",
                "Testear login, logout y refresh de tokens",
                "Incluir tests para casos de error y edge cases",
                "Mockear las llamadas a servicios externos",
                "Documentar los tests con descripciones claras",
            ]
        },
        {
            "titulo": "Documentar API endpoints v2",
            "tag": "Documentación",
            "emoji": "📝",
            "proyecto": "API REST Services",
            "departamento": "Desarrollo",
            "prioridad": "Baja",
            "compartido_por": "Sofia Ruiz",
            "fecha": "02/01/26",
            "atrasado": False,
            "requerimientos": [
                "Documentar todos los endpoints del API v2 en Swagger",
                "Incluir ejemplos de request y response",
                "Describir códigos de error y sus significados",
                "Añadir sección de autenticación y autorización",
                "Revisar y actualizar la documentación existente",
            ]
        },
        {
            "titulo": "Configurar pipeline CI/CD",
            "tag": "DevOps",
            "emoji": "⚙️",
            "proyecto": "Migración Cloud",
            "departamento": "DevOps",
            "prioridad": "Alta",
            "compartido_por": "Pedro Martínez",
            "fecha": "05/01/26",
            "atrasado": False,
            "requerimientos": [
                "Configurar GitHub Actions para build automático",
                "Añadir etapa de tests automatizados",
                "Configurar deploy automático a staging",
                "Implementar notificaciones en Slack",
                "Documentar el proceso de deployment",
            ]
        },
        {
            "titulo": "Optimizar consultas SQL reportes",
            "tag": "Base de Datos",
            "emoji": "🗄️",
            "proyecto": "Sistema de Pagos",
            "departamento": "Desarrollo",
            "prioridad": "Alta",
            "compartido_por": "Diego Torres",
            "fecha": "08/01/26",
            "atrasado": False,
            "requerimientos": [
                "Analizar consultas lentas con EXPLAIN",
                "Crear índices necesarios para mejorar rendimiento",
                "Optimizar JOINs en las consultas de reportes",
                "Reducir tiempo de respuesta a menos de 2 segundos",
                "Documentar cambios realizados en la base de datos",
            ]
        },
    ]

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
        texto_busqueda = input_busqueda.value
        page.snack_bar = ft.SnackBar(ft.Text(f"Buscando: {texto_busqueda}"))
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
                        #aviso atrasado (si aplica)
                        ft.Container(
                            visible=tarea["atrasado"],
                            bgcolor="#FFF3F3",
                            border_radius=8,
                            padding=ft.padding.all(8),
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("⚠️ Atrasado", size=11, color=COLOR_ATRASADO, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Vencía: {tarea['fecha']}", size=11, color=COLOR_ATRASADO),
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
                        #compartido por
                        ft.Column(spacing=2, controls=[
                            ft.Text("Compartido por", size=10, color=COLOR_LABEL),
                            ft.Row(
                                spacing=5,
                                controls=[
                                    ft.Icon(ft.Icons.PERSON, size=14, color=COLOR_LABEL),
                                    ft.Text(tarea["compartido_por"], size=11, color="black", weight=ft.FontWeight.BOLD),
                                ]
                            ),
                        ]),
                        #fechas (si no esta atrasado)
                        ft.Row(
                            visible=not tarea["atrasado"],
                            spacing=3,
                            controls=[
                                ft.Text("Fecha límite:", size=10, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                ft.Text(tarea["fecha"], size=10, color="black", weight=ft.FontWeight.W_500),
                            ]
                        ),
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
            page.snack_bar = ft.SnackBar(ft.Text("Filtros aplicados"))
            page.snack_bar.open = True
            page.update()

        def limpiar_filtros(e):
            radio_orden.value = "Más reciente primero"
            radio_prioridad.value = "Todas"
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
                height=420,
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
            page.snack_bar = ft.SnackBar(ft.Text(f"Tag: {filtro_tag_actual[0]}"))
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
            page.snack_bar = ft.SnackBar(ft.Text(f"Proyecto: {filtro_proyecto_actual[0]}"))
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
        """Crea una tarjeta para cada tarea compartida"""
        return ft.Container(
            bgcolor="white",
            border_radius=10,
            padding=ft.padding.all(10),
            margin=ft.margin.only(bottom=8),
            border=ft.border.all(1, "#FFCDD2") if tarea["atrasado"] else None,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=5,
                color=COLOR_SOMBRA_TARJETAS,
                offset=ft.Offset(0, 2),
            ),
            content=ft.Column(
                spacing=4,
                controls=[
                    #fila 1: Emoji + Título + Prioridad
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
                            ft.Container(
                                bgcolor=get_color_prioridad(tarea["prioridad"]),
                                border_radius=8,
                                padding=ft.padding.only(left=6, right=6, top=1, bottom=1),
                                content=ft.Text(tarea["prioridad"], size=9, color="white", weight=ft.FontWeight.BOLD),
                            ),
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
                    #fila 3: Compartido por + Fecha/Estado
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=4,
                                controls=[
                                    ft.Icon(ft.Icons.PERSON, size=12, color=COLOR_LABEL),
                                    ft.Text(f"{tarea['compartido_por']}", size=9, color="#666666", weight=ft.FontWeight.BOLD),
                                ]
                            ),
                            ft.Text(
                                f"⚠️ {tarea['fecha']}" if tarea["atrasado"] else f"{tarea['fecha']}",
                                size=9,
                                color=COLOR_ATRASADO if tarea["atrasado"] else "#666666",
                                weight=ft.FontWeight.BOLD if tarea["atrasado"] else ft.FontWeight.NORMAL,
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
        controls=[crear_tarjeta_tarea(tarea) for tarea in TAREAS_COMPARTIDAS],
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
                    content=ft.Text("COMPARTIDO CONMIGO", size=18, weight=ft.FontWeight.BOLD, color="white")
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
    page.title = "App Tareas - Compartido Conmigo"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 380
    page.window.min_height = 780
    page.padding = 0 
    
    vista = VistaCompartidoConmigo(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)