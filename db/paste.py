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
        return {'id': paste.id, 'hash': sha1}

def main():
    with Paster() as paste:
        return paste.create(b'This is a test paste')

if __name__ == "__main__":
    print(main())
