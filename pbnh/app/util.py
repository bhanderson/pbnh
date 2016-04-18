import hashlib
import io
import json
import magic
import validators

from pbnh.db import paste

# we really need to put these into a config file
DATABASE = 'postgresql'
DBNAME = 'pastedb'

def filedata(files):
    try:
        buf = files.stream
        if buf and isinstance(buf, io.BytesIO):
            data = buf.read()
            mime = magic.from_buffer(data, mime=True)
            print(mime)
            with paste.Paster(dialect=DATABASE, dbname=DBNAME) as pstr:
                j = pstr.create(data, mime=mime.decode('utf-8'))
                return json.dumps(j)
        if buf and isinstance(buf, io.BufferedRandom):
            with paste.Paster(dialect=DATABASE, dbname=DBNAME) as pstr:
                data = buf.read()
                mime = magic.from_buffer(data, mime=True)
                return json.dumps(pstr.create(data, mime=mime.decode('utf-8')))
    except IOError as e:
        return 'caught exception in filedata' + str(e)
    return 'File save error, your file is probably too big'

def stringdata(inputstr):
    encoded = inputstr.encode('utf-8')
    return hashlib.sha1(encoded).hexdigest()
