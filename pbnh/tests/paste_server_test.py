import os
import pbnh
import unittest
import tempfile

class PbnhTestCase(unittest.TestCase):

    def setUp(self):
        #self.db_fd, pbnh.app.config['DATABASE'] = tempfile.mkstemp()
        pbnh.app.app.config['TESTING'] = True
        self.app = pbnh.app.app.test_client()
        #pbnh.init_db()

    def tearDown(self):
        #os.close(self.db_fd)
        #os.unlink(pbnh.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/').status_code
        assert rv == 200

if __name__ == '__main__':
    unittest.main()
