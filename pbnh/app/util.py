import hashlib
import io
import json
import magic
import validators

from pbnh.db import paste
from datetime import datetime, timezone, timedelta

# we really need to put these into a config file
DATABASE = 'postgresql'
DBNAME = 'pastedb'

def fileData(files, addr=None, sunset=None):
    try:
        buf = files.stream
        if buf and isinstance(buf, io.BytesIO) or isinstance(buf,
                io.BufferedRandom):
            data = buf.read()
            mime = magic.from_buffer(data, mime=True)
            print(mime)
            with paste.Paster(dialect=DATABASE, dbname=DBNAME) as pstr:
                j = pstr.create(data, mime=mime.decode('utf-8'), ip=addr,
                        sunset=sunset)
                return json.dumps(j)
    except IOError as e:
        return 'caught exception in filedata' + str(e)
    return 'File save error, your file is probably too big'

def stringData(inputstr, addr=None, sunset=None):
    encoded = inputstr.encode('utf-8')
    return hashlib.sha1(encoded).hexdigest()

def redirectData(redirect, addr=None, sunset=None):
    with paste.Paster(dialect=DATABASE, dbname=DBNAME) as pstr:
        j = pstr.create(redirect.encode('utf-8'), mime='redirect', ip=addr,
                sunset=sunset)
        return json.dumps(j)

def getSunsetFromStr(sunsetstr):
    if sunsetstr:
        try:
            plustime = int(sunsetstr)
            return datetime.now(timezone.utc) + timedelta(seconds=plustime)
        except ValueError:
            return None
    return None
