import flet as ft

def VistaEstadisticas(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    
    #colores para métricas
    COLOR_USUARIOS = "#4CAF50"
    COLOR_TAREAS = "#2196F3"
    COLOR_PENDIENTES = "#FF9800"
    COLOR_COMPLETADAS = "#8BC34A"
    COLOR_ATRASADAS = "#F44336"
    COLOR_EQUIPOS = "#9C27B0"

    #datos demo para los diálogos
    USUARIOS_ACTIVOS = [
        {"nombre": "Ana García", "id": "EMP001", "departamento": "Desarrollo"},
        {"nombre": "Carlos López", "id": "EMP002", "departamento": "Diseño"},
        {"nombre": "María Rodríguez", "id": "EMP003", "departamento": "QA"},
        {"nombre": "Pedro Martínez", "id": "EMP004", "departamento": "DevOps"},
        {"nombre": "Laura Sánchez", "id": "EMP005", "departamento": "Backend"},
    ]

    TAREAS_TOTALES = [
        {"titulo": "Arreglar bug UpdateDate.py", "tag": "Desarrollo", "estado": "Pendiente"},
        {"titulo": "Diseñar mockups dashboard", "tag": "Diseño", "estado": "Completada"},
        {"titulo": "Tests unitarios Auth", "tag": "Testing", "estado": "Completada"},
        {"titulo": "Pipeline CI/CD", "tag": "DevOps", "estado": "Pendiente"},
        {"titulo": "Documentar API v2", "tag": "Documentación", "estado": "Completada"},
    ]

    TAREAS_PENDIENTES = [
        {"titulo": "Arreglar bug UpdateDate.py", "tag": "Desarrollo", "asignado": "Ana García", "fecha_fin": "31/01/26"},
        {"titulo": "Implementar OAuth2", "tag": "Backend", "asignado": "Laura Sánchez", "fecha_fin": "05/02/26"},
        {"titulo": "Diseñar mockups v2", "tag": "Diseño", "asignado": "Carlos López", "fecha_fin": "03/02/26"},
        {"titulo": "Configurar pipeline", "tag": "DevOps", "asignado": "Pedro Martínez", "fecha_fin": "28/01/26"},
    ]

    TAREAS_COMPLETADAS = [
        {"titulo": "Tests unitarios Auth", "tag": "Testing", "asignado": "María Rodríguez", "fecha_completado": "25/01/26"},
        {"titulo": "Documentar API v2", "tag": "Documentación", "asignado": "Sofia Ruiz", "fecha_completado": "23/01/26"},
        {"titulo": "Migrar base de datos", "tag": "Base de Datos", "asignado": "Diego Torres", "fecha_completado": "20/01/26"},
        {"titulo": "Optimizar queries SQL", "tag": "Backend", "asignado": "Laura Sánchez", "fecha_completado": "18/01/26"},
    ]

    TAREAS_ATRASADAS = [
        {"titulo": "Corregir validación form", "tag": "Frontend", "asignado": "Juan Fernández", "dias_atraso": 5},
        {"titulo": "Endpoint notificaciones", "tag": "Backend", "asignado": "Laura Sánchez", "dias_atraso": 3},
        {"titulo": "Actualizar dependencias", "tag": "DevOps", "asignado": "Pedro Martínez", "dias_atraso": 7},
    ]

    EQUIPOS_ACTIVOS = [
        {"nombre": "Cloud Infrastructure", "miembros": 6, "lider": "Pedro Martínez"},
        {"nombre": "Frontend Team", "miembros": 5, "lider": "Juan Fernández"},
        {"nombre": "Backend Team", "miembros": 7, "lider": "Laura Sánchez"},
        {"nombre": "QA Team", "miembros": 4, "lider": "María Rodríguez"},
    ]

    def btn_volver_click(e):
        """Acción al hacer clic en el botón volver atrás"""
        page.snack_bar = ft.SnackBar(ft.Text("Volver atrás"))
        page.snack_bar.open = True
        page.update()

    def mostrar_dialog_usuarios(e):
        """Muestra diálogo con lista de usuarios activos"""
        lista_items = [
            ft.Container(
                padding=ft.padding.all(8),
                border=ft.border.only(bottom=ft.BorderSide(1, COLOR_BORDE)),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            spacing=10,
                            controls=[
                                ft.Text("👤", size=16),
                                ft.Column(
                                    spacing=0,
                                    controls=[
                                        ft.Text(u["nombre"], size=12, color="black", weight=ft.FontWeight.W_500),
                                        ft.Text(u["id"], size=10, color=COLOR_LABEL),
                                    ]
                                ),
                            ]
                        ),
                        ft.Text(u["departamento"], size=10, color="#666666"),
                    ]
                )
            ) for u in USUARIOS_ACTIVOS
        ]

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("👥 Usuarios Activos", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=320,
                height=280,
                bgcolor="white",
                content=ft.ListView(controls=lista_items, spacing=0),
            ),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog(dialog))],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def mostrar_dialog_tareas_totales(e):
        """Muestra diálogo con todas las tareas"""
        lista_items = [
            ft.Container(
                padding=ft.padding.all(8),
                border=ft.border.only(bottom=ft.BorderSide(1, COLOR_BORDE)),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=0,
                            expand=True,
                            controls=[
                                ft.Text(t["titulo"], size=11, color="black", weight=ft.FontWeight.W_500, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(t["tag"], size=10, color=COLOR_LABEL),
                            ]
                        ),
                        ft.Container(
                            bgcolor=COLOR_COMPLETADAS if t["estado"] == "Completada" else COLOR_PENDIENTES,
                            border_radius=8,
                            padding=ft.padding.only(left=6, right=6, top=2, bottom=2),
                            content=ft.Text(t["estado"], size=9, color="white"),
                        ),
                    ]
                )
            ) for t in TAREAS_TOTALES
        ]

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("📋 Total Tareas", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=320,
                height=280,
                bgcolor="white",
                content=ft.ListView(controls=lista_items, spacing=0),
            ),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog(dialog))],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def mostrar_dialog_pendientes(e):
        """Muestra diálogo con tareas pendientes"""
        lista_items = [
            ft.Container(
                padding=ft.padding.all(8),
                border=ft.border.only(bottom=ft.BorderSide(1, COLOR_BORDE)),
                content=ft.Column(
                    spacing=3,
                    controls=[
                        ft.Text(t["titulo"], size=11, color="black", weight=ft.FontWeight.W_500, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"👤 {t['asignado']}", size=10, color="#666666"),
                                ft.Text(f"📅 {t['fecha_fin']}", size=10, color=COLOR_PENDIENTES),
                            ]
                        ),
                    ]
                )
            ) for t in TAREAS_PENDIENTES
        ]

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("⏳ Tareas Pendientes", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=320,
                height=280,
                bgcolor="white",
                content=ft.ListView(controls=lista_items, spacing=0),
            ),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog(dialog))],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def mostrar_dialog_completadas(e):
        """Muestra diálogo con tareas completadas"""
        lista_items = [
            ft.Container(
                padding=ft.padding.all(8),
                border=ft.border.only(bottom=ft.BorderSide(1, COLOR_BORDE)),
                content=ft.Column(
                    spacing=3,
                    controls=[
                        ft.Text(t["titulo"], size=11, color="black", weight=ft.FontWeight.W_500, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"👤 {t['asignado']}", size=10, color="#666666"),
                                ft.Text(f"✅ {t['fecha_completado']}", size=10, color=COLOR_COMPLETADAS),
                            ]
                        ),
                    ]
                )
            ) for t in TAREAS_COMPLETADAS
        ]

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("✅ Tareas Completadas", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=320,
                height=280,
                bgcolor="white",
                content=ft.ListView(controls=lista_items, spacing=0),
            ),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog(dialog))],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def mostrar_dialog_atrasadas(e):
        """Muestra diálogo con tareas atrasadas"""
        lista_items = [
            ft.Container(
                padding=ft.padding.all(8),
                border=ft.border.only(bottom=ft.BorderSide(1, COLOR_BORDE)),
                content=ft.Column(
                    spacing=3,
                    controls=[
                        ft.Text(t["titulo"], size=11, color="black", weight=ft.FontWeight.W_500, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"👤 {t['asignado']}", size=10, color="#666666"),
                                ft.Text(f"⚠️ {t['dias_atraso']} días de atraso", size=10, color=COLOR_ATRASADAS),
                            ]
                        ),
                    ]
                )
            ) for t in TAREAS_ATRASADAS
        ]

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("⚠️ Tareas Atrasadas", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=320,
                height=280,
                bgcolor="white",
                content=ft.ListView(controls=lista_items, spacing=0),
            ),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog(dialog))],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def mostrar_dialog_equipos(e):
        """Muestra diálogo con equipos activos"""
        lista_items = [
            ft.Container(
                padding=ft.padding.all(8),
                border=ft.border.only(bottom=ft.BorderSide(1, COLOR_BORDE)),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=0,
                            controls=[
                                ft.Text(eq["nombre"], size=12, color="black", weight=ft.FontWeight.W_500),
                                ft.Text(f"Líder: {eq['lider']}", size=10, color=COLOR_LABEL),
                            ]
                        ),
                        ft.Container(
                            bgcolor=COLOR_EQUIPOS,
                            border_radius=10,
                            padding=ft.padding.only(left=8, right=8, top=2, bottom=2),
                            content=ft.Text(f"{eq['miembros']} 👥", size=10, color="white"),
                        ),
                    ]
                )
            ) for eq in EQUIPOS_ACTIVOS
        ]

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("🏢 Equipos Activos", size=16, weight=ft.FontWeight.BOLD, color="black"),
            bgcolor="white",
            content=ft.Container(
                width=320,
                height=280,
                bgcolor="white",
                content=ft.ListView(controls=lista_items, spacing=0),
            ),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog(dialog))],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def cerrar_dialog(dialog):
        dialog.open = False
        page.update()

    def crear_tarjeta_metrica(titulo: str, valor: str, icono: str, color: str, subtitulo: str = None, on_click=None):
        """Crea una tarjeta de métrica con icono y valor, clickeable"""
        return ft.Container(
            width=155,
            height=90,
            bgcolor="white",
            border_radius=12,
            border=ft.border.all(1, COLOR_BORDE),
            padding=ft.padding.all(12),
            ink=True,
            on_click=on_click,
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(icono, size=24),
                            ft.Text(valor, size=22, color=color, weight=ft.FontWeight.BOLD),
                        ]
                    ),
                    ft.Text(titulo, size=11, color="black", weight=ft.FontWeight.W_500),
                    ft.Text(subtitulo, size=9, color="#888888") if subtitulo else ft.Container(),
                ]
            )
        )

    def crear_barra_progreso(label: str, valor: int, total: int, color: str):
        """Crea una barra de progreso con etiqueta"""
        porcentaje = (valor / total) * 100 if total > 0 else 0
        return ft.Column(
            spacing=3,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(label, size=11, color="black"),
                        ft.Text(f"{valor}/{total}", size=11, color=COLOR_LABEL),
                    ]
                ),
                ft.Container(
                    height=8,
                    border_radius=4,
                    bgcolor="#E0E0E0",
                    content=ft.Container(
                        width=porcentaje * 3.2,  #ancho máximo ~320px
                        height=8,
                        border_radius=4,
                        bgcolor=color,
                    )
                ),
            ]
        )

    def crear_item_ranking(posicion: int, nombre: str, tareas: int, emoji: str = "👤"):
        """Crea un item del ranking de usuarios"""
        return ft.Container(
            padding=ft.padding.only(top=5, bottom=5),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Container(
                                width=24,
                                height=24,
                                border_radius=12,
                                bgcolor=COLOR_LABEL if posicion <= 3 else "#E0E0E0",
                                alignment=ft.Alignment(0, 0),
                                content=ft.Text(str(posicion), size=11, color="white" if posicion <= 3 else "black", weight=ft.FontWeight.BOLD),
                            ),
                            ft.Text(emoji, size=16),
                            ft.Text(nombre, size=12, color="black"),
                        ]
                    ),
                    ft.Container(
                        bgcolor=COLOR_COMPLETADAS,
                        border_radius=10,
                        padding=ft.padding.only(left=8, right=8, top=2, bottom=2),
                        content=ft.Text(f"{tareas} tareas", size=10, color="white", weight=ft.FontWeight.W_500),
                    ),
                ]
            )
        )

    #botón volver
    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight=ft.FontWeight.BOLD),
        on_click=btn_volver_click,
        ink=True,
        padding=10,
    )

    #sección de métricas principales (2x2)
    seccion_metricas = ft.Column(
        spacing=10,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    crear_tarjeta_metrica("Usuarios Activos", "47", "👥", COLOR_USUARIOS, "+3 este mes", mostrar_dialog_usuarios),
                    crear_tarjeta_metrica("Total Tareas", "283", "📋", COLOR_TAREAS, "Este mes", mostrar_dialog_tareas_totales),
                ]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    crear_tarjeta_metrica("Pendientes", "64", "⏳", COLOR_PENDIENTES, "Por completar", mostrar_dialog_pendientes),
                    crear_tarjeta_metrica("Completadas", "189", "✅", COLOR_COMPLETADAS, "66.8%", mostrar_dialog_completadas),
                ]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    crear_tarjeta_metrica("Atrasadas", "30", "⚠️", COLOR_ATRASADAS, "Requieren atención", mostrar_dialog_atrasadas),
                    crear_tarjeta_metrica("Equipos", "8", "🏢", COLOR_EQUIPOS, "Activos", mostrar_dialog_equipos),
                ]
            ),
        ]
    )

    #sección tareas por departamento
    seccion_departamentos = ft.Container(
        bgcolor="white",
        border_radius=12,
        border=ft.border.all(1, COLOR_BORDE),
        padding=ft.padding.all(15),
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Text("Tareas por Departamento", size=13, color="black", weight=ft.FontWeight.BOLD),
                crear_barra_progreso("Desarrollo", 45, 60, "#4CAF50"),
                crear_barra_progreso("Diseño", 28, 35, "#2196F3"),
                crear_barra_progreso("QA", 32, 40, "#FF9800"),
                crear_barra_progreso("DevOps", 18, 25, "#9C27B0"),
                crear_barra_progreso("Backend", 38, 50, "#00BCD4"),
            ]
        )
    )

    #sección ranking usuarios
    seccion_ranking = ft.Container(
        bgcolor="white",
        border_radius=12,
        border=ft.border.all(1, COLOR_BORDE),
        padding=ft.padding.all(15),
        content=ft.Column(
            spacing=5,
            controls=[
                ft.Text("🏆 Top Usuarios del Mes", size=13, color="black", weight=ft.FontWeight.BOLD),
                ft.Divider(height=1, color=COLOR_BORDE),
                crear_item_ranking(1, "Ana García", 32, "👩‍💻"),
                crear_item_ranking(2, "Carlos López", 28, "👨‍🎨"),
                crear_item_ranking(3, "María Rodríguez", 25, "👩‍🔬"),
                crear_item_ranking(4, "Pedro Martínez", 22, "👨‍💼"),
                crear_item_ranking(5, "Laura Sánchez", 19, "👩‍💼"),
            ]
        )
    )

    #resumen rápido
    seccion_resumen = ft.Container(
        bgcolor="#F5F8FF",
        border_radius=12,
        padding=ft.padding.all(12),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text("📊 Resumen Rápido", size=12, color="black", weight=ft.FontWeight.BOLD),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Productividad media:", size=11, color="#666666"),
                        ft.Text("87%", size=11, color=COLOR_COMPLETADAS, weight=ft.FontWeight.BOLD),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Tareas/usuario promedio:", size=11, color="#666666"),
                        ft.Text("6.0", size=11, color=COLOR_TAREAS, weight=ft.FontWeight.BOLD),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Tiempo medio resolución:", size=11, color="#666666"),
                        ft.Text("2.3 días", size=11, color=COLOR_PENDIENTES, weight=ft.FontWeight.BOLD),
                    ]
                ),
            ]
        )
    )

    #contenido scrolleable
    contenido_scroll = ft.Column(
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            seccion_metricas,
            seccion_departamentos,
            seccion_ranking,
            seccion_resumen,
        ]
    )

    #tarjeta blanca principal
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
            content=ft.Container(
                height=580,
                content=contenido_scroll,
            )
        )
    )

    #header flotante
    header_flotante = ft.Container(
        width=220,
        height=50,
        bgcolor=COLOR_HEADER_BG,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            "ESTADÍSTICAS",
            size=18,
            weight=ft.FontWeight.BOLD,
            color="white"
        )
    )

    #contenido superpuesto (tarjeta + header)
    contenido_superpuesto = ft.Container(
        width=380,
        height=700,
        content=ft.Stack(
            controls=[
                ft.Container(
                    content=tarjeta_blanca,
                    top=30,
                ),
                ft.Container(
                    content=header_flotante,
                    top=0,
                    left=80,
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
    page.title = "App Tareas - Estadísticas"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 400
    page.window.min_height = 750
    page.padding = 0 
    
    vista = VistaEstadisticas(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)