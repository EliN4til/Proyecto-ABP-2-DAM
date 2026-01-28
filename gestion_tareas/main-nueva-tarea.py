import flet as ft
from vistas.vista_nueva_tarea import VistaNuevaTarea

def main(page: ft.Page):
    page.title = "App Tareas - Nueva Tarea"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 380
    page.window.min_height = 780
    page.padding = 0 
    
    vista = VistaNuevaTarea(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)