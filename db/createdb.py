from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

import models

class DBConnect():
    """create db connection string"""
    def __init__(self, dialect=None, driver=None, username=None, password=None,
                 host=None, port=None, dbname=None):
        self._connect = dialect
        if driver:
            self._connect += '+' + driver
        self._connect += '://'
        if username:
            self._connect += username
            if password:
                self._connect += ':' + password
            self._connnect +='@'
        if host:
            self._connect += host
            if port:
                self._connect += ':' + port
        if dbname:
            self._connect += '/' + dbname

    @property
    def connect(self):
        """Connection string read-only property"""
        return self._connect

def main():
    connection = DBConnect(dialect='sqlite', dbname='test.db').connect
    print('Creating database: ' + connection)
    engine = create_engine(connection)
    models.Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()
