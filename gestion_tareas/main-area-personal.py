import flet as ft
from vistas.vista_area_personal import VistaAreaPersonal

def main(page: ft.Page):
    page.title = "App Tareas - Área Personal"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 360
    page.window.min_height = 480
    page.padding = 0 
    
    vista = VistaAreaPersonal(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)