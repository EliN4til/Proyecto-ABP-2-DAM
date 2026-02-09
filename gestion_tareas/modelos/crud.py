from bson import ObjectId
from datetime import datetime
from gestion_tareas.servicios.db_manager import instancia_db
from gestion_tareas.modelos.init import (
    EmpleadoModel, 
    DepartamentoModel, 
    ProyectoModel, 
    TareaModel
)
from pydantic import ValidationError

from gestion_tareas.servicios.sesion_service import obtener_nombre_usuario

# pillar la base de datos del db_manager (la conexion que se hizo al hacer login)
def get_db():
    return instancia_db.obtener_instancia()


def es_id_valido(id_str):
    #comprueba si el id es valido para mongodb
    try:
        ObjectId(id_str)
        return True
    except:
        return False


def registrar_log(accion, modulo, descripcion, usuario=None):
    #guarda un log de lo que se hace en la app
    try:
        # Si no se especifica usuario, intentamos obtener el de la sesión
        if usuario is None:
            usuario = obtener_nombre_usuario()
            # Si devuelve "Usuario" (por defecto cuando no hay nada), lo cambiamos a Sistema si es una acción interna
            if usuario == "Usuario":
                usuario = "Sistema"

        log = {
            "accion": accion,
            "modulo": modulo,
            "descripcion": descripcion,
            "usuario": usuario,
            "fecha_completa": datetime.now(),
        }
        get_db().auditoria.insert_one(log)
    except Exception as e:
        print("error guardando log:", e)



# --- empleados ---

def existe_email_empleado(email):
    # mira si ya hay un empleado con ese email
    if not email:
        return False
    empleado = get_db().empleados.find_one({"email": email})
    return empleado is not None

def existe_identificador_empleado(identificador):
    # mira si ya hay un empleado con ese dni/nie
    if not identificador:
        return False
    empleado = get_db().empleados.find_one({"identificador": identificador})
    return empleado is not None


def crear_empleado(datos):
    #crea un empleado nuevo
    try:
        # Validacion con Pydantic
        empleado = EmpleadoModel(**datos)
        
        # Validar duplicados manual
        errores = []
        if existe_email_empleado(datos.get("email")):
            errores.append({"loc": ["email"], "msg": "El email ya está registrado"})
            
        if existe_identificador_empleado(datos.get("identificador")):
            errores.append({"loc": ["identificador"], "msg": "El DNI/NIE ya está registrado"})
            
        if errores:
            return (False, errores)
        
        # Insertar usando el dump del modelo
        resultado = get_db().empleados.insert_one(empleado.model_dump(by_alias=True, exclude=["id"]))
        datos["_id"] = str(resultado.inserted_id)
        
        registrar_log("Crear", "Usuarios", "usuario registrado: " + datos["nombre"])
        return (True, datos)
    except ValidationError as e:
        return (False, e.errors())
    except Exception as e:
        return (False, str(e))


def obtener_empleado(id_empleado):
    #busca un empleado por su id
    if not es_id_valido(id_empleado):
        return (False, "id no valido")
    
    empleado = get_db().empleados.find_one({"_id": ObjectId(id_empleado)})
    if empleado:
        empleado["_id"] = str(empleado["_id"])
        return (True, empleado)
    return (False, "empleado no encontrado")


def obtener_empleado_por_email(email):
    #busca un empleado por email
    empleado = get_db().empleados.find_one({"email": email})
    if empleado:
        empleado["_id"] = str(empleado["_id"])
        return (True, empleado)
    return (False, "empleado no encontrado")


def obtener_todos_empleados():
    #devuelve todos los empleados
    try:
        empleados = list(get_db().empleados.find())
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
        resultado = get_db().empleados.update_one(
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
        emp = get_db().empleados.find_one({"_id": ObjectId(id_empleado)})
        if emp:
            nombre = emp["nombre"] + " " + emp["apellidos"]
        else:
            nombre = id_empleado
        
        resultado = get_db().empleados.delete_one({"_id": ObjectId(id_empleado)})
        if resultado.deleted_count > 0:
            registrar_log("Eliminar", "Usuarios", "usuario eliminado: " + nombre)
            return (True, "empleado eliminado")
        return (False, "no se encontro el empleado")
    except Exception as e:
        return (False, str(e))


# --- departamentos ---

def existe_codigo_departamento(codigo):
    if not codigo: return False
    return get_db().departamentos.find_one({"codigo": codigo}) is not None

def crear_departamento(datos):
    #crea un departamento

    try:
        # Validacion con Pydantic
        if "fecha_creacion" not in datos:
            datos["fecha_creacion"] = datetime.now()
            
        depto = DepartamentoModel(**datos)
        
        # Validar duplicados manual
        errores = []
        if existe_codigo_departamento(datos.get("codigo")):
            errores.append({"loc": ["codigo"], "msg": "El código de departamento ya existe"})
            
        if errores:
            return (False, errores)
        
        resultado = get_db().departamentos.insert_one(depto.model_dump(by_alias=True, exclude=["id"]))
        datos["_id"] = str(resultado.inserted_id)
        

        registrar_log("Crear", "Departamentos", f"departamento creado: {datos['nombre']}")
        return (True, datos)
    except ValidationError as e:
        return (False, e.errors())
    except Exception as e:
        return (False, str(e))



def obtener_departamento(id_departamento):
    #busca un departamento por id
    if not es_id_valido(id_departamento):
        return (False, "id no valido")
    
    depto = get_db().departamentos.find_one({"_id": ObjectId(id_departamento)})
    if depto:
        depto["_id"] = str(depto["_id"])
        return (True, depto)
    return (False, "departamento no encontrado")


def obtener_todos_departamentos():
    #devuelve todos los departamentos
    try:
        deptos = list(get_db().departamentos.find())

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
        resultado = get_db().departamentos.update_one(
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
        resultado = get_db().departamentos.delete_one({"_id": ObjectId(id_departamento)})
        if resultado.deleted_count > 0:
            registrar_log("Eliminar", "Departamentos", "departamento borrado")
            return (True, "departamento eliminado")
        return (False, "no se encontro el departamento")
    except Exception as e:
        return (False, str(e))

# --- proyectos ---

def existe_codigo_proyecto(codigo):
    if not codigo: return False
    return get_db().proyectos.find_one({"codigo": codigo}) is not None

def crear_proyecto(datos):
    #crea un proyecto nuevo
    try:
        # Validacion con Pydantic
        proyecto = ProyectoModel(**datos)
        
        # Validar duplicados manual
        errores = []
        if existe_codigo_proyecto(datos.get("codigo")):
            errores.append({"loc": ["codigo"], "msg": "El código de proyecto ya existe"})
            
        if errores:
            return (False, errores)
        
        resultado = get_db().proyectos.insert_one(proyecto.model_dump(by_alias=True, exclude=["id"]))
        datos["_id"] = str(resultado.inserted_id)
        
        registrar_log("Crear", "Proyectos", f"proyecto iniciado: {datos['nombre']}")
        return (True, datos)
    except ValidationError as e:
        return (False, e.errors())
    except Exception as e:
        return (False, str(e))


def obtener_proyecto(id_proyecto):
    #busca un proyecto por id
    if not es_id_valido(id_proyecto):
        return (False, "id no valido")
    
    proyecto = get_db().proyectos.find_one({"_id": ObjectId(id_proyecto)})
    if proyecto:
        proyecto["_id"] = str(proyecto["_id"])
        return (True, proyecto)
    return (False, "proyecto no encontrado")


def obtener_todos_proyectos():
    #devuelve todos los proyectos
    try:
        proyectos = list(get_db().proyectos.find())
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
        resultado = get_db().proyectos.update_one(
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
        resultado = get_db().proyectos.delete_one({"_id": ObjectId(id_proyecto)})
        if resultado.deleted_count > 0:
            registrar_log("Eliminar", "Proyectos", "proyecto borrado")
            return (True, "proyecto eliminado")
        return (False, "no se encontro el proyecto")
    except Exception as e:
        return (False, str(e))


# --- tareas ---

def crear_tarea(datos):
    #crea una tarea nueva
    try:
        # Validacion con Pydantic
        tarea = TareaModel(**datos)
        
        resultado = get_db().tareas.insert_one(tarea.model_dump(by_alias=True, exclude=["id"]))
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
    
    tarea = get_db().tareas.find_one({"_id": ObjectId(id_tarea)})
    if tarea:
        tarea["_id"] = str(tarea["_id"])
        return (True, tarea)
    return (False, "tarea no encontrada")


def obtener_todas_tareas():
    #devuelve todas las tareas
    try:
        tareas = list(get_db().tareas.find())
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def obtener_tareas_por_estado(estado):
    #busca tareas por su estado (pendiente, completada, etc)
    try:
        tareas = list(get_db().tareas.find({"estado": estado}))
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
        tareas = list(get_db().tareas.find(filtro))
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def obtener_tareas_por_usuario(id_usuario):
    #busca las tareas asignadas a un usuario
    try:
        tareas = list(get_db().tareas.find({"asignados.id_usuario": id_usuario}))
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def obtener_tareas_atrasadas(id_usuario, nombre_usuario):
    #busca las tareas que estan atrasadas
    try:
        ahora = datetime.now()
        #buscamos tareas no completadas con fecha limite pasada
        filtro = {
            "estado": {"$ne": "completada"},
            "fecha_limite": {"$lt": ahora},
            "$or": [
                {"asignados.id_usuario": id_usuario},
                {"compartido_por": nombre_usuario}
            ]
        }
        tareas = list(get_db().tareas.find(filtro))
        for t in tareas:
            t["_id"] = str(t["_id"])
        return (True, tareas)
    except Exception as e:
        return (False, str(e))


def obtener_tareas_completadas_usuario(id_usuario, nombre_usuario):
    #busca las tareas completadas del usuario (asignadas o creadas por el)
    try:
        filtro = {
            "estado": "completada",
            "$or": [
                {"asignados.id_usuario": id_usuario},
                {"compartido_por": nombre_usuario}
            ]
        }
        tareas = list(get_db().tareas.find(filtro))
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
        
        resultado = get_db().tareas.update_one(
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
        resultado = get_db().tareas.delete_one({"_id": ObjectId(id_tarea)})
        if resultado.deleted_count > 0:
            registrar_log("Eliminar", "Tareas", "tarea borrada")
            return (True, "tarea eliminada")
        return (False, "no se encontro la tarea")
    except Exception as e:
        return (False, str(e))


# --- login ---

def validar_login(email, contrasenya):
    #comprueba si el email y la contraseña son correctos
    if not email or not contrasenya:
        return (False, "email y contraseña son obligatorios")
    
    empleado = get_db().empleados.find_one({"email": email})
    
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


# --- configuracion ---

def obtener_configuracion():
    # devuelve la configuración actual, si no existe la crea
    try:
        config = get_db().configuracion.find_one()
        if not config:
            # Crear configuración por defecto
            nueva_config = ConfiguracionModel()
            resultado = get_db().configuracion.insert_one(nueva_config.model_dump(by_alias=True, exclude=["id"]))
            nueva_config.id = str(resultado.inserted_id)
            return (True, nueva_config.model_dump(by_alias=True))
        
        config["_id"] = str(config["_id"])
        return (True, config)
    except Exception as e:
        return (False, str(e))

def actualizar_configuracion(nuevos_datos):
    # actualiza la configuración
    try:
        # Actualizamos el único documento que debería haber
        resultado = get_db().configuracion.update_one(
            {}, # Filtro vacío para pillar el primero (y único)
            {"$set": nuevos_datos},
            upsert=True # Si no existe lo crea (por seguridad)
        )
        
        registrar_log("Configuración", "Sistema", "configuración global actualizada")
        return (True, "Configuración actualizada")
    except Exception as e:
        return (False, str(e))


# --- filtrar y ordenar tareas ---

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
            # Comprobamos si el tag está en la lista de tags
            if filtro_tag not in tarea.get("tags", []):
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
        return sorted(tareas, key=lambda t: (t.get("titulo") or "").lower())
    
    #ordenar de Z a A
    elif criterio_orden == "Alfabético Z-A":
        return sorted(tareas, key=lambda t: (t.get("titulo") or "").lower(), reverse=True)
    
    #ordenar por prioridad alta primero
    elif criterio_orden == "Por prioridad alta":
        orden = {"alta": 0, "media": 1, "baja": 2}
        return sorted(tareas, key=lambda t: orden.get((t.get("prioridad") or "media").lower(), 1))
    
    #ordenar por prioridad baja primero
    elif criterio_orden == "Por prioridad baja":
        orden = {"alta": 2, "media": 1, "baja": 0}
        return sorted(tareas, key=lambda t: orden.get((t.get("prioridad") or "media").lower(), 1))
    
    #ordenar por proyecto
    elif criterio_orden == "Por proyecto":
        return sorted(tareas, key=lambda t: (t.get("proyecto") or "").lower())
    
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