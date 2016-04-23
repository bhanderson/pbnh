import argparse
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database

from pbnh import conf
from pbnh.db import models
from pbnh.db.connect import DBConnect

class CreateDB():
    def __init__(self, dialect=None, driver=None, username=None, password=None,
                 host=None, port=None, dbname=None):
        """Grab connection information to pass to DBConnect"""
        self.dialect = dialect or 'sqlite'
        self.dbname = dbname or 'test'
        self.driver = driver
        self.username = username
        self.password = password
        self.host = host or 'localhost'
        self.port = port

    def create(self):
        connection = DBConnect(
                dialect=self.dialect,
                driver=self.driver,
                username=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                dbname=self.dbname
                )
        print(connection)
        create_database(str(connection))
        engine = create_engine(str(connection))
        models.Base.metadata.create_all(engine)
        return connection

def main():
    config = conf.get_config().get('database')
    parser = argparse.ArgumentParser(description='Initialize a paste db')
    parser.add_argument('-t', '--type', default=config.get('dialect'),
                        help='sqlite or postgresql')
    parser.add_argument('-n', '--dbname', default=config.get('dbname'),
                        help='name of the database to be created')
    parser.add_argument('-d', '--driver', default=config.get('driver'),
                        help='database driver for sqlalchemy to use')
    parser.add_argument('-u', '--username', default=config.get('username'),
                        help='username to use for the database connection')
    parser.add_argument('-p', '--password', default=config.get('password'),
                        help='password to use for the database connection')
    parser.add_argument('-s', '--server', default=config.get('host'),
                        help='host of the database')
    parser.add_argument('-P', '--port', default=config.get('port'),
                        help='port the database listens on')
    args = parser.parse_args()
    newdb = CreateDB(dialect=args.type, driver=args.driver, username=args.username,
                     password=args.password, host=args.server, port=args.port,
                     dbname=args.dbname)
    print(newdb.create())

if __name__ == "__main__":
    main()
