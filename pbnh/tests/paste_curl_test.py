#!/usr/bin/python3
import unittest
import json
import os

from pbnh import conf
from pbnh import app
from pbnh.db.createdb import CreateDB


DEFAULTS = {
    "server": {
        "bind_ip": "127.0.0.1",
        "bind_port": 8080,
        "debug": True,
    },
    "database": {
        "dbname": "pastedb",
        "dialect": "sqlite",
        "driver": None,
        "host": None,
        "password": None,
        "port": None,
        "username": None
    }
}


class TestPost(unittest.TestCase):
    def setUp(self):
        self.newdb = CreateDB(dialect=DEFAULTS['database']['dialect'],
                dbname=DEFAULTS['database']['dbname'])
        self.newdb.create()
        app.app.config['CONFIG'] = DEFAULTS
        self.app = app.app.test_client()

    def tearDown(self):
        os.unlink(DEFAULTS['database']['dbname'])

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.app.get('/about.md')
        self.assertEqual(response.status_code, 200)

    def test_nopaste(self):
        response = self.app.get('/1')
        self.assertEqual(response.status_code, 404)

    def test_paste(self):
        response = self.app.post('/', data={'content': 'abc'})
        j = json.loads(response.data.decode('utf-8'))
        self.failUnlessEqual(j.get('hashid'),
                'a9993e364706816aba3e25717850c26c9cd0d89d')
        self.assertEqual(response.status_code, 201)
        response = self.app.get('/1')
        self.assertEqual(response.status_code, 200)
