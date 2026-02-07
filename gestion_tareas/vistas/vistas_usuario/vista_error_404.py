import flet as ft

def VistaError404(page: ft.Page):
    """Vista de error 404 - página no encontrada"""
    
    #colores del tema
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_BTN_BG = "#4682B4"         
    COLOR_SOMBRA = "#66000000"       
    
    async def btn_volver_click(e):
        """Volvemos a la pantalla de conexion"""
        await page.push_route("/")
    
    #tarjeta principal con el mensaje de error
    tarjeta_error = ft.Container(
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
                #cabecera con el titulo
                ft.Container(
                    height=60,
                    width=320,
                    bgcolor=COLOR_HEADER_BG,
                    border_radius=ft.BorderRadius.only(top_left=20, top_right=20),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text(
                        "¡OOPS!",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color="white"
                    )
                ),
                
                #contenido del error
                ft.Container(
                    padding=ft.Padding.only(left=30, right=30, top=30, bottom=40),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                        controls=[
                            #emoji triste grande
                            ft.Text(
                                "😵",
                                size=60,
                            ),
                            
                            #codigo de error
                            ft.Text(
                                "404",
                                size=48,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_HEADER_BG
                            ),
                            
                            #mensaje descriptivo
                            ft.Text(
                                "Página no encontrada",
                                size=16,
                                weight=ft.FontWeight.W_500,
                                color="#666666",
                                text_align=ft.TextAlign.CENTER
                            ),
                            
                            #mensaje adicional
                            ft.Text(
                                "La ruta que buscas no existe o ha sido movida.",
                                size=12,
                                color="#999999",
                                text_align=ft.TextAlign.CENTER
                            ),
                            
                            #espacio antes del boton
                            ft.Container(height=10),
                            
                            #boton para volver al inicio
                            ft.Button(
                                content=ft.Text(
                                    "Volver al inicio",
                                    color="white",
                                    weight=ft.FontWeight.BOLD
                                ),
                                bgcolor=COLOR_BTN_BG,
                                width=180,
                                height=45,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=25),
                                ),
                                on_click=btn_volver_click
                            )
                        ]
                    )
                )
            ]
        )
    )
    
    #contenedor principal con gradiente de fondo
    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[COLOR_FONDO_TOP, COLOR_FONDO_BOT],
        ),
        alignment=ft.Alignment(0, 0), 
        content=tarjeta_error
    )


#para probar esta vista de forma independiente
def main(page):
    page.title = "Error 404"
    page.window.width = 420
    page.window.height = 800
    page.padding = 0 
    
    vista = VistaError404(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)
