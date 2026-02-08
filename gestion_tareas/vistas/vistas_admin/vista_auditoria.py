import flet as ft
from datetime import datetime
from gestion_tareas.servicios.db_manager import instancia_db

def VistaAuditoria(page):
    # configuracion de colores
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_SOMBRA_TARJETAS = "#30000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    
    # colores de accion
    COLOR_CREAR = "#4CAF50"
    COLOR_EDITAR = "#2196F3"
    COLOR_ELIMINAR = "#E53935"
    COLOR_LOGIN = "#9C27B0"
    COLOR_CONFIG = "#FF9800"

    # opciones para los filtros
    FILTROS_TIPO = ["Todos", "Crear", "Editar", "Eliminar", "Login", "Configuración"]
    FILTROS_MODULO = ["Todos", "Usuarios", "Tareas", "Equipos", "Departamentos", "Roles", "Sistema"]
    FILTROS_PERIODO = ["Hoy", "Últimos 7 días", "Todos"]

    filtro_tipo_actual = ["Todos"]
    filtro_modulo_actual = ["Todos"]
    filtro_periodo_actual = ["Todos"]

    # variable para almacenar registros reales de la bd
    registros_reales = []

    # logica para cargar datos de mongodb
    def cargar_datos_auditoria():
        nonlocal registros_reales
        try:
            # consultamos la coleccion auditoria ordenada por lo mas reciente
            cursor = instancia_db.obtener_instancia().auditoria.find().sort("_id", -1).limit(100)
            lista_raw = list(cursor)
            
            procesados = []
            for r in lista_raw:
                # formateamos la fecha para la interfaz
                fecha_dt = r.get("fecha_completa", datetime.now())
                
                procesados.append({
                    "accion": r.get("accion", "Info"),
                    "modulo": r.get("modulo", "Sistema"),
                    "descripcion": r.get("descripcion", "Sin descripción"),
                    "usuario": r.get("usuario", "Desconocido"),
                    "fecha": fecha_dt.strftime("%d/%m/%y") if isinstance(fecha_dt, datetime) else str(fecha_dt),
                    "hora": fecha_dt.strftime("%H:%M") if isinstance(fecha_dt, datetime) else "--:--",
                    "ip": r.get("ip", "0.0.0.0"),
                    "dt_objeto": fecha_dt # guardamos el objeto para filtros de fecha
                })
            registros_reales = procesados
        except Exception as e:
            print(f"error al cargar auditoria: {e}")
            registros_reales = []

    # funcion para refrescar la lista en la interfaz
    def actualizar_lista_ui():
        texto = input_busqueda.value.lower() if input_busqueda.value else ""
        ahora = datetime.now()
        
        filtrados = []
        for r in registros_reales:
            # filtro de texto
            if texto and texto not in r["descripcion"].lower() and texto not in r["usuario"].lower():
                continue
            
            # filtro de tipo
            if filtro_tipo_actual[0] != "Todos" and r["accion"] != filtro_tipo_actual[0]:
                continue
                
            # filtro de modulo
            if filtro_modulo_actual[0] != "Todos" and r["modulo"] != filtro_modulo_actual[0]:
                continue

            # filtro de periodo simple
            if filtro_periodo_actual[0] == "Hoy":
                if r["fecha"] != ahora.strftime("%d/%m/%y"):
                    continue

            filtrados.append(r)

        # repintamos la lista
        lista_registros.controls = []
        if not filtrados:
            lista_registros.controls.append(ft.Text("No hay registros que coincidan", color="grey", size=12))
        else:
            for reg in filtrados:
                lista_registros.controls.append(crear_tarjeta_registro(reg))
        
        contador_registros.value = f"{len(filtrados)} registros encontrados"
        page.update()

    # ejecucion de carga inicial
    cargar_datos_auditoria()

    async def btn_volver_click(e):
        await page.push_route("/area_admin")

    def btn_buscar_click(e):
        actualizar_lista_ui()

    def get_color_accion(accion):
        colores = {
            "Crear": COLOR_CREAR,
            "Editar": COLOR_EDITAR,
            "Eliminar": COLOR_ELIMINAR,
            "Login": COLOR_LOGIN,
            "Configuración": COLOR_CONFIG,
        }
        return colores.get(accion, COLOR_LABEL)

    def get_icono_accion(accion):
        iconos = {
            "Crear": "➕",
            "Editar": "✏️",
            "Eliminar": "🗑️",
            "Login": "🔐",
            "Configuración": "⚙️",
        }
        return iconos.get(accion, "📋")

    # dialog detalle
    def mostrar_detalle_registro(registro):
        color_accion = get_color_accion(registro["accion"])
        icono_accion = get_icono_accion(registro["accion"])
        
        dialog_detalle = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Text(icono_accion, size=20),
                ft.Container(
                    bgcolor=color_accion, border_radius=8,
                    padding=ft.Padding(left=8, right=8, top=2, bottom=2),
                    content=ft.Text(registro["accion"], size=11, color="white", weight="bold"),
                ),
                ft.Text(registro["modulo"], size=14, color=COLOR_LABEL),
            ], spacing=8),
            bgcolor="white",
            content=ft.Container(
                width=320,
                content=ft.Column([
                    ft.Column([ft.Text("Descripción", size=11, color=COLOR_LABEL), ft.Text(registro["descripcion"], size=12, color="black")], spacing=2),
                    ft.Divider(height=1, color=COLOR_BORDE),
                    ft.Row([
                        ft.Column([ft.Text("Usuario", size=11, color=COLOR_LABEL), ft.Text(registro["usuario"], size=12, color="black")], spacing=2),
                        ft.Column([ft.Text("Fecha y hora", size=11, color=COLOR_LABEL), ft.Text(f"{registro['fecha']} {registro['hora']}", size=12, color="black")], horizontal_alignment="end"),
                    ], alignment="spaceBetween"),
                    ft.Column([ft.Text("Dirección IP", size=11, color=COLOR_LABEL), ft.Text(registro["ip"], size=12, color="black")], spacing=2),
                ], spacing=12, tight=True)
            ),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog(dialog_detalle))],
            actions_alignment="end",
        )
        page.overlay.append(dialog_detalle)
        dialog_detalle.open = True
        page.update()

    def cerrar_dialog(dialog):
        dialog.open = False
        page.update()

    # dialog filtros
    def mostrar_dialog_filtros(e):
        radio_tipo = ft.RadioGroup(
            value=filtro_tipo_actual[0],
            content=ft.Column([ft.Radio(value=t, label=t, label_style=ft.TextStyle(color="black", size=12)) for t in FILTROS_TIPO], spacing=2)
        )
        radio_periodo = ft.RadioGroup(
            value=filtro_periodo_actual[0],
            content=ft.Column([ft.Radio(value=p, label=p, label_style=ft.TextStyle(color="black", size=12)) for p in FILTROS_PERIODO], spacing=2)
        )

        def aplicar(e):
            filtro_tipo_actual[0] = radio_tipo.value
            filtro_periodo_actual[0] = radio_periodo.value
            dialog_filtros.open = False
            actualizar_lista_ui()

        dialog_filtros = ft.AlertDialog(
            title=ft.Text("Filtrar auditoría", size=16, weight="bold", color="black"),
            bgcolor="white",
            content=ft.Container(
                width=300, height=350,
                content=ft.Column([
                    ft.Text("Tipo de Acción:", size=13, weight="bold", color=COLOR_LABEL), radio_tipo,
                    ft.Divider(),
                    ft.Text("Período:", size=13, weight="bold", color=COLOR_LABEL), radio_periodo,
                ], scroll="auto")
            ),
            actions=[ft.TextButton("Aplicar", on_click=aplicar)],
        )
        page.overlay.append(dialog_filtros)
        dialog_filtros.open = True
        page.update()

    # constructor de tarjetas
    def crear_tarjeta_registro(reg):
        color_acc = get_color_accion(reg["accion"])
        return ft.Container(
            bgcolor="white", border_radius=10, padding=10, margin=ft.Margin(bottom=8, top=0, left=0, right=0),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=4, color=COLOR_SOMBRA_TARJETAS, offset=ft.Offset(0, 2)),
            on_click=lambda e: mostrar_detalle_registro(reg), ink=True,
            content=ft.Row([
                ft.Column([
                    ft.Text(get_icono_accion(reg["accion"]), size=18),
                    ft.Container(bgcolor=color_acc, border_radius=6, padding=ft.Padding(left=5, right=5, top=1, bottom=1),
                                content=ft.Text(reg["accion"][:4].upper(), size=8, color="white", weight="bold")),
                ], horizontal_alignment="center", spacing=3),
                ft.Column([
                    ft.Text(reg["descripcion"], size=11, color="black", weight="w500", max_lines=2, overflow="ellipsis"),
                    ft.Row([
                        ft.Text(f"👤 {reg['usuario']}", size=9, color="#666666"),
                        ft.Text(f"{reg['fecha']} {reg['hora']}", size=9, color=COLOR_LABEL),
                    ], alignment="spaceBetween"),
                ], expand=True, spacing=2)
            ], spacing=10, vertical_alignment="start")
        )

    # elementos de ui
    input_busqueda = ft.TextField(
        hint_text="Buscar en auditoría...", border_color=COLOR_BORDE, border_radius=5, height=38, expand=True,
        text_size=12, content_padding=ft.Padding(left=10, right=10), on_submit=btn_buscar_click
    )

    btn_filtrar = ft.Container(
        content=ft.Text("Filtrar", size=11, color="black"),
        bgcolor="white", border=ft.Border(
            top=ft.BorderSide(1, COLOR_BORDE), 
            bottom=ft.BorderSide(1, COLOR_BORDE), 
            left=ft.BorderSide(1, COLOR_BORDE), 
            right=ft.BorderSide(1, COLOR_BORDE)
        ), border_radius=5,
        padding=ft.Padding(left=12, right=12, top=8, bottom=8), on_click=mostrar_dialog_filtros, ink=True
    )

    btn_buscar = ft.Container(
        content=ft.Icon(ft.Icons.SEARCH, size=20, color="white"),
        bgcolor=COLOR_LABEL, border_radius=5, padding=8, on_click=btn_buscar_click, ink=True
    )

    contador_registros = ft.Text("Cargando registros...", size=11, color=COLOR_LABEL)
    lista_registros = ft.ListView(spacing=0, expand=True)

    # diseño de la tarjeta blanca
    tarjeta_blanca = ft.Container(
        width=380, bgcolor="white", border_radius=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color=COLOR_SOMBRA, offset=ft.Offset(0, 5)),
        content=ft.Container(
            padding=ft.Padding(left=18, right=18, top=55, bottom=20),
            content=ft.Column([
                ft.Row([input_busqueda, btn_filtrar, btn_buscar], spacing=8),
                contador_registros,
                ft.Container(height=450, content=lista_registros),
            ], spacing=10)
        )
    )

    header_flotante = ft.Container(
        width=200, height=50, bgcolor=COLOR_HEADER_BG, border_radius=25, alignment=ft.Alignment(0, 0),
        content=ft.Text("AUDITORÍA", size=18, weight="bold", color="white")
    )

    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight="bold"),
        on_click=btn_volver_click, top=10, left=10, padding=10
    )

    # carga final de la ui
    actualizar_lista_ui()

    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[COLOR_FONDO_TOP, COLOR_FONDO_BOT]),
        content=ft.Stack([
            ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=ft.Stack([
                ft.Container(content=tarjeta_blanca, top=30),
                ft.Container(content=header_flotante, top=0, left=90)
            ], width=380, height=620)),
            btn_volver
        ])
    )