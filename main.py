from datetime import date
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
import uvicorn

# Aplicación FastAPI
app = FastAPI(title="API de Autos y Reservas Daniel")


class Auto(SQLModel, table=True):  # Tabla de autos
    id: int | None = Field(default=None, primary_key=True)
    marca: str
    modelo: str
    anio: int
    placa: str
    disponible: bool = True


class Reserva(SQLModel, table=True):  # Tabla de reservas
    id: int | None = Field(default=None, primary_key=True)
    auto_id: int = Field(foreign_key="auto.id")
    cliente: str
    fecha_inicio: date
    fecha_fin: date
    estado: str = "pendiente"  # pendiente, confirmada, cancelada, finalizada


engine = create_engine(  # Motor de base de datos SQLite
    "sqlite:///database.db",
    connect_args={"check_same_thread": False},
)
SQLModel.metadata.create_all(engine)


@app.get("/")  # Ruta de inicio
def inicio():
    return {"mensaje": "API de Autos y Reservas Daniel."}


# ---------------------- CRUD AUTOS ----------------------

@app.post("/autos/")  # Crear un nuevo auto
def crear_auto(auto: Auto):
    auto.id = None
    with Session(engine) as session:
        session.add(auto)
        session.commit()
        session.refresh(auto)
        return auto


@app.get("/autos/")  # Listar todos los autos
def listar_autos():
    with Session(engine) as session:
        return session.exec(select(Auto)).all()


@app.get("/autos/{auto_id}")  # Obtener un auto por su ID
def obtener_auto(auto_id: int):
    with Session(engine) as session:
        auto = session.get(Auto, auto_id)
        if not auto:
            raise HTTPException(status_code=404, detail="Auto no encontrado")
        return auto


@app.put("/autos/{auto_id}")  # Actualizar un auto
def actualizar_auto(auto_id: int, datos: Auto):
    with Session(engine) as session:
        auto = session.get(Auto, auto_id)
        if not auto:
            raise HTTPException(status_code=404, detail="Auto no encontrado")
        auto.marca = datos.marca
        auto.modelo = datos.modelo
        auto.anio = datos.anio
        auto.placa = datos.placa
        auto.disponible = datos.disponible
        session.add(auto)
        session.commit()
        session.refresh(auto)
        return auto


@app.delete("/autos/{auto_id}")  # Eliminar un auto por su ID
def eliminar_auto(auto_id: int):
    with Session(engine) as session:
        auto = session.get(Auto, auto_id)
        if not auto:
            raise HTTPException(status_code=404, detail="Auto no encontrado")
        session.delete(auto)
        session.commit()
        return {"mensaje": "Auto eliminado"}


# ---------------------- CRUD RESERVAS ----------------------

@app.post("/reservas/")  # Crear una nueva reserva
def crear_reserva(reserva: Reserva):
    reserva.id = None
    with Session(engine) as session:
        auto = session.get(Auto, reserva.auto_id)
        if not auto:
            raise HTTPException(status_code=404, detail="El auto especificado no existe")
        session.add(reserva)
        session.commit()
        session.refresh(reserva)
        return reserva


@app.get("/reservas/")  # Listar todas las reservas
def listar_reservas():
    with Session(engine) as session:
        return session.exec(select(Reserva)).all()


@app.get("/reservas/{reserva_id}")  # Obtener una reserva por su ID
def obtener_reserva(reserva_id: int):
    with Session(engine) as session:
        reserva = session.get(Reserva, reserva_id)
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        return reserva


@app.put("/reservas/{reserva_id}")  # Actualizar una reserva
def actualizar_reserva(reserva_id: int, datos: Reserva):
    with Session(engine) as session:
        reserva = session.get(Reserva, reserva_id)
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        reserva.auto_id = datos.auto_id
        reserva.cliente = datos.cliente
        reserva.fecha_inicio = datos.fecha_inicio
        reserva.fecha_fin = datos.fecha_fin
        reserva.estado = datos.estado
        session.add(reserva)
        session.commit()
        session.refresh(reserva)
        return reserva


@app.delete("/reservas/{reserva_id}")  # Eliminar una reserva por su ID
def eliminar_reserva(reserva_id: int):
    with Session(engine) as session:
        reserva = session.get(Reserva, reserva_id)
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        session.delete(reserva)
        session.commit()
        return {"mensaje": "Reserva eliminada"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
