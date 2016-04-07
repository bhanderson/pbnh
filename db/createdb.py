import argparse
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database

import models
from connect import DBConnect

def main():
    parser = argparse.ArgumentParser(description='Initialize a paste db')
    parser.add_argument('-t', '--type', default='sqlite', 
                        help='sqlite or postgresql')
    args = parser.parse_args()

    if args.type == 'sqlite':
	    connection = DBConnect(dialect='sqlite', dbname='test.db').connect
    elif args.type == 'postgresql':
            psqlconnection = DBConnect(dialect='postgresql', dbname='postgres').connect
            engine = create_engine(psqlconnection)
            conn = engine.connect()
            conn.execute('commit')
            conn.execute('create database test;')
            conn.close()
            engine.dispose()
            connection = DBConnect(dialect='postgresql', dbname='test').connect
    else:
        return 'No database could be created'
    print('Creating database: ' + connection)
    engine = create_engine(connection)
    models.Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()
