import argparse
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database

from pbnh.db import models
from pbnh.db.connect import DBConnect


class CreateDB():
    def __init__(self, dialect=None, driver=None, username=None, password=None,
                 host=None, port=None, dbname=None):
        """Grab connection information to pass to DBConnect"""
        self.dialect = dialect or 'sqlite'
        self.dbname = dbname or 'pastedb'
        self.driver = driver
        self.username = username
        self.password = password
        self.host = host
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
        #print(connection)
        create_database(str(connection))
        engine = create_engine(str(connection))
        models.Base.metadata.create_all(engine)
        return connection
