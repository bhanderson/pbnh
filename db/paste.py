import codecs
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from . import models
from .connect import DBConnect

class Paster():
    def __init__(self, dialect='sqlite', dbname='test.db'):
        self.dialect = dialect
        self.dbname = dbname

    def __enter__(self):
        connection = DBConnect(dialect=self.dialect, dbname=self.dbname).connect
        self.engine = create_engine(connection)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.session.close()
        self.engine.dispose()

    def create(self, data, ip=None, mac=None, mime=None, sunset=None,
               timestamp=None):
        sha1 = hashlib.sha1(data).hexdigest()
        collision = self.query(hashid=sha1)
        if collision:
            print(collision)
            pasteid = collision.get('id')
        else:
            paste = models.Paste(
                    hashid = sha1,
                    ip = ip,
                    mac = mac,
                    mime = mime,
                    sunset = sunset,
                    timestamp = timestamp,
                    data = data
                    )
            try:
                self.session.add(paste)
                self.session.commit()
            except IntegrityError:
                pasteid = 'HASH COLLISION'
                self.session.rollback()
            else:
                pasteid = paste.id
        return {'id': pasteid, 'hashid': sha1}

    def query(self, id=None, hashid=None):
        result = None
        if id:
            result = (self.session.query(models.Paste)
                      .filter(models.Paste.id == id).first())
        elif hashid:
            result = (self.session.query(models.Paste)
                      .filter(models.Paste.hashid == hashid).first())
        else:
            return None
        if result:
            result = {
                    'id': result.id,
                    'hashid': result.hashid,
                    'ip': result.ip,
                    'mac': result.mac,
                    'mime': result.mime,
                    'timestamp': result.timestamp,
                    'sunset': result.sunset,
                    'data': result.data
                    }

        return result

    def delete(self, id=None, hashid=None):
        if id:
            result = (self.session.query(models.Paste)
                      .filter(models.Paste.id == id).first())
        elif hashid:
            result = (self.session.query(models.Paste)
                      .filter(models.Paste.hashid == hashid).first())
        else:
            return None
        self.session.delete(result)
        self.session.commit()
