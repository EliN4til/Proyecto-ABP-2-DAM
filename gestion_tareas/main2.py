import flet as ft
from vistas.vista_login import VistaLogin

def main(page: ft.Page):
    page.title = "App Tareas - Conexión"
    
    page.window_width = 400 
    page.window_height = 800
    page.padding = 0 
    
    vista = VistaLogin(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)