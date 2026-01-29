from pymongo import MongoClient
from pydantic import BaseModel, Field, EmailStr, BeforeValidator
from typing import List, Optional, Annotated
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

client = MongoClient("mongodb+srv://ayoze:9978@gestiontareas1.mgzio0n.mongodb.net/?appName=GestionTareas1")
db = client["tareas_db"]

# Submodelos que vamos a incrustar en las colecciones
class InfoDepartamento(BaseModel):
    nombre: str
    ubicacion: str

class UsuarioResumen(BaseModel):
    """
    Guardamos una copia pequeña de los datos del usuario
    en la colección de tareas para cargar las tareas más rapidamente.
    (Basicamente patrón Subset)
    """
    id_usuario: PyObjectId
    nombre: str
    foto: Optional[str] = None


# EMPLEADOS
class EmpleadoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    identificador: str
    nombre: str
    email: EmailStr
    contrasenya: str
    foto: Optional[str] = None
    
    # incrustamos los datos a los que accederemos regularmente
    departamento: InfoDepartamento 
    cargo: str
    es_admin: bool = False

# PROYECTOS
class ProyectoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    nombre_proyecto: str
    cliente: str
    presupuesto: float
    fecha_inicio: datetime
    fecha_fin: datetime
    activo: bool = True

# 3. TAREAS
class TareaModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    titulo: str
    descripcion: str
    estado: str = "pendiente"
    
    # Referencia al id del al que pertenece proyecto
    id_proyecto: PyObjectId
    
    asignados: List[UsuarioResumen] = []
    fecha_limite: Optional[datetime] = None

def cargar_datos_prueba():
    empleado = EmpleadoModel(
        identificador="26603992F",
        nombre="Laura",
        email="laura@test.com",
        contrasenya="1234",
        departamento=InfoDepartamento(nombre="IT", ubicacion="Planta 1"),
        cargo="Desarrollador Backend"
    )
    resumen_empleado = db.empleados.insert_one(empleado.model_dump(by_alias=True, exclude=["id"]))

    proy = ProyectoModel(
        nombre_proyecto="App Gestión Empleados",
        cliente="Mercadona",
        presupuesto=1500.00,
        fecha_inicio=datetime.today(),
        fecha_fin=datetime(2026, 6, 30)
    )
    resumen_proyecto = db.proyectos.insert_one(proy.model_dump(by_alias=True, exclude=["id"]))
    

    resumen_laura = UsuarioResumen(
        id_usuario=str(resumen_empleado.inserted_id),
        nombre="Laura",
        foto="img_laura.png"
    )
    
    tarea = TareaModel(
        titulo="Diseñar Base de Datos",
        descripcion="Hay que diseñar el modelo de la BBDD que usará la aplicación",
        id_proyecto=str(resumen_proyecto.inserted_id),
        asignados=[resumen_laura]
    )
    db.tareas.insert_one(tarea.model_dump(by_alias=True, exclude=["id"]))
    
    print("Se han insertado los datos de prueba correctamente")

if __name__ == "__main__":
    cargar_datos_prueba()