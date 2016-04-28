#!/usr/bin/python3
import unittest
import json
import os

from pbnh import conf
from pbnh import app
from pbnh.db.createdb import CreateDB
from io import BytesIO


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

    def test_paste_string_c(self):
        response = self.app.post('/', data={'c': 'abc'})
        j = json.loads(response.data.decode('utf-8'))
        self.failUnlessEqual(j.get('hashid'),
                'a9993e364706816aba3e25717850c26c9cd0d89d')
        self.assertEqual(response.status_code, 201)
        response = self.app.get('/1')
        self.assertEqual(response.status_code, 200)

    def test_paste_string_content(self):
        response = self.app.post('/', data={'content': 'abc'})
        j = json.loads(response.data.decode('utf-8'))
        self.failUnlessEqual(j.get('hashid'),
                'a9993e364706816aba3e25717850c26c9cd0d89d')
        self.assertEqual(response.status_code, 201)
        response = self.app.get('/1')
        self.assertEqual(response.status_code, 200)

    def test_redirect(self):
        response = self.app.post('/', data={'r': 'http://www.google.com'})
        j = json.loads(response.data.decode('utf-8'))
        self.failUnlessEqual(j.get('hashid'),
                '738ddf35b3a85a7a6ba7b232bd3d5f1e4d284ad1')
        self.assertEqual(response.status_code, 201)

    def test_paste_file_c(self):
        response = self.app.post('/', data={'c': (BytesIO(b"contents"),
            'test')})
        self.assertEqual(response.status_code, 201)
        j = json.loads(response.data.decode('utf-8'))
        self.failUnlessEqual(j.get('hashid'),
                '4a756ca07e9487f482465a99e8286abc86ba4dc7')

    def test_paste_file_c(self):
        response = self.app.post('/', data={'content': (BytesIO(b"contents"),
            'test')})
        self.assertEqual(response.status_code, 201)
        j = json.loads(response.data.decode('utf-8'))
        self.failUnlessEqual(j.get('hashid'),
                '4a756ca07e9487f482465a99e8286abc86ba4dc7')

    def test_paste_extension(self):
        response = self.app.post('/', data={'content': 'abc'})
        response = self.app.get('/1.txt')
        self.assertEqual(response.status_code, 200)

    def test_paste_highlight(self):
        response = self.app.post('/', data={'content': 'abc'})
        response = self.app.get('/1/txt')
        self.assertEqual(response.status_code, 200)

