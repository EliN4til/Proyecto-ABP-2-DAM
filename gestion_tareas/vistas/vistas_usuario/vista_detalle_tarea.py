import flet as ft

def VistaDetalleTarea(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_SOMBRA_TARJETAS = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    COLOR_BTN_EDITAR = "#4682B4"
    COLOR_BTN_COMPLETAR = "#4CAF50"
    
    COLOR_PRIORIDAD_ALTA = "#E53935"
    COLOR_PRIORIDAD_MEDIA = "#FF9800"
    COLOR_PRIORIDAD_BAJA = "#4CAF50"

    #datos demo de la tarea
    tarea = {
        "titulo": "Arreglar bug linea 287 fichero UpdateDate.py",
        "tag": "Desarrollo",
        "emoji": "👨‍💻",
        "proyecto": "App Móvil v2.0",
        "departamento": "Desarrollo",
        "prioridad": "Alta",
        "asignados": ["Ana García", "Laura Sánchez"],
        "fecha_inicio": "25/12/25",
        "fecha_fin": "31/12/25",
        "estado": "Pendiente",
        "requisitos": [
            "Identificar el error en la línea 287 del fichero UpdateDate.py",
            "El bucle debe iterar correctamente sobre la lista de fechas",
            "Validar que no se produzcan excepciones de tipo IndexError",
            "Añadir logs para seguimiento del proceso",
            "Realizar pruebas con datos de producción simulados",
            "Documentar la solución en el wiki del proyecto"
        ]
    }

    def get_color_prioridad(prioridad):
        if prioridad == "Alta":
            return COLOR_PRIORIDAD_ALTA
        elif prioridad == "Media":
            return COLOR_PRIORIDAD_MEDIA
        else:
            return COLOR_PRIORIDAD_BAJA

    def btn_volver_click(e):
        page.snack_bar = ft.SnackBar(ft.Text("Volver atrás"))
        page.snack_bar.open = True
        page.update()

    def btn_editar_click(e):
        page.snack_bar = ft.SnackBar(ft.Text(f"Editando tarea: {tarea['titulo']}"))
        page.snack_bar.open = True
        page.update()

    def btn_completar_click(e):
        page.snack_bar = ft.SnackBar(ft.Text("¡Tarea completada con éxito!"))
        page.snack_bar.open = True
        page.update()

    #header tarea (emoji + titulo)
    header_tarea = ft.Row(
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Text(tarea["emoji"], size=32),
            ft.Text(
                tarea["titulo"],
                size=14,
                color="black",
                weight=ft.FontWeight.BOLD,
                expand=True,
            ),
        ]
    )

    #fila de badges (prioridad y tag)
    fila_badges = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Container(
                bgcolor=get_color_prioridad(tarea["prioridad"]),
                border_radius=15,
                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                content=ft.Text(f"Prioridad {tarea['prioridad']}", size=11, color="white", weight=ft.FontWeight.BOLD),
            ),
            ft.Container(
                bgcolor="#F0F4F8",
                border_radius=15,
                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                border=ft.border.all(1, COLOR_BORDE),
                content=ft.Row(
                    spacing=5,
                    controls=[
                        ft.Icon(ft.Icons.LABEL_OUTLINE, size=14, color=COLOR_LABEL),
                        ft.Text(tarea["tag"], size=11, color="black", weight=ft.FontWeight.W_500),
                    ]
                )
            ),
        ]
    )

    #bloque de informacion (proyecto, depto, asignados, fechas)
    bloque_info = ft.Container(
        bgcolor="white",
        border=ft.border.all(1, COLOR_BORDE),
        border_radius=10,
        padding=12,
        content=ft.Column(
            spacing=8,
            controls=[
                #fila proyecto y departamento
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(spacing=2, controls=[
                            ft.Text("Proyecto", size=10, color=COLOR_LABEL, weight=ft.FontWeight.BOLD),
                            ft.Text(tarea["proyecto"], size=11, color="black"),
                        ]),
                        ft.Column(spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END, controls=[
                            ft.Text("Departamento", size=10, color=COLOR_LABEL, weight=ft.FontWeight.BOLD),
                            ft.Text(tarea["departamento"], size=11, color="black"),
                        ]),
                    ]
                ),
                ft.Divider(height=1, color="#F0F0F0"),
                #asignados
                ft.Column(spacing=4, controls=[
                    ft.Row(spacing=5, controls=[
                        ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=14, color=COLOR_LABEL),
                        ft.Text("Asignado a:", size=10, color=COLOR_LABEL, weight=ft.FontWeight.BOLD),
                    ]),
                    ft.Text(", ".join(tarea["asignados"]), size=11, color="black", weight=ft.FontWeight.W_500),
                ]),
                ft.Divider(height=1, color="#F0F0F0"),
                #fechas
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(spacing=2, controls=[
                            ft.Text("Fecha Inicio", size=10, color=COLOR_LABEL),
                            ft.Text(tarea["fecha_inicio"], size=11, color="black", weight=ft.FontWeight.BOLD),
                        ]),
                        ft.Column(spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END, controls=[
                            ft.Text("Fecha Límite", size=10, color=COLOR_LABEL),
                            ft.Text(tarea["fecha_fin"], size=11, color="black", weight=ft.FontWeight.BOLD),
                        ]),
                    ]
                ),
            ]
        )
    )

    #lista de requerimientos
    def crear_requisito(texto: str):
        return ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Text("•", size=14, color=COLOR_LABEL, weight="bold"),
                ft.Text(texto, size=12, color="#444444", expand=True),
            ]
        )

    contenedor_requisitos = ft.Container(
        bgcolor="#FAFAFA", 
        border_radius=10,
        padding=12,
        border=ft.border.all(1, COLOR_BORDE),
        expand=True, 
        content=ft.Column(
            controls=[
                ft.Text("Requerimientos", size=12, color="black", weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, color="transparent"),
                ft.ListView(
                    spacing=6,
                    padding=0,
                    controls=[crear_requisito(req) for req in tarea["requisitos"]]
                )
            ]
        )
    )

    #botones de accion
    btn_editar = ft.Container(
        expand=True,
        height=42,
        bgcolor="white",
        border=ft.border.all(1, COLOR_BTN_EDITAR),
        border_radius=21,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_editar_click,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
            controls=[
                ft.Icon(ft.Icons.EDIT, size=16, color=COLOR_BTN_EDITAR),
                ft.Text("Editar", color=COLOR_BTN_EDITAR, weight=ft.FontWeight.BOLD, size=13),
            ]
        )
    )

    btn_completar = ft.Container(
        expand=True,
        height=42,
        bgcolor=COLOR_BTN_COMPLETAR,
        border_radius=21,
        alignment=ft.Alignment(0, 0),
        ink=True,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=COLOR_SOMBRA_TARJETAS, offset=ft.Offset(0, 4)),
        on_click=btn_completar_click,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
            controls=[
                ft.Icon(ft.Icons.CHECK, size=16, color="white"),
                ft.Text("Completar", color="white", weight=ft.FontWeight.BOLD, size=13),
            ]
        )
    )

    fila_botones = ft.Container(
        padding=ft.padding.only(top=10),
        content=ft.Row(
            spacing=15,
            controls=[btn_editar, btn_completar]
        )
    )

    #tarjeta blanca principal
    tarjeta_blanca = ft.Container(
        width=400,
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=COLOR_SOMBRA),
        content=ft.Column(
            spacing=0,
            tight=True,
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
                    content=ft.Text("DETALLE TAREA", size=18, weight=ft.FontWeight.BOLD, color="white")
                ),
                
                #contenido scrollable
                ft.Container(
                    padding=ft.padding.only(left=20, right=20, top=20, bottom=25),
                    height=600,
                    content=ft.Column(
                        spacing=15,
                        scroll=ft.ScrollMode.HIDDEN, 
                        controls=[
                            header_tarea,
                            fila_badges,
                            bloque_info,
                            contenedor_requisitos,
                            fila_botones,
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
    page.title = "App Tareas - Detalle Tarea"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 380
    page.window.min_height = 780
    page.padding = 0 
    
    vista = VistaDetalleTarea(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)