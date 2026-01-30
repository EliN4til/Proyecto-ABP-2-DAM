import flet as ft

#importamos todas las vistas de admin
from vistas.vistas_admin.vista_dashboard import VistaAreaAdmin
from vistas.vistas_admin.vista_configuracion import VistaConfiguracion
from vistas.vistas_admin.vista_auditoria import VistaAuditoria
from vistas.vistas_admin.vista_estadisticas import VistaEstadisticas
from vistas.vistas_admin.vista_gestionar_trabajadores import VistaGestionarTrabajadores
from vistas.vistas_admin.vista_gestionar_roles import VistaGestionarRoles
from vistas.vistas_admin.vista_crear_trabajador import VistaCrearTrabajador
from vistas.vistas_admin.vista_crear_departamento import VistaCrearDepartamento
from vistas.vistas_admin.vista_crear_equipo import VistaCrearEquipo
from vistas.vistas_admin.vista_crear_proyectos import VistaCrearProyecto
from vistas.vistas_admin.vista_gestionar_proyectos import VistaGestionarProyectos
from vistas.vistas_admin.vista_gestionar_departamentos import VistaGestionarDepartamentos

#importamos todas las vistas de usuario
from vistas.vistas_usuario.vista_login import VistaLogin
from vistas.vistas_usuario.vista_conexion import VistaConexion
from vistas.vistas_usuario.vista_area_personal import VistaAreaPersonal
from vistas.vistas_usuario.vista_mis_datos import VistaMisDatos
from vistas.vistas_usuario.vista_tareas_pendientes import VistaTareasPendientes
from vistas.vistas_usuario.vista_tareas_realizadas import VistaTareasRealizadas
from vistas.vistas_usuario.vista_tareas_atrasadas import VistaTareasAtrasadas
from vistas.vistas_usuario.vista_nueva_tarea import VistaNuevaTarea
from vistas.vistas_usuario.vista_compartido_conmigo import VistaCompartidoConmigo
from vistas.vistas_usuario.vista_detalle_tarea import VistaDetalleTarea
from vistas.vistas_usuario.vista_mis_proyectos import VistaMisProyectos
from vistas.vistas_usuario.vista_error_404 import VistaError404


def main(page: ft.Page):
    """Función principal que configura la app y gestiona la navegación"""
    
    #configuracion de la ventana
    page.title = "Gestión de Tareas"
    page.window.width = 420
    page.window.height = 800
    page.window.min_width = 360
    page.window.min_height = 600
    page.padding = 0
    
    #diccionario que mapea cada ruta a su vista correspondiente
    #esto nos permite navegar entre vistas usando page.go("/ruta")
    rutas = {
        #vistas principales
        "/": lambda: VistaConexion(page),
        "/login": lambda: VistaLogin(page),
        
        #vistas de usuario
        "/area_personal": lambda: VistaAreaPersonal(page),
        "/mis_datos": lambda: VistaMisDatos(page),
        "/tareas_pendientes": lambda: VistaTareasPendientes(page),
        "/tareas_realizadas": lambda: VistaTareasRealizadas(page),
        "/tareas_atrasadas": lambda: VistaTareasAtrasadas(page),
        "/nueva_tarea": lambda: VistaNuevaTarea(page),
        "/compartido_conmigo": lambda: VistaCompartidoConmigo(page),
        "/detalle_tarea": lambda: VistaDetalleTarea(page),
        "/mis_proyectos": lambda: VistaMisProyectos(page),
        
        #vistas de admin
        "/area_admin": lambda: VistaAreaAdmin(page),
        "/configuracion": lambda: VistaConfiguracion(page),
        "/auditoria": lambda: VistaAuditoria(page),
        "/estadisticas": lambda: VistaEstadisticas(page),
        "/gestionar_trabajadores": lambda: VistaGestionarTrabajadores(page),
        "/gestionar_roles": lambda: VistaGestionarRoles(page),
        "/crear_trabajador": lambda: VistaCrearTrabajador(page),
        "/crear_departamento": lambda: VistaCrearDepartamento(page),
        "/crear_equipo": lambda: VistaCrearEquipo(page),
        "/crear_proyecto": lambda: VistaCrearProyecto(page),
        "/gestionar_proyectos": lambda: VistaGestionarProyectos(page),
        "/gestionar_departamentos": lambda: VistaGestionarDepartamentos(page),  #archivo con guiones
    }
    
    def cambiar_ruta(e):
        """Manejador del cambio de ruta - se ejecuta cada vez que llamamos page.go()"""
        
        #limpiamos la pantalla actual
        page.controls.clear()
        
        #obtenemos la ruta actual
        ruta_actual = page.route
        
        #buscamos la vista correspondiente en el diccionario
        if ruta_actual in rutas:
            vista = rutas[ruta_actual]()
            page.add(vista)
        else:
            #si la ruta no existe, mostramos la vista de error 404
            vista = VistaError404(page)
            page.add(vista)
        
        page.update()
    
    #conectamos el manejador de cambio de ruta
    page.on_route_change = cambiar_ruta
    
    #cargamos la vista inicial (conexion)
    vista = VistaConexion(page)
    page.add(vista)


#ejecutamos la app
if __name__ == "__main__":
    ft.app(target=main)