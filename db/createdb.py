from sqlalchemy import create_engine
from sqlalchemy_utils import create_database

import models
from connect import DBConnect

def main():
    connection = DBConnect(dialect='sqlite', dbname='test.db').connect
    print('Creating database: ' + connection)
    engine = create_engine(connection)
    models.Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()
