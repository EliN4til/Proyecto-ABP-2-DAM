from pymongo import MongoClient
from pydantic import BaseModel, Field, EmailStr, BeforeValidator
from typing import Optional, List, Annotated
from datetime import date

PyObjectId = Annotated[str, BeforeValidator(str)]

class DepartamentoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    nombre_departamento: str
    empresa: Optional[str] = None
    ubicacion: Optional[str] = None

class EmpleadoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    foto: Optional[str] = None
    identificador: str
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    cargo: Optional[str] = None
    id_departamento: PyObjectId
    email: EmailStr
    contrasenya: str
    telefono: Optional[str] = None
    incorporacion: Optional[date] = None
    estado: bool = True
    admin: bool = False

class EquipoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    nombre_equipo: Optional[str] = None
    empresa: Optional[str] = None
    integrantes: List[PyObjectId] = []

class TareaModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    icono: Optional[str] = None
    titulo: str
    descripcion: str
    categoria: Optional[str] = None
    terminada: bool = False
    retrasada: bool = False
    acceso: List[PyObjectId] = []
    inicio: Optional[date] = None
    cierre: Optional[date] = None

client = MongoClient("mongodb+srv://[usuario]:[contraseña]@gestiontareas1.mgzio0n.mongodb.net/?appName=GestionTareas1")
db = client["tareas_db"]

def crear_demo():
    dept_data = {
        "nombre_departamento": "Tecnología",
        "empresa": "TechCorp",
        "ubicacion": "Planta 2"
    }
    dept_model = DepartamentoModel(**dept_data)
    res_dept = db.departamentos.insert_one(dept_model.model_dump(by_alias=True, exclude=["id"]))
    dept_id = res_dept.inserted_id

    emp_data = {
        "identificador": "EMP-99",
        "email": "ana@techcorp.com",
        "contrasenya": "secure_pass",
        "id_departamento": str(dept_id),
        "nombre": "Ana",
        "cargo": "DevOps"
    }
    emp_model = EmpleadoModel(**emp_data)
    res_emp = db.empleados.insert_one(emp_model.model_dump(by_alias=True, exclude=["id"]))
    emp_id = res_emp.inserted_id

    equipo_data = {
        "nombre_equipo": "Infraestructura",
        "integrantes": [str(emp_id)]
    }
    equipo_model = EquipoModel(**equipo_data)
    db.equipos.insert_one(equipo_model.model_dump(by_alias=True, exclude=["id"]))

    tarea_data = {
        "titulo": "Migrar Servidores",
        "descripcion": "Mover todo a AWS",
        "acceso": [str(emp_id)]
    }
    tarea_model = TareaModel(**tarea_data)
    db.tareas.insert_one(tarea_model.model_dump(by_alias=True, exclude=["id"]))

if __name__ == "__main__":
    crear_demo()