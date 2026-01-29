import flet as ft

def VistaLogin(page: ft.Page):
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"
    COLOR_BTN_BG = "#5B88C4"
    COLOR_INPUT_BG = "#EEEEEE"       
    COLOR_SOMBRA = "#66000000"       

    def btn_login_click(e):
        page.snack_bar = ft.SnackBar(ft.Text("Iniciando sesión..."))
        page.snack_bar.open = True
        page.update()

    def btn_back_click(e):
        page.go("/")

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
        )

    txt_email = crear_input()
    txt_pass = crear_input(es_password=True)

    btn_iniciar = ft.ElevatedButton(
        content=ft.Text("Iniciar Sesión", color="white", weight=ft.FontWeight.BOLD),
        bgcolor=COLOR_BTN_BG,
        width=180,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=25),
        ),
        on_click=btn_login_click
    )

    tarjeta_blanca = ft.Container(
        width=320,
        bgcolor="white",
        border_radius=25,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=COLOR_SOMBRA),
        content=ft.Column(
            spacing=0,
            tight=True,
            controls=[
                ft.Container(
                    padding=ft.padding.only(left=20, top=15, bottom=10),
                    alignment=ft.Alignment(-1, 0),
                    content=ft.Container(
                        content=ft.Text("←", size=30, color="black", weight="bold"),
                        on_click=btn_back_click,
                        ink=True,
                        border_radius=50,
                        padding=5,
                    ),
                ),

                ft.Container(
                    height=55,
                    width=320,
                    bgcolor=COLOR_HEADER_BG,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("INICIO DE SESIÓN", size=18, weight=ft.FontWeight.BOLD, color="white")
                ),
                
                ft.Container(
                    padding=ft.padding.only(left=30, right=30, top=30, bottom=40),
                    content=ft.Column(
                        spacing=5,
                        tight=True,
                        controls=[
                            ft.Text("Correo Electrónico", weight=ft.FontWeight.BOLD, color="black", size=14),
                            ft.Container(content=txt_email, margin=ft.margin.only(bottom=15)),
                            
                            ft.Text("Contraseña", weight=ft.FontWeight.BOLD, color="black", size=14),
                            ft.Container(content=txt_pass, margin=ft.margin.only(bottom=25)),

                            ft.Container(content=btn_iniciar, alignment=ft.Alignment(0, 0))
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
    page.title = "App Tareas - Conexión"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 360
    page.window.min_height = 480
    page.padding = 0 
    
    vista = VistaLogin(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)