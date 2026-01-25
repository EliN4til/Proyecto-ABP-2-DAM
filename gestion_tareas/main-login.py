import flet as ft
from vistas.vista_login import VistaLogin

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