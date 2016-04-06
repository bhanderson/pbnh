from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declaratice_base()

class Paste(Base):
    __tablename__ = 'paste'

    id = Column(Integer, primary_key=True)
    ip = Column(String)
    contents = Column(Blob)
