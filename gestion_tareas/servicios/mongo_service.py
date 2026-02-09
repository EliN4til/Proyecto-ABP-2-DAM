import pymongo

class ServiceMongo:
    def __init__(self):
        self.cliente = None
        self.base_datos = None

    def conectar(self, uri_servidor, usuario, contrasena):
        # intenta conectar a mongo atlas
        try:
            ruta_conexion = f"mongodb+srv://{usuario}:{contrasena}@{uri_servidor}/?appName=GestionTareas1"
            
            self.cliente = pymongo.MongoClient(ruta_conexion, serverSelectionTimeoutMS=2000)
            
            # probamos si la conexion funciona
            self.cliente.admin.command('ping')
            
            self.base_datos = self.cliente["tareas_db"]
            return True
        except Exception as e:
            print(f"Error de conexion en Mongo: {e}")
            self.cliente = None
            return False

    def obtener_instancia(self):
        # devuelve la base de datos para poder usarla
        return self.base_datos