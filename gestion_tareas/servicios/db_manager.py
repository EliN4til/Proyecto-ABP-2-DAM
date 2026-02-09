from gestion_tareas.servicios.mongo_service import ServiceMongo

instancia_db = ServiceMongo()

def realizar_conexion(uri, user, password):
    # funcion que llama la vista de login para conectar
    return instancia_db.conectar(uri, user, password)