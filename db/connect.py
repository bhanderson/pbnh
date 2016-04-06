class DBConnect():
    """create db connection string"""
    def __init__(self, dialect=None, driver=None, username=None, password=None,
                 host=None, port=None, dbname=None):
        self._connect = dialect
        if driver:
            self._connect += '+' + driver
        self._connect += '://'
        if username:
            self._connect += username
            if password:
                self._connect += ':' + password
            self._connnect +='@'
        if host:
            self._connect += host
            if port:
                self._connect += ':' + port
        if dbname:
            self._connect += '/' + dbname

    @property
    def connect(self):
        """Connection string read-only property"""
        return self._connect
