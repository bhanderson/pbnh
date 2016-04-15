#!/usr/bin/python3
import pycurl
import unittest
import json
import hashlib

URL = 'http://localhost:5001/'

class TestPost(unittest.TestCase):
    def setUp(self):
        self.c = pycurl.Curl()
        self.c.setopt(self.c.URL, URL)
        pass

    def tearDown(self):
        self.c.close()
        pass

    def test_hash_string(self):
        #c = pycurl.Curl()
        data = [('c', 'abc')]
        ret = []
        self.c.setopt(self.c.HTTPPOST, data)
        self.c.setopt(self.c.WRITEFUNCTION, ret.append)
        self.c.perform()
        r = ret.pop()
        self.failUnlessEqual(r, b'a9993e364706816aba3e25717850c26c9cd0d89d')

    def test_file_send(self):
        data = [('c', (pycurl.FORM_FILE, __file__))]
        self.c.setopt(self.c.HTTPPOST, data)
        ret = []
        self.c.setopt(self.c.WRITEFUNCTION, ret.append)
        self.c.perform()
        print(ret)
        r = json.loads(ret.pop().decode('utf-8'))
        f = open(__file__, 'r')
        filehash = hashlib.sha1(f.read().encode('utf-8')).hexdigest()
        self.failUnlessEqual(filehash, r.get('hashid'))
