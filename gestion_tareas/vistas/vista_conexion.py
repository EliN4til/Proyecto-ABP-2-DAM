import flet as ft

def VistaConexion(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_BTN_BG = "#4682B4"         
    COLOR_INPUT_BG = "#EEEEEE"       
    COLOR_SOMBRA = "#66000000"       

    def btn_conectar_click(e):
        page.snack_bar = ft.SnackBar(ft.Text(f"Conectando a {txt_uri.value}..."))
        page.snack_bar.open = True
        page.update()

    def crear_input(es_password=False):
        return ft.TextField(
            password=es_password,
            can_reveal_password=es_password,
            border_color="transparent",        
            focused_border_color="transparent",
            bgcolor=COLOR_INPUT_BG,
            border_radius=15,
            text_size=14,
            content_padding=15,
            height=45,
            color="black",
            cursor_color="black",
            text_align=ft.TextAlign.LEFT
        )

    txt_uri = crear_input()
    txt_usuario = crear_input()
    txt_pass = crear_input(es_password=True)

    btn_conectar = ft.ElevatedButton(
        content=ft.Text("Iniciar Sesión", color="white", weight=ft.FontWeight.BOLD),
        bgcolor=COLOR_BTN_BG,
        width=180,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=25),
        ),
        on_click=btn_conectar_click
    )

    tarjeta_blanca = ft.Container(
        width=320,
        bgcolor="white",
        border_radius=20,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=20,
            color=COLOR_SOMBRA, 
        ),
        content=ft.Column(
            spacing=0,
            tight=True,
            controls=[
                ft.Container(
                    height=60,
                    width=320,
                    bgcolor=COLOR_HEADER_BG,
                    border_radius=ft.border_radius.only(top_left=20, top_right=20),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text(
                        "CONEXIÓN BD",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="white"
                    )
                ),
                
                ft.Container(
                    padding=ft.padding.only(left=30, right=30, top=25, bottom=40),
                    content=ft.Column(
                        spacing=5,
                        tight=True,
                        controls=[
                            ft.Text("URI", weight=ft.FontWeight.BOLD, color="black", size=14),
                            ft.Container(content=txt_uri, margin=ft.margin.only(bottom=15)),
                            
                            ft.Text("Usuario", weight=ft.FontWeight.BOLD, color="black", size=14),
                            ft.Container(content=txt_usuario, margin=ft.margin.only(bottom=15)),

                            ft.Text("Contraseña", weight=ft.FontWeight.BOLD, color="black", size=14),
                            ft.Container(content=txt_pass, margin=ft.margin.only(bottom=25)),

                            ft.Container(content=btn_conectar, alignment=ft.Alignment(0, 0))
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