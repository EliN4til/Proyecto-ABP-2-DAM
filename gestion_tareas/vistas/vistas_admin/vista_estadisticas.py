import flet as ft
from datetime import datetime
from modelos.crud import obtener_todas_tareas, obtener_todos_empleados, obtener_todos_departamentos

def VistaEstadisticas(page):
    # configuracion de colores del tema
    COLOR_FONDO_TOP = "#152060"      
    COLOR_FONDO_BOT = "#4FC3F7"      
    COLOR_HEADER_BG = "#1F2855"      
    COLOR_SOMBRA = "#40000000"
    COLOR_LABEL = "#5B9BD5"
    COLOR_BORDE = "#E0E0E0"
    
    # colores para metricas
    COLOR_USUARIOS = "#4CAF50"
    COLOR_TAREAS = "#2196F3"
    COLOR_PENDIENTES = "#FF9800"
    COLOR_COMPLETADAS = "#8BC34A"
    COLOR_ATRASADAS = "#F44336"
    COLOR_DEPARTAMENTOS = "#9C27B0"

    # variables de estado para datos reales
    datos_db = {
        "usuarios": [],
        "tareas": [],
        "tareas_pendientes": [],
        "tareas_completadas": [],
        "tareas_atrasadas": [],
        "departamentos": [],
        "ranking": [],
        "productividad": 0,
        "promedio_tareas": 0
    }

    # funcion para procesar toda la info de la bd con seguridad de tipos
    def procesar_datos_reales():
        nonlocal datos_db
        ahora = datetime.now()
        
        # obtenemos colecciones
        exito_u, lista_u = obtener_todos_empleados()
        exito_t, lista_t = obtener_todas_tareas()
        exito_d, lista_d = obtener_todos_departamentos()

        if exito_u: datos_db["usuarios"] = lista_u
        if exito_d: datos_db["departamentos"] = lista_d

        if exito_t:
            datos_db["tareas"] = lista_t
            pendientes = []
            completadas = []
            atrasadas = []
            conteo_ranking = {}

            for t in lista_t:
                # validamos que t sea un diccionario
                if not isinstance(t, dict): continue
                
                estado = t.get("estado", "pendiente")
                
                # clasificacion por estado
                if estado == "completada":
                    completadas.append(t)
                    # ranking de productividad
                    asignados = t.get("asignados", [])
                    if isinstance(asignados, list):
                        for asig in asignados:
                            if isinstance(asig, dict):
                                nom = asig.get("nombre", "Usuario")
                                conteo_ranking[nom] = conteo_ranking.get(nom, 0) + 1
                else:
                    pendientes.append(t)
                    # verificamos atraso por fecha
                    f_limite = t.get("fecha_limite")
                    if f_limite and isinstance(f_limite, datetime) and f_limite < ahora:
                        diff = ahora - f_limite
                        t["dias_atraso_calculado"] = diff.days
                        atrasadas.append(t)

            datos_db["tareas_pendientes"] = pendientes
            datos_db["tareas_completadas"] = completadas
            datos_db["tareas_atrasadas"] = atrasadas
            
            # metricas de resumen
            total = len(lista_t)
            if total > 0:
                datos_db["productividad"] = int((len(completadas) / total) * 100)
                if exito_u and len(lista_u) > 0:
                    datos_db["promedio_tareas"] = round(total / len(lista_u), 1)
            
            # ordenamos el ranking top 5
            datos_db["ranking"] = sorted(conteo_ranking.items(), key=lambda x: x[1], reverse=True)[:5]

    # carga inicial de datos
    procesar_datos_reales()

    async def btn_volver_click(e):
        # navegacion al dashboard
        await page.push_route("/area_admin")

    # dialogos de detalle
    def mostrar_dialog_usuarios(e):
        lista_items = []
        for u in datos_db["usuarios"]:
            if not isinstance(u, dict): continue
            item = ft.Container(
                padding=8,
                border=ft.Border(bottom=ft.BorderSide(1, COLOR_BORDE)),
                content=ft.Row([
                    ft.Row([
                        ft.Text("👤", size=16),
                        ft.Column([
                            ft.Text(f"{u.get('nombre', 'N/A')} {u.get('apellidos', '')}", size=12, color="black", weight="bold"),
                            ft.Text(u.get("cargo", "Empleado"), size=10, color=COLOR_LABEL),
                        ], spacing=0)
                    ], spacing=10),
                    ft.Text(u.get("id_empleado", "N/A"), size=10, color="#666666"),
                ], alignment="spaceBetween")
            )
            lista_items.append(item)
        abrir_modal("👥 Usuarios Registrados", lista_items)

    def mostrar_dialog_tareas_totales(e):
        lista_items = []
        for t in datos_db["tareas"]:
            if not isinstance(t, dict): continue
            item = ft.Container(
                padding=8,
                border=ft.Border(bottom=ft.BorderSide(1, COLOR_BORDE)),
                content=ft.Row([
                    ft.Column([
                        ft.Text(t.get("titulo", "Sin título"), size=11, color="black", weight="bold", max_lines=1),
                        ft.Text(t.get("proyecto", "General"), size=10, color=COLOR_LABEL),
                    ], expand=True, spacing=0),
                    ft.Container(
                        bgcolor=COLOR_COMPLETADAS if t.get("estado")=="completada" else COLOR_PENDIENTES,
                        border_radius=8, padding=ft.Padding(left=6, right=6, top=2, bottom=2),
                        content=ft.Text(t.get("estado", "pendiente"), size=9, color="white")
                    )
                ], alignment="spaceBetween")
            )
            lista_items.append(item)
        abrir_modal("📋 Historial de Tareas", lista_items)

    def mostrar_dialog_pendientes(e):
        lista_items = []
        for t in datos_db["tareas_pendientes"]:
            # extraccion segura del nombre del primer asignado
            nombre_asig = "Sin asignar"
            asigs = t.get("asignados", [])
            if isinstance(asigs, list) and len(asigs) > 0:
                if isinstance(asigs[0], dict):
                    nombre_asig = asigs[0].get("nombre", "N/A")

            item = ft.Container(
                padding=8,
                border=ft.Border(bottom=ft.BorderSide(1, COLOR_BORDE)),
                content=ft.Column([
                    ft.Text(t.get("titulo", "Tarea"), size=11, color="black", weight="bold"),
                    ft.Row([
                        ft.Text(f"👤 {nombre_asig}", size=10, color="#666666"),
                        ft.Text(f"📅 {str(t.get('fecha_limite', 'S/F'))[:10]}", size=10, color=COLOR_PENDIENTES),
                    ], alignment="spaceBetween")
                ], spacing=3)
            )
            lista_items.append(item)
        abrir_modal("⏳ Tareas Pendientes", lista_items)

    def mostrar_dialog_completadas(e):
        lista_items = []
        for t in datos_db["tareas_completadas"]:
            item = ft.Container(
                padding=8,
                border=ft.Border(bottom=ft.BorderSide(1, COLOR_BORDE)),
                content=ft.Column([
                    ft.Text(t.get("titulo", "Tarea"), size=11, color="black", weight="bold"),
                    ft.Row([
                        ft.Text(f"✅ Finalizada", size=10, color=COLOR_COMPLETADAS),
                        ft.Text(str(t.get("fecha_completado", t.get("fecha_limite")))[:10], size=10, color="#666666"),
                    ], alignment="spaceBetween")
                ], spacing=3)
            )
            lista_items.append(item)
        abrir_modal("✅ Tareas Completadas", lista_items)

    def mostrar_dialog_atrasadas(e):
        lista_items = []
        for t in datos_db["tareas_atrasadas"]:
            item = ft.Container(
                padding=8,
                border=ft.Border(bottom=ft.BorderSide(1, COLOR_BORDE)),
                content=ft.Column([
                    ft.Text(t.get("titulo", "Tarea"), size=11, color="black", weight="bold"),
                    ft.Row([
                        ft.Text(f"⚠️ {t.get('dias_atraso_calculado', 1)} días de atraso", size=10, color=COLOR_ATRASADAS),
                        ft.Text(f"Venció: {str(t.get('fecha_limite', 'S/F'))[:10]}", size=10, color="#666666"),
                    ], alignment="spaceBetween")
                ], spacing=3)
            )
            lista_items.append(item)
        abrir_modal("⚠️ Tareas Atrasadas", lista_items)

    def mostrar_dialog_departamentos_tarjeta(e):
        lista_items = []
        for d in datos_db["departamentos"]:
            item = ft.Container(
                padding=8,
                border=ft.Border(bottom=ft.BorderSide(1, COLOR_BORDE)),
                content=ft.Row([
                    ft.Column([
                        ft.Text(d.get("nombre", "Departamento"), size=12, color="black", weight="bold"),
                        ft.Text(f"Responsable: {d.get('responsable', 'No asignado')}", size=10, color=COLOR_LABEL),
                    ], spacing=0),
                    ft.Container(bgcolor=COLOR_DEPARTAMENTOS, border_radius=10, padding=ft.Padding(left=8, right=8, top=2, bottom=2),
                                content=ft.Text(f"{len(d.get('miembros', []))} 👥", size=10, color="white"))
                ], alignment="spaceBetween")
            )
            lista_items.append(item)
        abrir_modal("🏢 Departamentos Activos", lista_items)

    def abrir_modal(titulo, items):
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(titulo, size=16, weight="bold", color="black"),
            bgcolor="white",
            content=ft.Container(width=320, height=350, content=ft.ListView(controls=items, spacing=0)),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog(dialog))],
            actions_alignment="end"
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def cerrar_dialog(dialog):
        dialog.open = False
        page.update()

    # constructores de componentes graficos
    def crear_tarjeta_metrica(titulo, valor, icono, color, subtitulo, on_click):
        return ft.Container(
            width=155, height=90, bgcolor="white", border_radius=12, border=ft.Border(
                top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), 
                left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)
            ),
            padding=12, ink=True, on_click=on_click,
            content=ft.Column([
                ft.Row([ft.Text(icono, size=24), ft.Text(valor, size=22, color=color, weight="bold")], alignment="spaceBetween"),
                ft.Text(titulo, size=11, color="black", weight="bold"),
                ft.Text(subtitulo, size=9, color="#888888"),
            ], spacing=5)
        )

    def crear_barra_progreso(label, valor, total, color):
        porcentaje = (valor / total) if total > 0 else 0
        return ft.Column([
            ft.Row([ft.Text(label, size=11, color="black"), ft.Text(f"{valor}/{total}", size=11, color=COLOR_LABEL)], alignment="spaceBetween"),
            ft.Container(height=8, border_radius=4, bgcolor="#E0E0E0", content=ft.Container(width=porcentaje*320, height=8, border_radius=4, bgcolor=color))
        ], spacing=3)

    def crear_item_ranking(pos, nombre, tareas):
        return ft.Container(
            padding=ft.Padding(top=5, bottom=5),
            content=ft.Row([
                ft.Row([
                    ft.Container(width=24, height=24, border_radius=12, bgcolor=COLOR_LABEL if pos <= 3 else "#E0E0E0",
                                alignment=ft.Alignment(0,0), content=ft.Text(str(pos), size=11, color="white" if pos<=3 else "black", weight="bold")),
                    ft.Text("👩‍💻" if pos%2==0 else "👨‍💻", size=16),
                    ft.Text(nombre, size=12, color="black"),
                ], spacing=10),
                ft.Container(bgcolor=COLOR_COMPLETADAS, border_radius=10, padding=ft.Padding(left=8, right=8, top=2, bottom=2),
                            content=ft.Text(f"{tareas} tareas", size=10, color="white", weight="bold")),
            ], alignment="spaceBetween")
        )

    # ensamblaje de la interfaz de usuario
    seccion_metricas = ft.Column([
        ft.Row([
            crear_tarjeta_metrica("Usuarios Activos", str(len(datos_db["usuarios"])), "👥", COLOR_USUARIOS, "Registrados", mostrar_dialog_usuarios),
            crear_tarjeta_metrica("Total Tareas", str(len(datos_db["tareas"])), "📋", COLOR_TAREAS, "Histórico", mostrar_dialog_tareas_totales),
        ], alignment="center", spacing=10),
        ft.Row([
            crear_tarjeta_metrica("Pendientes", str(len(datos_db["tareas_pendientes"])), "⏳", COLOR_PENDIENTES, "Por hacer", mostrar_dialog_pendientes),
            crear_tarjeta_metrica("Completadas", str(len(datos_db["tareas_completadas"])), "✅", COLOR_COMPLETADAS, f"{datos_db['productividad']}% éxito", mostrar_dialog_completadas),
        ], alignment="center", spacing=10),
        ft.Row([
            crear_tarjeta_metrica("Atrasadas", str(len(datos_db["tareas_atrasadas"])), "⚠️", COLOR_ATRASADAS, "Vencidas", mostrar_dialog_atrasadas),
            crear_tarjeta_metrica("Departamentos", str(len(datos_db["departamentos"])), "🏢", COLOR_DEPARTAMENTOS, "Activos", mostrar_dialog_departamentos_tarjeta),
        ], alignment="center", spacing=10),
    ], spacing=10)

    # carga por departamentos (calculo real basado en usuarios asignados)
    items_departamentos = []
    total_t = len(datos_db["tareas"])
    for d in datos_db["departamentos"]:
        if not isinstance(d, dict): continue
        conteo = 0
        for t in datos_db["tareas"]:
            # verificamos el primer asignado de la tarea
            asigs = t.get("asignados", [])
            if isinstance(asigs, list) and len(asigs) > 0:
                primer_asig = asigs[0]
                if isinstance(primer_asig, dict):
                    id_u = primer_asig.get("id_usuario")
                    # buscamos al usuario para ver su departamento
                    for u in datos_db["usuarios"]:
                        if str(u.get("_id")) == str(id_u):
                            # comprobamos si el departamento coincide (puede ser dict o str)
                            dep_data = u.get("departamento")
                            nombre_dep_usuario = ""
                            if isinstance(dep_data, dict):
                                nombre_dep_usuario = dep_data.get("nombre")
                            elif isinstance(dep_data, str):
                                nombre_dep_usuario = dep_data
                            
                            if nombre_dep_usuario == d.get("nombre"):
                                conteo += 1
                                break
        if conteo > 0:
            items_departamentos.append(crear_barra_progreso(d.get("nombre", "Dep"), conteo, total_t, COLOR_TAREAS))

    seccion_departamentos = ft.Container(
        bgcolor="white", border_radius=12, border=ft.Border(
            top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), 
            left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)
        ), padding=15,
        content=ft.Column([
            ft.Text("Tareas por Departamento", size=13, color="black", weight="bold"),
            *(items_departamentos if items_departamentos else [ft.Text("Sin datos de asignación", size=11, color="grey")])
        ], spacing=10)
    )

    seccion_ranking = ft.Container(
        bgcolor="white", border_radius=12, border=ft.Border(
            top=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), 
            left=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)
        ), padding=15,
        content=ft.Column([
            ft.Text("🏆 Top Usuarios del Mes", size=13, color="black", weight="bold"),
            ft.Divider(height=1, color=COLOR_BORDE),
            *[crear_item_ranking(i+1, r[0], r[1]) for i, r in enumerate(datos_db["ranking"])]
        ], spacing=5)
    )

    seccion_resumen = ft.Container(
        bgcolor="#F5F8FF", border_radius=12, padding=12,
        content=ft.Column([
            ft.Text("📊 Resumen Rápido", size=12, color="black", weight="bold"),
            ft.Row([ft.Text("Productividad media:", size=11, color="#666666"), ft.Text(f"{datos_db['productividad']}%", size=11, color=COLOR_COMPLETADAS, weight="bold")], alignment="spaceBetween"),
            ft.Row([ft.Text("Promedio tareas/usu:", size=11, color="#666666"), ft.Text(str(datos_db["promedio_tareas"]), size=11, color=COLOR_TAREAS, weight="bold")], alignment="spaceBetween"),
        ], spacing=8)
    )

    # contenedor principal con scroll
    contenido_scroll = ft.Column(
        spacing=15, scroll="auto",
        controls=[seccion_metricas, seccion_departamentos, seccion_ranking, seccion_resumen]
    )

    tarjeta_blanca = ft.Container(
        width=380, bgcolor="white", border_radius=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color=COLOR_SOMBRA, offset=ft.Offset(0, 5)),
        content=ft.Container(
            padding=ft.Padding(left=18, right=18, top=55, bottom=20),
            content=ft.Container(height=580, content=contenido_scroll)
        )
    )

    header_flotante = ft.Container(
        width=220, height=50, bgcolor=COLOR_HEADER_BG, border_radius=25, alignment=ft.Alignment(0, 0),
        content=ft.Text("ESTADÍSTICAS", size=18, weight="bold", color="white")
    )

    btn_volver = ft.Container(
        content=ft.Text("←", size=24, color="white", weight="bold"),
        on_click=btn_volver_click, ink=True, padding=10
    )

    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[COLOR_FONDO_TOP, COLOR_FONDO_BOT]),
        content=ft.Stack([
            ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=ft.Stack([
                ft.Container(content=tarjeta_blanca, top=30),
                ft.Container(content=header_flotante, top=0, left=80)
            ], width=380, height=700)),
            ft.Container(content=btn_volver, top=10, left=10)
        ])
    )