import io
import json

from pbnh.db import paste
from datetime import datetime, timezone, timedelta

# we really need to put these into a config file
DATABASE = 'postgresql'
DBNAME = 'pastedb'

def fileData(files, addr=None, sunset=None, mime=None):
    try:
        buf = files.stream
        if buf and isinstance(buf, io.BytesIO) or isinstance(buf,
                io.BufferedRandom):
            data = buf.read()
            with paste.Paster(dialect=DATABASE, dbname=DBNAME) as pstr:
                j = pstr.create(data, mime=mime, ip=addr,
                        sunset=sunset)
                return json.dumps(j)
    except IOError as e:
        return 'caught exception in filedata' + str(e)
    return 'File save error'

def stringData(inputstr, addr=None, sunset=None, mime=None):
    with paste.Paster(dialect=DATABASE, dbname=DBNAME) as pstr:
        j = pstr.create(inputstr.encode('utf-8'), mime=mime, ip=addr, sunset=sunset)
        return json.dumps(j)
    return 'String save error'

def getSunsetFromStr(sunsetstr):
    if sunsetstr:
        try:
            plustime = int(sunsetstr)
            return datetime.now(timezone.utc) + timedelta(seconds=plustime)
        except ValueError:
            return None
    return None

def redirectData(redirect, addr=None, sunset=None):
    with paste.Paster(dialect=DATABASE, dbname=DBNAME) as pstr:
        j = pstr.create(redirect.encode('utf-8'), mime='redirect', ip=addr,
                sunset=sunset)
        return json.dumps(j)
