from pymongo import MongoClient
from pydantic import BaseModel, Field, EmailStr, BeforeValidator
from typing import List, Optional, Annotated
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

client = MongoClient("mongodb+srv://ayoze:9978@gestiontareas1.mgzio0n.mongodb.net/?appName=GestionTareas1")
db = client["tareas_db"]

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


class EmpleadoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    identificador: str
    nombre: str
    apellidos: str
    email: EmailStr
    contrasenya: str
    foto: Optional[str] = None
    estado: str = "ACTIVO"
    empresa: str
    equipo: str
    proyecto: Optional[str] = None
    departamento: InfoDepartamento 
    cargo: str
    id_empleado: str
    telefono: str
    ubicacion: str
    fecha_incorporacion: datetime
    fecha_alta: Optional[datetime] = None
    es_admin: bool = False

class DepartamentoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    nombre: str
    codigo: Optional[str] = None
    empresa: str
    responsable: Optional[str] = None
    descripcion: Optional[str] = None
    ubicacion: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    presupuesto: Optional[float] = None
    estado: str = "ACTIVO"

class EquipoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    nombre: str
    codigo: Optional[str] = None
    empresa: str
    departamento: str
    lider: Optional[str] = None
    miembros: List[str] = []
    descripcion: Optional[str] = None
    metodologia: Optional[str] = None
    capacidad: Optional[int] = None
    estado: bool = False

class ProyectoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    nombre: str
    codigo: Optional[str] = None
    responsable: Optional[str] = None
    cliente: str
    presupuesto: str
    estado: str = "ACTIVO"
    fecha_inicio: datetime
    fecha_fin: datetime

class TareaModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    titulo: str
    requisitos: str
    estado: str = "pendiente"
    tags: List[str] = []
    icono: str
    id_proyecto: PyObjectId
    proyecto: Optional[str] = None
    prioridad: str = "Media"
    asignados: List[UsuarioResumen] = []
    compartido_por: Optional[str] = None
    atrasado: bool = False
    fecha_inicio: Optional[datetime] = None
    fecha_limite: Optional[datetime] = None
    fecha_completado: Optional[datetime] = None

class RolModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    nombre: str
    codigo: str
    descripcion: str
    usuarios: int = 0
    color: str = "#4682B4"
    permisos: dict = {}

def cargar_datos_prueba():
    empleado = EmpleadoModel(
        identificador="26603992F",
        nombre="Laura",
        apellidos="García",
        email="laura@test.com",
        contrasenya="1234",
        estado="ACTIVO",
        empresa="TechSolutions S.L",
        equipo="Backend Team",
        departamento=InfoDepartamento(nombre="IT", ubicacion="Planta 1"),
        cargo="Desarrollador Backend",
        id_empleado="EMP001",
        telefono="+34 912 345 678",
        ubicacion="Oficina Central - Madrid",
        fecha_incorporacion=datetime(2021, 3, 15)
    )
    resumen_empleado = db.empleados.insert_one(empleado.model_dump(by_alias=True, exclude=["id"]))

    proy = ProyectoModel(
        nombre="App Gestión Empleados",
        codigo="PRY001",
        responsable="Laura García",
        cliente="Mercadona",
        presupuesto="1.500 €",
        fecha_inicio=datetime.today(),
        fecha_fin=datetime(2026, 6, 30)
    )
    resumen_proyecto = db.proyectos.insert_one(proy.model_dump(by_alias=True, exclude=["id"]))
    

    resumen_laura = UsuarioResumen(
        id_usuario=str(resumen_empleado.inserted_id),
        nombre="Laura",
        foto=None
    )
    
    tarea = TareaModel(
        titulo="Diseñar Base de Datos",
        requisitos="Hay que diseñar el modelo de la BBDD que usará la aplicación",
        icono="📋",
        id_proyecto=str(resumen_proyecto.inserted_id),
        asignados=[resumen_laura]
    )
    db.tareas.insert_one(tarea.model_dump(by_alias=True, exclude=["id"]))
    
    print("Se han insertado los datos de prueba correctamente")

if __name__ == "__main__":
    cargar_datos_prueba()