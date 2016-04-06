import codecs
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

import models
from connect import DBConnect

class Paster():
    def __enter__(self):
        connection = DBConnect(dialect='sqlite', dbname='test.db').connect
        self.engine = create_engine(connection)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.session.close()
        self.engine.dispose()

    def create(self, data, ip=None, mac=None, mime=None, sunset=None):
        sha1 = hashlib.sha1(data).hexdigest()
        paste = models.Paste(
                hashid = sha1,
                ip = ip,
                mac = mac,
                mime = mime,
                sunset = sunset,
                data = data
                )
        try:
            self.session.add(paste)
            self.session.commit()
        except IntegrityError:
            paste.id = 'HASH COLLISION'
            self.session.rollback()
        return {'id': paste.id, 'hashid': sha1}

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

def main():
    with Paster() as paste:
        created = paste.create(b'This is a test paste')
        print(created)
        lookup = paste.query(hashid=created['hashid'])
        return lookup

if __name__ == "__main__":
    print(main())
