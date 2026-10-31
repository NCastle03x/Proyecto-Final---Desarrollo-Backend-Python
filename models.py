from sqlalchemy import Column, Integer, String, Text
from database import Base

class Resena(Base):
    __tablename__ = "resenas"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, index=True)
    comentario = Column(Text)
    calificacion = Column(Integer)
    sentimiento = Column(String)  # Positivo, Neutral, Negativo
