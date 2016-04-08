import argparse
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database

# ugly hack around import a shitty import system
# TODO: Fix this once we get packaging working
try:
    from . import models
    from .connect import DBConnect
except SystemError:
    import models
    from connect import DBConnect

class CreateDB():
    def __init__(self, dialect, dbname='test'):
        self.dialect = dialect
        self.dbname = dbname

    def create(self):
        if self.dialect == 'sqlite':
            connection = DBConnect(
                    dialect='sqlite',
                    dbname=self.dbname
                    ).connect
        elif self.dialect == 'postgresql':
            tmpconn = DBConnect(
                    dialect='postgresql',
                    dbname='postgres'
                    ).connect
            engine = create_engine(tmpconn)
            conn = engine.connect()
            conn.execute('commit')
            conn.execute('create database ' + self.dbname + ';')
            conn.close()
            engine.dispose()
            connection = DBConnect(
                    dialect='postgresql',
                    dbname=self.dbname
                    ).connect
        else:
            return 'No database could be created'
        engine = create_engine(connection)
        models.Base.metadata.create_all(engine)
        return connection

def main():
    parser = argparse.ArgumentParser(description='Initialize a paste db')
    parser.add_argument('-t', '--type', default='sqlite',
                        help='sqlite or postgresql')
    parser.add_argument('-d', '--dbname', default='test.db',
                        help='name of the database to be created')
    args = parser.parse_args()
    newdb = CreateDB(args.type, args.dbname)
    print(newdb.create())

if __name__ == "__main__":
    main()
