from servicios.mongo_service import ServiceMongo

instancia_db = ServiceMongo()

def realizar_conexion(uri, user, password):
    """Función que llama la vista"""
    return instancia_db.conectar(uri, user, password)