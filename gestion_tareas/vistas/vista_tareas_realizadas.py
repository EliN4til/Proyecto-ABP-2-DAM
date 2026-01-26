import flet as ft

def VistaTareasRealizadas(page: ft.Page):
    COLOR_FONDO_TOP = "#152060"
    COLOR_FONDO_BOT = "#4FC3F7"
    COLOR_HEADER_BG = "#1F2855"
    COLOR_SOMBRA = "#44000000"
    COLOR_TAG = "#3F51B5"

    def btn_back_click(e):
        page.go("/")

    def btn_buscador_click(e):
        print("Buscando...")

    def crear_tarjeta_tarea(titulo, tag, fecha):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon("person", color="black", size=30),
                        bgcolor="#EEEEEE",
                        padding=10,
                        border_radius=10,
                    ),
                    ft.Column(
                        expand=True,
                        spacing=2,
                        controls=[
                            ft.Text(titulo, weight="bold", color="black", size=13),
                            ft.Row(
                                spacing=15,
                                controls=[
                                    ft.Text(f"TAG: {tag}", color=COLOR_TAG, size=11, weight="bold"),
                                    ft.Text(f"Completado el: {fecha}", color=COLOR_TAG, size=11, weight="bold"),
                                ]
                            )
                        ]
                    )
                ],
            ),
            bgcolor="white",
            padding=15,
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=10, color="#33000000", offset=ft.Offset(0, 5)),
            margin=ft.margin.only(bottom=15)
        )

    tarjeta_blanca = ft.Container(
        width=360,
        height=720,
        bgcolor="white",
        border_radius=30,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=COLOR_SOMBRA),
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Container(
                    padding=ft.padding.only(left=20, top=15, bottom=5),
                    alignment=ft.Alignment(-1, 0),
                    content=ft.Container(
                        content=ft.Text("←", size=35, color="black", weight="bold"),
                        on_click=btn_back_click,
                        ink=True,
                        border_radius=50,
                    )
                ),
                
                ft.Container(
                    bgcolor=COLOR_HEADER_BG,
                    height=70,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("TAREAS REALIZADAS", size=22, weight="bold", color="white")
                ),
                
                ft.Container(
                    padding=20,
                    expand=True,
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                spacing=10,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.TextField(
                                        hint_text="Buscar por palabras clave...",
                                        bgcolor="#F0F0F0",
                                        border_radius=20,
                                        border_color="transparent",
                                        height=40,
                                        text_size=12,
                                        expand=True,
                                        content_padding=ft.padding.only(left=15, right=15)
                                    ),
                                    ft.Container(
                                        content=ft.Text("Filtrar por", size=11, weight="bold", color="black"),
                                        bgcolor="#E0E0E0",
                                        padding=ft.padding.symmetric(horizontal=10, vertical=8),
                                        border_radius=5
                                    ),
                                    ft.Container(
                                        content=ft.Text("Buscar🔎", color="black", size=12, weight="bold"),
                                        bgcolor="#76FF03",
                                        on_click=btn_buscador_click,
                                        ink=True,
                                        width=90,
                                        height=40,
                                        border_radius=10,
                                        alignment=ft.Alignment(0, 0)
                                    )
                                ]
                            ),
                            
                            ft.Divider(height=20, color="transparent"),
                            
                            ft.Column(
                                expand=True,
                                scroll=ft.ScrollMode.AUTO,
                                controls=[
                                    crear_tarjeta_tarea("Arreglar bug linea 287 fichero UpdateDate.py", "Desarrollo", "25/12/25"),
                                    crear_tarjeta_tarea("Optimizar consultas SQL en modulo Auth", "Backend", "24/12/25"),
                                    crear_tarjeta_tarea("Actualizar documentación de API", "Docs", "23/12/25"),
                                ]
                            )
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