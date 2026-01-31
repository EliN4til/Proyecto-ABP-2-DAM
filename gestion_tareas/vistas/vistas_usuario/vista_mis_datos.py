import flet as ft
from servicios.sesion_service import obtener_usuario

def VistaMisDatos(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_LABEL = "#5B9BD5"

    #obtenemos los datos del usuario de la sesión
    usuario_sesion = obtener_usuario()
    
    #si hay sesión activa, cogemos los datos del usuario
    if usuario_sesion:
        nombre = usuario_sesion.get("nombre", "Usuario")
        apellidos = usuario_sesion.get("apellidos", "")
        estado = usuario_sesion.get("estado", "ACTIVO")
        identificador = usuario_sesion.get("identificador", "N/A")
        empresa = usuario_sesion.get("empresa", "N/A")
        equipo = usuario_sesion.get("equipo", "N/A")
        cargo = usuario_sesion.get("cargo", "N/A")
        id_empleado = usuario_sesion.get("id_empleado", "N/A")
        correo = usuario_sesion.get("email", "N/A")
        telefono = usuario_sesion.get("telefono", "N/A")
        ubicacion = usuario_sesion.get("ubicacion", "N/A")
        
        #el departamento es un objeto con nombre y ubicacion
        departamento = usuario_sesion.get("departamento", {})
        if departamento:
            nombre_depto = departamento.get("nombre", "N/A")
        else:
            nombre_depto = "N/A"
        
        #la fecha de incorporacion viene como objeto, la convertimos a string
        fecha_incorporacion_raw = usuario_sesion.get("fecha_incorporacion", None)
        if fecha_incorporacion_raw:
            #si es un string lo dejamos tal cual, si es fecha la formateamos
            if isinstance(fecha_incorporacion_raw, str):
                fecha_incorporacion = fecha_incorporacion_raw
            else:
                fecha_incorporacion = str(fecha_incorporacion_raw)[:10]
        else:
            fecha_incorporacion = "N/A"
        
        foto_url = usuario_sesion.get("foto", None)
    else:
        #si no hay una sesión, ponemos valores por defecto (esto es por si ejecutamos la vista directamente sin iniciar sesión, para probarla)
        nombre = "Usuario"
        apellidos = ""
        estado = "ACTIVO"
        identificador = "N/A"
        empresa = "N/A"
        equipo = "N/A"
        cargo = "N/A"
        id_empleado = "N/A"
        correo = "N/A"
        telefono = "N/A"
        ubicacion = "N/A"
        nombre_depto = "N/A"
        fecha_incorporacion = "N/A"
        foto_url = None

    def crear_campo(label: str, valor: str):
        return ft.Column(
            spacing=2,
            controls=[
                ft.Text(label, size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                ft.Text(valor, size=14, color="black", weight=ft.FontWeight.BOLD),
            ]
        )

    def btn_volver_click(e):
        #volvemos al área personal
        page.go("/area_personal")

    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight=ft.FontWeight.BOLD),
        on_click=btn_volver_click,
        ink=True,
        padding=10,
    )

    #foto del perfil
    if foto_url:
        contenido_foto = ft.Image(
            src=foto_url,
            width=100,
            height=100,
            fit=ft.ImageFit.COVER,
            border_radius=10,
        )
    else:
        contenido_foto = ft.Icon("person", size=50, color="#999999")
    
    foto_perfil = ft.Container(
        width=100,
        height=100,
        border_radius=10,
        bgcolor="#E0E0E0",
        content=contenido_foto
    )

    #estado con punto verde o rojo
    estado_activo = estado == "ACTIVO"
    if estado_activo:
        color_estado = "#4CAF50"  #verde
    else:
        color_estado = "#F44336"  #rojo
    
    estado_widget = ft.Row(
        spacing=5,
        controls=[
            ft.Text(estado, size=14, color="black", weight=ft.FontWeight.BOLD),
            ft.Container(
                width=12,
                height=12,
                border_radius=6,
                bgcolor=color_estado,
            )
        ]
    )

    #sección superior (foto + nombre/apellidos/estado)
    seccion_superior = ft.Row(
        spacing=15,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            foto_perfil,
            ft.Column(
                spacing=8,
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text("Nombre", size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                            ft.Text(nombre, size=14, color="black", weight=ft.FontWeight.BOLD),
                        ]
                    ),
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text("Apellidos", size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                            ft.Text(apellidos, size=14, color="black", weight=ft.FontWeight.BOLD),
                        ]
                    ),
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text("Estado", size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                            estado_widget,
                        ]
                    ),
                ]
            )
        ]
    )


    tarjeta_blanca = ft.Container(
        width=340,
        bgcolor="white",
        border_radius=20,
        shadow=ft.BoxShadow(
        ),

        content=ft.Container(
            padding=ft.padding.only(left=20, right=20, top=50, bottom=25),
            content=ft.Column(
                spacing=15,
                tight=True,
                controls=[
                    seccion_superior,
                    ft.Divider(height=1, color="#E0E0E0"),
                    crear_campo("Identificador", identificador),
                    crear_campo("Empresa", empresa),
                    crear_campo("Departamento", nombre_depto),
                    crear_campo("Equipo", equipo),
                    crear_campo("Cargo", cargo),
                    crear_campo("ID Empleado", id_empleado),
                    crear_campo("Correo corporativo", correo),
                    crear_campo("Teléfono", telefono),
                    crear_campo("Ubicación", ubicacion),
                    crear_campo("Fecha de Incorporación", fecha_incorporacion),
                ]
            )
        )
    )

    #bloque azul flotante superior
    header_flotante = ft.Container(
        width=200,
        height=50,
        bgcolor=COLOR_HEADER_BG,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            "MIS DATOS",
            size=18,
            weight=ft.FontWeight.BOLD,
            color="white"
        )
    )

    contenido_superpuesto = ft.Container(
        width=340,
        height=820,
        content=ft.Stack(
            controls=[
                ft.Container(
                    content=tarjeta_blanca,
                    top=25,
                ),
                ft.Container(
                    content=header_flotante,
                    top=0,
                    left=70,
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
        
        content=ft.Stack(
            expand=True,
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment(0, 0),
                    content=contenido_superpuesto
                ),

                ft.Container(
                    content=btn_volver,
                    top=10,
                    left=10,
                )
            ]
        )
    )


def main(page: ft.Page):
    page.title = "App Tareas - Mis Datos"
    
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 380
    page.window.min_height = 780
    page.padding = 0 
    
    vista = VistaMisDatos(page)
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)