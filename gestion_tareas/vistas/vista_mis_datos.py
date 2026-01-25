import flet as ft

def VistaMisDatos(page: ft.Page):
    
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#66000000"
    COLOR_LABEL = "#5B9BD5"

    #datos de usuario de ejemplo, ya se sustituirá por datos reales cuando haya backend
    usuario = {
        "nombre": "Rubén",
        "apellidos": "Doblas Gundersen",
        "estado": "ACTIVO",
        "identificador": "12345678A",
        "empresa": "TechSolutions S.L",
        "equipo": "Cloud Infrastructure & DevOps",
        "cargo": "Senior Software Engineer",
        "id_empleado": "XXXXXX",
        "correo": "j.perez@techsolutions.com",
        "telefono": "+34 912 345 678 (Ext. 402)",
        "ubicacion": "Oficina Central - Madrid (Torre A)",
        "fecha_incorporacion": "15/03/2021",
        "foto_url": None  #reemplazar con URL real o ruta de imagen
    }

    def crear_campo(label: str, valor: str):
        return ft.Column(
            spacing=2,
            controls=[
                ft.Text(label, size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                ft.Text(valor, size=14, color="black", weight=ft.FontWeight.BOLD),
            ]
        )

    def btn_volver_click(e):
        #hay que implementar la navegación real
        page.snack_bar = ft.SnackBar(ft.Text("Volver atrás"))
        page.snack_bar.open = True
        page.update()

    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight=ft.FontWeight.BOLD),
        on_click=btn_volver_click,
        ink=True,
        padding=10,
    )

    #foto, tambien cambiar cuando haya backend
    foto_perfil = ft.Container(
        width=100,
        height=100,
        border_radius=10,
        bgcolor="#E0E0E0",
        content=ft.Image(
            src=usuario["foto_url"] if usuario["foto_url"] else "https://via.placeholder.com/100",
            width=100,
            height=100,
            fit=ft.ImageFit.COVER,
            border_radius=10,
        ) if usuario["foto_url"] else ft.Icon("person", size=50, color="#999999")
    )

    #estado con punto verde o rojo
    estado_activo = usuario["estado"] == "ACTIVO"
    estado_widget = ft.Row(
        spacing=5,
        controls=[
            ft.Text(usuario["estado"], size=14, color="black", weight=ft.FontWeight.BOLD),
            ft.Container(
                width=12,
                height=12,
                border_radius=6,
                bgcolor="#4CAF50" if estado_activo else "#F44336",
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
                            ft.Text(usuario["nombre"], size=14, color="black", weight=ft.FontWeight.BOLD),
                        ]
                    ),
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text("Apellidos", size=12, color=COLOR_LABEL, weight=ft.FontWeight.W_500),
                            ft.Text(usuario["apellidos"], size=14, color="black", weight=ft.FontWeight.BOLD),
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
                    crear_campo("Identificador", usuario["identificador"]),
                    crear_campo("Empresa", usuario["empresa"]),
                    crear_campo("Equipo", usuario["equipo"]),
                    crear_campo("Cargo", usuario["cargo"]),
                    crear_campo("ID Empleado", usuario["id_empleado"]),
                    crear_campo("Correo corporativo", usuario["correo"]),
                    crear_campo("Teléfono", usuario["telefono"]),
                    crear_campo("Ubicación", usuario["ubicacion"]),
                    crear_campo("Fecha de Incorporación", usuario["fecha_incorporacion"]),
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