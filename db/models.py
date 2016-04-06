from sqlalchemy import Blob, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declaratice_base()

class Paste(Base):
    """Class to define the paste table
    
    paste
    -------------
    id           (PK) int
    hashid       string (hash of data)
    ip           string (will be of "ip address" type in pg)
    mac          string (will be of "mac address" type in pg)
    mime         string
    timestamp    datetime
    sunset       datetime
    data         blob    
    """
    __tablename__ = 'paste'

    id = Column(Integer, primary_key=True)
    hashid = Column(String, nullable=False)
    ip = Column(String)
    mac = Column(String)
    timestamp = Colum(DateTime, nullable=False)
    mime = Column(String, default='text/plain')
    sunset = Column(DateTime)
    data = Column(Blob)
