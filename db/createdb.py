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
    def __init__(self, dialect=None, dbname=None):
        self.dialect = dialect or 'sqlite'
        self.dbname = dbname or 'test'

    def create(self):
        if self.dialect == 'sqlite':
            connection = DBConnect(
                    dialect='sqlite',
                    dbname=self.dbname
                    )
        elif self.dialect == 'postgresql':
            connection = DBConnect(
                    dialect='postgresql',
                    dbname=self.dbname
                    )
        else:
            return 'No database could be created'
        create_database(str(connection))
        engine = create_engine(str(connection))
        models.Base.metadata.create_all(engine)
        return connection

def main():
    parser = argparse.ArgumentParser(description='Initialize a paste db')
    parser.add_argument('-t', '--type',
                        help='sqlite or postgresql')
    parser.add_argument('-d', '--dbname',
                        help='name of the database to be created')
    args = parser.parse_args()
    newdb = CreateDB(args.type, args.dbname)
    print(newdb.create())

if __name__ == "__main__":
    main()
