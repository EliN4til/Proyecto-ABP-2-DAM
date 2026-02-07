_usuario_activo = None
_contexto_dashboard = "personal"  #puede ser "admin" o "personal"


def guardar_usuario(datos_usuario):
    #guarda los datos del usuario cuando inicia sesion
    global _usuario_activo
    _usuario_activo = datos_usuario


def obtener_usuario():
    #devuelve los datos del usuario o None si no hay sesion
    return _usuario_activo


def obtener_nombre_usuario():
    #devuelve el nombre del usuario activo o "Usuario" como dato por defecto si no hay una sesion iniciada
    if _usuario_activo and "nombre" in _usuario_activo:
        return _usuario_activo["nombre"]
    return "Usuario"


def obtener_id_usuario():
    #devuelve el id del usuario o None si no hay sesion
    if _usuario_activo and "_id" in _usuario_activo:
        return _usuario_activo["_id"]
    return None


def hay_sesion():
    #comprueba si hay un usuario con sesión activa
    return _usuario_activo is not None


def cerrar_sesion():
    #cierra la sesion del usuario
    global _usuario_activo
    _usuario_activo = None


def establecer_contexto(contexto):
    #guarda de que panel viene el usuario (admin o personal)
    global _contexto_dashboard
    _contexto_dashboard = contexto


def obtener_contexto():
    #devuelve el contexto guardado
    return _contexto_dashboard