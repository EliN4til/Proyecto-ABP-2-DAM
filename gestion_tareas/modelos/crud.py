from bson import ObjectId
from datetime import datetime
from modelos.init import (
    db, 
    EmpleadoModel, 
    DepartamentoModel, 
    ProyectoModel, 
    TareaModel, 
    RolModel
)
from pydantic import ValidationError


# ========== FUNCIONES AUXILIARES ==========

def es_id_valido(id_str):
    #comprueba si el id es valido para mongodb
    try:
        ObjectId(id_str)
        return True
    except:
        return False


def registrar_log(accion, modulo, descripcion, usuario="Sistema"):
    #guarda un log de lo que se hace en la app
    try:
        log = {
            "accion": accion,
            "modulo": modulo,
            "descripcion": descripcion,
            "usuario": usuario,
            "fecha_completa": datetime.now(),
            "ip": "127.0.0.1"
        }
        db.auditoria.insert_one(log)
    except Exception as e:
        print("error guardando log:", e)


# ========== EMPLEADOS ==========

def crear_empleado(datos):
    #crea un empleado nuevo
    try:
        # Validacion con Pydantic
        empleado = EmpleadoModel(**datos)
        
        # Insertar usando el dump del modelo
        resultado = db.empleados.insert_one(empleado.model_dump(by_alias=True, exclude=["id"]))
        datos["_id"] = str(resultado.inserted_id)
        
        registrar_log("Crear", "Usuarios", "usuario registrado: " + datos["nombre"])
        return (True, datos)
    except ValidationError as e:
        return (False, str(e))
    except Exception as e:
        return (False, str(e))


def obtener_empleado(id_empleado):
    #busca un empleado por su id
    if not es_id_valido(id_empleado):
        return (False, "id no valido")
    
    empleado = db.empleados.find_one({"_id": ObjectId(id_empleado)})
    if empleado:
        empleado["_id"] = str(empleado["_id"])
        return (True, empleado)
    return (False, "empleado no encontrado")


def obtener_empleado_por_email(email):
    #busca un empleado por email
    empleado = db.empleados.find_one({"email": email})
    if empleado:
        empleado["_id"] = str(empleado["_id"])
        return (True, empleado)
    return (False, "empleado no encontrado")


def obtener_todos_empleados():
    #devuelve todos los empleados
    try:
        empleados = list(db.empleados.find())
        for emp in empleados:
            emp["_id"] = str(emp["_id"])
        return (True, empleados)
    except Exception as e:
        return (False, str(e))


def actualizar_empleado(id_empleado, datos):
    #actualiza un empleado
    if not es_id_valido(id_empleado):
        return (False, "id no valido")
    
    try:
        resultado = db.empleados.update_one(
            {"_id": ObjectId(id_empleado)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            registrar_log("Editar", "Usuarios", "usuario actualizado id: " + id_empleado)
            return (True, "empleado actualizado")
        return (False, "no se encontro el empleado")
    except Exception as e:
        return (False, str(e))


def eliminar_empleado(id_empleado):
    #borra un empleado
    if not es_id_valido(id_empleado):
        return (False, "id no valido")
    
    try:
        #pillamos el nombre antes de borrar para el log
        emp = db.empleados.find_one({"_id": ObjectId(id_empleado)})
        if emp:
            nombre = emp["nombre"] + " " + emp["apellidos"]
        else:
            nombre = id_empleado
        
        resultado = db.empleados.delete_one({"_id": ObjectId(id_empleado)})
        if resultado.deleted_count > 0:
            registrar_log("Eliminar", "Usuarios", "usuario eliminado: " + nombre)
            return (True, "empleado eliminado")
        return (False, "no se encontro el empleado")
    except Exception as e:
        return (False, str(e))


# ========== DEPARTAMENTOS ==========

def crear_departamento(datos):
    #crea un departamento
    try:
        # Validacion con Pydantic
        depto = DepartamentoModel(**datos)
        
        resultado = db.departamentos.insert_one(depto.model_dump(by_alias=True, exclude=["id"]))
        datos["_id"] = str(resultado.inserted_id)
        
        registrar_log("Crear", "Departamentos", f"departamento creado: {datos['nombre']}")
        return (True, datos)
    except ValidationError as e:
        return (False, str(e))
    except Exception as e:
        return (False, str(e))


def obtener_departamento(id_departamento):
    #busca un departamento por id
    if not es_id_valido(id_departamento):
        return (False, "id no valido")
    
    depto = db.departamentos.find_one({"_id": ObjectId(id_departamento)})
    if depto:
        depto["_id"] = str(depto["_id"])
        return (True, depto)
    return (False, "departamento no encontrado")


def obtener_todos_departamentos():
    #devuelve todos los departamentos
    try:
        deptos = list(db.departamentos.find())
        for d in deptos:
            d["_id"] = str(d["_id"])
        return (True, deptos)
    except Exception as e:
        return (False, str(e))


def actualizar_departamento(id_departamento, datos):
    #actualiza un departamento
    if not es_id_valido(id_departamento):
        return (False, "id no valido")
    
    try:
        resultado = db.departamentos.update_one(
            {"_id": ObjectId(id_departamento)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            registrar_log("Editar", "Departamentos", "departamento actualizado")
            return (True, "departamento actualizado")
        return (False, "no se encontro el departamento")
    except Exception as e:
        return (False, str(e))


def eliminar_departamento(id_departamento):
    #borra un departamento
    if not es_id_valido(id_departamento):
        return (False, "id no valido")
    
    try:
        resultado = db.departamentos.delete_one({"_id": ObjectId(id_departamento)})
        if resultado.deleted_count > 0:
            registrar_log("Eliminar", "Departamentos", "departamento borrado")
            return (True, "departamento eliminado")
        return (False, "no se encontro el departamento")
    except Exception as e:
        return (False, str(e))


# ========== EQUIPOS ==========

def crear_equipo(datos):
    #crea un equipo nuevo
    try:
        if "nombre" not in datos or not datos["nombre"]:
            return (False, "el nombre es obligatorio")
        
        resultado = db.equipos.insert_one(datos)
        datos["_id"] = str(resultado.inserted_id)
        
        registrar_log("Crear", "Equipos", "equipo creado: " + datos["nombre"])
        return (True, datos)
    except Exception as e:
        return (False, str(e))


def obtener_equipo(id_equipo):
    #busca un equipo por id
    if not es_id_valido(id_equipo):
        return (False, "id no valido")
    
    equipo = db.equipos.find_one({"_id": ObjectId(id_equipo)})
    if equipo:
        equipo["_id"] = str(equipo["_id"])
        return (True, equipo)
    return (False, "equipo no encontrado")


def obtener_todos_equipos():
    #devuelve todos los equipos
    try:
        equipos = list(db.equipos.find())
        for eq in equipos:
            eq["_id"] = str(eq["_id"])
        return (True, equipos)
    except Exception as e:
        return (False, str(e))


def actualizar_equipo(id_equipo, datos):
    #actualiza un equipo
    if not es_id_valido(id_equipo):
        return (False, "id no valido")
    
    try:
        resultado = db.equipos.update_one(
            {"_id": ObjectId(id_equipo)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            registrar_log("Editar", "Equipos", "equipo editado")
            return (True, "equipo actualizado")
        return (False, "no se encontro el equipo")
    except Exception as e:
        return (False, str(e))


def eliminar_equipo(id_equipo):
    #borra un equipo
    if not es_id_valido(id_equipo):
        return (False, "id no valido")
    
    try:
        resultado = db.equipos.delete_one({"_id": ObjectId(id_equipo)})
        if resultado.deleted_count > 0:
            registrar_log("Eliminar", "Equipos", "equipo eliminado")
            return (True, "equipo eliminado")
        return (False, "no se encontro el equipo")
    except Exception as e:
        return (False, str(e))


# ========== PROYECTOS ==========

def crear_proyecto(datos):
    #crea un proyecto nuevo
    try:
        # Validacion con Pydantic
        proyecto = ProyectoModel(**datos)
        
        resultado = db.proyectos.insert_one(proyecto.model_dump(by_alias=True, exclude=["id"]))
        datos["_id"] = str(resultado.inserted_id)
        
        registrar_log("Crear", "Proyectos", f"proyecto iniciado: {datos['nombre']}")
        return (True, datos)
    except ValidationError as e:
        return (False, str(e))
    except Exception as e:
        return (False, str(e))


def obtener_proyecto(id_proyecto):
    #busca un proyecto por id
    if not es_id_valido(id_proyecto):
        return (False, "id no valido")
    
    proyecto = db.proyectos.find_one({"_id": ObjectId(id_proyecto)})
    if proyecto:
        proyecto["_id"] = str(proyecto["_id"])
        return (True, proyecto)
    return (False, "proyecto no encontrado")


def obtener_todos_proyectos():
    #devuelve todos los proyectos
    try:
        proyectos = list(db.proyectos.find())
        for p in proyectos:
            p["_id"] = str(p["_id"])
        return (True, proyectos)
    except Exception as e:
        return (False, str(e))


def actualizar_proyecto(id_proyecto, datos):
    #actualiza un proyecto
    if not es_id_valido(id_proyecto):
        return (False, "id no valido")
    
    try:
        resultado = db.proyectos.update_one(
            {"_id": ObjectId(id_proyecto)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            registrar_log("Editar", "Proyectos", "proyecto actualizado")
            return (True, "proyecto actualizado")
        return (False, "no se encontro el proyecto")
    except Exception as e:
        return (False, str(e))


def eliminar_proyecto(id_proyecto):
    #borra un proyecto
    if not es_id_valido(id_proyecto):
        return (False, "id no valido")
    
    try:
        resultado = db.proyectos.delete_one({"_id": ObjectId(id_proyecto)})
        if resultado.deleted_count > 0:
            registrar_log("Eliminar", "Proyectos", "proyecto borrado")
            return (True, "proyecto eliminado")
        return (False, "no se encontro el proyecto")
    except Exception as e:
        return (False, str(e))


# ========== TAREAS ==========

def crear_tarea(datos):
    #crea una tarea nueva
    try:
        # Validacion con Pydantic
        tarea = TareaModel(**datos)
        
        resultado = db.tareas.insert_one(tarea.model_dump(by_alias=True, exclude=["id"]))
        datos["_id"] = str(resultado.inserted_id)
        
        registrar_log("Crear", "Tareas", "tarea creada: " + datos["titulo"])
        return (True, datos)
    except ValidationError as e:
        return (False, str(e))
    except Exception as e:
        return (False, str(e))


def obtener_tarea(id_tarea):
    #busca una tarea por id
    if not es_id_valido(id_tarea):
        return (False, "id no valido")
    
    tarea = db.tareas.find_one({"_id": ObjectId(id_tarea)})
    if tarea:
        tarea["_id"] = str(tarea["_id"])
        return (True, tarea)
    return (False, "tarea no encontrada")


def obtener_todas_tareas():
    #devuelve todas las tareas
    try:
        tareas = list(db.tareas.find())
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def obtener_tareas_por_estado(estado):
    #busca tareas por su estado (pendiente, completada, etc)
    try:
        tareas = list(db.tareas.find({"estado": estado}))
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def obtener_tareas_pendientes_usuario(id_usuario, nombre_usuario):
    #busca las tareas pendientes del usuario
    try:
        #buscamos tareas donde el usuario esta asignado O las creo el
        filtro = {
            "estado": "pendiente",
            "$or": [
                {"asignados.id_usuario": id_usuario},
                {"compartido_por": nombre_usuario}
            ]
        }
        tareas = list(db.tareas.find(filtro))
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def obtener_tareas_por_usuario(id_usuario):
    #busca las tareas asignadas a un usuario
    try:
        tareas = list(db.tareas.find({"asignados.id_usuario": id_usuario}))
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def obtener_tareas_atrasadas():
    #busca las tareas que estan atrasadas
    try:
        ahora = datetime.now()
        #buscamos tareas no completadas con fecha limite pasada
        filtro = {
            "estado": {"$ne": "completada"},
            "fecha_limite": {"$lt": ahora}
        }
        tareas = list(db.tareas.find(filtro))
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def actualizar_tarea(id_tarea, datos):
    #actualiza una tarea
    #convertimos a string por si viene como ObjectId
    if isinstance(id_tarea, ObjectId):
        id_str = str(id_tarea)
    else:
        id_str = id_tarea
    
    if not es_id_valido(id_str):
        return (False, "id no valido")
    
    try:
        datos["fecha_modificacion"] = datetime.now()
        
        resultado = db.tareas.update_one(
            {"_id": ObjectId(id_str)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            registrar_log("Editar", "Tareas", "tarea actualizada")
            return (True, "tarea actualizada")
        return (False, "no se encontro la tarea")
    except Exception as e:
        return (False, str(e))


def completar_tarea(id_tarea):
    #marca una tarea como completada
    datos = {
        "estado": "completada",
        "fecha_completado": datetime.now()
    }
    exito, msg = actualizar_tarea(id_tarea, datos)
    if exito:
        registrar_log("Editar", "Tareas", "tarea completada id: " + str(id_tarea))
    return (exito, msg)


def eliminar_tarea(id_tarea):
    #borra una tarea
    if not es_id_valido(id_tarea):
        return (False, "id no valido")
    
    try:
        resultado = db.tareas.delete_one({"_id": ObjectId(id_tarea)})
        if resultado.deleted_count > 0:
            registrar_log("Eliminar", "Tareas", "tarea borrada")
            return (True, "tarea eliminada")
        return (False, "no se encontro la tarea")
    except Exception as e:
        return (False, str(e))


# ========== ROLES ==========

def crear_rol(datos):
    #crea un rol nuevo
    try:
        # Validacion con Pydantic
        rol = RolModel(**datos)
        
        resultado = db.roles.insert_one(rol.model_dump(by_alias=True, exclude=["id"]))
        datos["_id"] = str(resultado.inserted_id)
        
        registrar_log("Crear", "Roles", "rol creado: " + datos["nombre"])
        return (True, datos)
    except ValidationError as e:
        return (False, str(e))
    except Exception as e:
        return (False, str(e))


def obtener_rol(id_rol):
    #busca un rol por id
    if not es_id_valido(id_rol):
        return (False, "id no valido")
    
    rol = db.roles.find_one({"_id": ObjectId(id_rol)})
    if rol:
        rol["_id"] = str(rol["_id"])
        return (True, rol)
    return (False, "rol no encontrado")


def obtener_todos_roles():
    #devuelve todos los roles
    try:
        roles = list(db.roles.find())
        for r in roles:
            r["_id"] = str(r["_id"])
        return (True, roles)
    except Exception as e:
        return (False, str(e))


def actualizar_rol(id_rol, datos):
    #actualiza un rol
    if not es_id_valido(id_rol):
        return (False, "id no valido")
    
    try:
        resultado = db.roles.update_one(
            {"_id": ObjectId(id_rol)},
            {"$set": datos}
        )
        if resultado.matched_count > 0:
            registrar_log("Editar", "Roles", f"rol actualizado id: {id_rol}")
            return (True, "rol actualizado")
        return (False, "no se encontro el rol")
    except Exception as e:
        return (False, str(e))


def eliminar_rol(id_rol):
    #borra un rol
    if not es_id_valido(id_rol):
        return (False, "id no válido")
    
    try:
        resultado = db.roles.delete_one({"_id": ObjectId(id_rol)})
        if resultado.deleted_count > 0:
            registrar_log("Eliminar", "Roles", f"rol eliminado id: {id_rol}")
            return (True, "rol eliminado")
        return (False, "no se encontro el rol")
    except Exception as e:
        return (False, str(e))


# ========== LOGIN ==========

def validar_login(email, contrasenya):
    #comprueba si el email y la contraseña son correctos
    if not email or not contrasenya:
        return (False, "email y contraseña son obligatorios")
    
    empleado = db.empleados.find_one({"email": email})
    
    if not empleado:
        registrar_log("Login", "Sistema", f"fallo de acceso: el email {email} no existe")
        return (False, "usuario no encontrado")
    
    if empleado["contrasenya"] != contrasenya:
        registrar_log("Login", "Sistema", f"fallo de acceso: contraseña incorrecta para el email {email}")
        return (False, "contraseña incorrecta")
    
    # login valido
    empleado["_id"] = str(empleado["_id"])
    registrar_log("Login", "Sistema", f"sesión iniciada correctamente con el email: {email}")
    return (True, empleado)


def cambiar_contrasenya(id_empleado, contrasenya_actual, contrasenya_nueva):
    #cambia la contraseña de un empleado
    exito, resultado = obtener_empleado(id_empleado)
    
    if not exito:
        return (False, "empleado no encontrado")
    
    if resultado["contrasenya"] != contrasenya_actual:
        return (False, "la contraseña actual no es correcta")
    
    exito_upd, msg = actualizar_empleado(id_empleado, {"contrasenya": contrasenya_nueva})
    if exito_upd:
        registrar_log("Editar", "Usuarios", f"contraseña cambiada para id: {id_empleado}")
    return (exito_upd, msg)


# ========== FILTRAR Y ORDENAR TAREAS ==========

def filtrar_tareas(tareas, filtros, texto_busqueda=""):
    #filtra las tareas segun los criterios que le pasemos
    resultado = []
    
    for tarea in tareas:
        incluir = True
        
        #filtro por texto de busqueda
        if texto_busqueda:
            texto = texto_busqueda.lower()
            titulo = tarea.get("titulo", "").lower()
            proyecto = tarea.get("proyecto", "").lower()
            if texto not in titulo and texto not in proyecto:
                incluir = False
        
        #filtro por prioridad
        filtro_prioridad = filtros.get("prioridad", "Todas")
        if filtro_prioridad != "Todas":
            prioridad_tarea = tarea.get("prioridad", "").lower()
            prioridad_filtro = filtro_prioridad.lower()
            if prioridad_tarea != prioridad_filtro:
                incluir = False
        
        #filtro por tag
        filtro_tag = filtros.get("tag", "Todos")
        if filtro_tag != "Todos":
            if tarea.get("tag") != filtro_tag:
                incluir = False
        
        #filtro por proyecto
        filtro_proyecto = filtros.get("proyecto", "Todos")
        if filtro_proyecto != "Todos":
            if tarea.get("proyecto") != filtro_proyecto:
                incluir = False
        
        #si pasa todos los filtros la añadimos
        if incluir:
            resultado.append(tarea)
    
    return resultado


def ordenar_tareas(tareas, criterio_orden, campo_fecha="fecha_fin"):
    #ordena las tareas usando sorted
    
    #ordenar de A a Z
    if criterio_orden == "Alfabético A-Z":
        return sorted(tareas, key=lambda t: t.get("titulo", "").lower())
    
    #ordenar de Z a A
    elif criterio_orden == "Alfabético Z-A":
        return sorted(tareas, key=lambda t: t.get("titulo", "").lower(), reverse=True)
    
    #ordenar por prioridad alta primero
    elif criterio_orden == "Por prioridad alta":
        orden = {"alta": 0, "media": 1, "baja": 2}
        return sorted(tareas, key=lambda t: orden.get(t.get("prioridad", "media").lower(), 1))
    
    #ordenar por prioridad baja primero
    elif criterio_orden == "Por prioridad baja":
        orden = {"alta": 2, "media": 1, "baja": 0}
        return sorted(tareas, key=lambda t: orden.get(t.get("prioridad", "media").lower(), 1))
    
    #ordenar por proyecto
    elif criterio_orden == "Por proyecto":
        return sorted(tareas, key=lambda t: t.get("proyecto", "").lower())
    
    #ordenar por fecha de menor a mayor
    elif criterio_orden == "Fecha ascendente":
        return sorted(tareas, key=lambda t: t.get(campo_fecha, "") or "99/99/99")
    
    #ordenar por fecha de mayor a menor
    elif criterio_orden == "Fecha descendente":
        return sorted(tareas, key=lambda t: t.get(campo_fecha, "") or "00/00/00", reverse=True)
    
    #ordenar por mas atrasado primero
    elif criterio_orden == "Más atrasado primero":
        return sorted(tareas, key=lambda t: t.get("dias_atrasado", 0), reverse=True)
    
    #ordenar por menos atrasado primero
    elif criterio_orden == "Menos atrasado primero":
        return sorted(tareas, key=lambda t: t.get("dias_atrasado", 0))
    
    #si no hay criterio, devolvemos tal cual
    return tareas


def filtrar_y_ordenar(tareas, filtros, texto_busqueda="", criterio_orden="", campo_fecha="fecha_fin"):
    #primero filtramos y luego ordenamos
    tareas_filtradas = filtrar_tareas(tareas, filtros, texto_busqueda)
    
    #si hay criterio de orden, ordenamos
    if criterio_orden:
        tareas_ordenadas = ordenar_tareas(tareas_filtradas, criterio_orden, campo_fecha)
        return tareas_ordenadas
    
    return tareas_filtradas