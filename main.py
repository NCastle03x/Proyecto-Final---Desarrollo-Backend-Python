from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
import services
from database import engine, get_db

# Creación de tablas en SQLite si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Reseñas de Negocios RD",
    description="API Inteligente para la gestión y análisis de reseñas utilizando FastAPI, SQLite y Google Gemini.",
    version="1.0.0"
)

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a la API de Reseñas de Negocios RD. Utiliza los endpoints para interactuar con las reseñas y obtener análisis de sentimientos."}

@app.post("/resenas/", response_model=schemas.ResenaResponse, status_code=status.HTTP_201_CREATED)
def crear_resena(resena: schemas.ResenaCreate, db: Session = Depends(get_db)):
    # 1. Determinar sentimiento mediante el servicio de IA
    sentimiento_detectado = services.analizar_sentimiento(resena.comentario)
    
    # 2. Guardar registro en la base de datos
    db_resena = models.Resena(
        cliente=resena.cliente,
        comentario=resena.comentario,
        calificacion=resena.calificacion,
        sentimiento=sentimiento_detectado
    )
    db.add(db_resena)
    db.commit()
    db.refresh(db_resena)
    return db_resena

@app.get("/resenas/", response_model=list[schemas.ResenaResponse])
def listar_resenas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Resena).offset(skip).limit(limit).all()

@app.get("/resenas/resumen")
def obtener_resumen(db: Session = Depends(get_db)):
    resenas = db.query(models.Resena).all()
    resumen = services.generar_resumen_opiniones(resenas)
    return {"resumen_ia": resumen}

# -------------------------------------------------------------------
# NUEVOS ENDPOINTS: PUT Y DELETE
# -------------------------------------------------------------------

@app.put("/resenas/{resena_id}", response_model=schemas.ResenaResponse, summary="Actualizar una reseña existente")
def actualizar_resena(resena_id: int, resena_actualizada: schemas.ResenaCreate, db: Session = Depends(get_db)):
    # 1. Buscar la reseña por ID
    db_resena = db.query(models.Resena).filter(models.Resena.id == resena_id).first()
    if not db_resena:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Reseña con ID {resena_id} no encontrada"
        )
    
    # 2. Re-evaluar el sentimiento si el comentario cambió
    if db_resena.comentario != resena_actualizada.comentario:
        db_resena.sentimiento = services.analizar_sentimiento(resena_actualizada.comentario)
    
    # 3. Actualizar los campos
    db_resena.cliente = resena_actualizada.cliente
    db_resena.comentario = resena_actualizada.comentario
    db_resena.calificacion = resena_actualizada.calificacion
    
    db.commit()
    db.refresh(db_resena)
    return db_resena

@app.delete("/resenas/{resena_id}", status_code=status.HTTP_200_OK, summary="Eliminar una reseña")
def eliminar_resena(resena_id: int, db: Session = Depends(get_db)):
    # 1. Buscar la reseña por ID
    db_resena = db.query(models.Resena).filter(models.Resena.id == resena_id).first()
    if not db_resena:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Reseña con ID {resena_id} no encontrada"
        )
    
    # 2. Eliminar del registro
    db.delete(db_resena)
    db.commit()
    return {"mensaje": f"Reseña con ID {resena_id} eliminada exitosamente"}