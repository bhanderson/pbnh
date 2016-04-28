#!/usr/bin/python3
import pycurl
import unittest
import json
import hashlib
import tempfile
import os

from pbnh import conf
from pbnh import app
from pbnh.db.createdb import CreateDB

config = conf.get_config().get('server')
host = config.get('bind_ip')
port = config.get('bind_port')
URL = 'http://{}:{}/'.format(host, port)


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
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.URL, URL)
        self.newdb = CreateDB(dialect=DEFAULTS['database']['dialect'],
                dbname=DEFAULTS['database']['dbname'])
        self.newdb.create()
        app.app.config['CONFIG'] = DEFAULTS
        self.app = app.app.test_client()

    def tearDown(self):
        self.c.close()

    def test_one(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_two(self):
        response = self.app.get('/1')
        self.assertEqual(response.status_code, 200)

"""
    def test_hash_string(self):
        #c = pycurl.Curl()
        data = [('content', 'abc')]
        ret = []
        self.c.setopt(pycurl.HTTPPOST, data)
        self.c.setopt(pycurl.WRITEFUNCTION, ret.append)
        self.c.perform()
        r = ret.pop()
        self.failUnlessEqual(r, b'a9993e364706816aba3e25717850c26c9cd0d89d')

    def test_file_send(self):
        data = [('content', (pycurl.FORM_FILE, __file__))]
        self.c.setopt(pycurl.HTTPPOST, data)
        ret = []
        self.c.setopt(pycurl.WRITEFUNCTION, ret.append)
        self.c.perform()
        #print(ret)
        r = json.loads(ret.pop().decode('utf-8'))
        f = open(__file__, 'r')
        filehash = hashlib.sha1(f.read().encode('utf-8')).hexdigest()
        self.failUnlessEqual(filehash, r.get('hashid'))
        return r

    def test_get_file(self):
        # verify the file exists
        r = self.test_file_send()
        ret = []
        #print(r)
        id = r.get('id')
        self.c.reset() # we need this for some dumb reason
        self.c.setopt(pycurl.URL, URL + str(id) + '.raw')
        self.c.setopt(pycurl.WRITEFUNCTION, ret.append)
        self.c.perform()
        self.failUnless(ret)
        self.failUnlessEqual(hashlib.sha1(ret[0]).hexdigest(), r.get('hashid'))

    def test_get_file_with_hash(self):
        #not working anyways
        pass

    def test_set_and_get_redirect(self):
        ret = []
        testurl = 'http://abcdefgjikl.xyz'
        data = [('r', testurl)]
        self.c.setopt(pycurl.HTTPPOST, data)
        self.c.setopt(pycurl.WRITEFUNCTION, ret.append)
        self.c.perform()
        if ret:
            r = json.loads(ret.pop().decode('utf-8'))
            self.c.reset()
            self.c.setopt(pycurl.URL, URL + str(r.get('id')))
            self.c.setopt(pycurl.WRITEFUNCTION, ret.append)
            self.c.perform()
            self.failUnless(testurl in ret.pop().decode('utf-8'))
        else:
            self.fail()
"""
