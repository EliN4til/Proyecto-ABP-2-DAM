import flet as ft

def VistaDetalleTarea(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_SOMBRA_TARJETAS = "#40000000"
    COLOR_BTN_EDITAR = "#4682B4"
    COLOR_BTN_COMPLETAR = "#5A7A8A"
    COLOR_LABEL = "#5B9BD5"

    #datos de tarea de ejemplo, ya se sustituirá por datos reales cuando haya backend
    tarea = {
        "titulo": "Arreglar bug linea 287 fichero UpdateDate.py",
        "tag": "Desarrollo",
        "fecha_inicio": "25/12/25",
        "fecha_fin": "31/12/25",
        "requisitos": [
            "Se requiere que en esa linea haya un bucle que haga sdjfhdskjfhds",
            "Se requiere que en esa linea haya un bucle que haga sdjfhdskjfhds",
            "Se requiere que en esa linea haya un bucle que haga sdjfhdskjfhds",
            "Se requiere que en esa linea haya un bucle que haga sdjfhdskjfhds",
            "Se requiere que en esa linea haya un bucle que haga sdjfhdskjfhds",
            "Se requiere que en esa linea haya un bucle que haga sdjfhdskjfhds",
        ],
        "icono": "👨‍💻"
    }

    def btn_volver_click(e):
        page.snack_bar = ft.SnackBar(ft.Text("Volver atrás"))
        page.snack_bar.open = True
        page.update()

    def btn_editar_click(e):
        page.snack_bar = ft.SnackBar(ft.Text("Editar tarea"))
        page.snack_bar.open = True
        page.update()

    def btn_completar_click(e):
        page.snack_bar = ft.SnackBar(ft.Text("Completar tarea"))
        page.snack_bar.open = True
        page.update()

    #sección superior: icono + título + tag + fecha
    seccion_superior = ft.Container(
        bgcolor="#F5F5F5",
        border_radius=10,
        padding=15,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=12,
            color=COLOR_SOMBRA_TARJETAS,
            offset=ft.Offset(0, 4),
        ),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Row(
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(tarea["icono"], size=30),
                        ft.Text(
                            tarea["titulo"],
                            size=14,
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            expand=True,
                        ),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            spacing=5,
                            controls=[
                                ft.Text("TAG:", size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                ft.Text(tarea["tag"], size=12, color="black", weight=ft.FontWeight.W_500),
                            ]
                        ),
                        ft.Row(
                            spacing=5,
                            controls=[
                                ft.Text("Fecha:", size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                                ft.Text(f"{tarea['fecha_inicio']} - {tarea['fecha_fin']}", size=12, color="black", weight=ft.FontWeight.W_500),
                            ]
                        ),
                    ]
                )
            ]
        )
    )

    def crear_requisito(texto: str):
        return ft.Text(
            f"- {texto}",
            size=12,
            color="black",
        )

    lista_requisitos = ft.Container(
        bgcolor="#F5F5F5",
        border_radius=10,
        padding=15,
        height=220,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=12,
            color=COLOR_SOMBRA_TARJETAS,
            offset=ft.Offset(0, 4),
        ),
        content=ft.ListView(
            spacing=10,
            controls=[crear_requisito(req) for req in tarea["requisitos"]]
        )
    )

    btn_editar = ft.Container(
        width=140,
        height=40,
        bgcolor=COLOR_BTN_EDITAR,
        border_radius=20,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_editar_click,
        content=ft.Text("Editar Tarea", color="white", weight=ft.FontWeight.BOLD, size=13),
    )

    btn_completar = ft.Container(
        width=140,
        height=40,
        bgcolor=COLOR_BTN_COMPLETAR,
        border=ft.border.all(2, COLOR_BTN_COMPLETAR),
        border_radius=20,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=btn_completar_click,
        content=ft.Text("Completar Tarea", color="white", weight=ft.FontWeight.BOLD, size=13),
    )

    fila_botones = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
        controls=[btn_editar, btn_completar]
    )

    tarjeta_blanca = ft.Container(
        width=340,
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=COLOR_SOMBRA),
        content=ft.Column(
            spacing=0,
            tight=True,
            controls=[
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

                ft.Container(
                    height=55,
                    width=340,
                    bgcolor=COLOR_HEADER_BG,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("DETALLE TAREA", size=18, weight=ft.FontWeight.BOLD, color="white")
                ),
                
                ft.Container(
                    padding=ft.padding.only(left=20, right=20, top=20, bottom=25),
                    content=ft.Column(
                        spacing=15,
                        tight=True,
                        controls=[
                            seccion_superior,
                            lista_requisitos,
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