import io
import json
import magic
import mimetypes

from pbnh import conf
from pbnh.db import paste
from pbnh import conf
from datetime import datetime, timezone, timedelta

config = conf.get_config().get('database')

def fileData(files, addr=None, sunset=None, mimestr=None):
    try:
        buf = files.stream
        if buf and isinstance(buf, io.BytesIO) or isinstance(buf,
                io.BufferedRandom):
            data = buf.read()
            mime = getMime(data=data, mimestr=mimestr)
            with paste.Paster(dialect=config.get('dialect'), dbname=config.get('dbname'),
                              driver=config.get('driver'), host=config.get('host'),
                              password=config.get('password'), port=config.get('port'),
                              username=config.get('username')) as pstr:
                print(pstr.__dict__)
                j = pstr.create(data, mime=mime, ip=addr,
                                sunset=sunset)
                return json.dumps(j)
    except IOError as e:
        return 'caught exception in filedata' + str(e)
    return 'File save error'

def stringData(inputstr, addr=None, sunset=None, mime=None):
    with paste.Paster(dialect=config.get('dialect'), dbname=config.get('dbname'),
		      driver=config.get('driver'), host=config.get('host'),
		      password=config.get('password'), port=config.get('port'),
		      username=config.get('username')) as pstr:
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

def getMime(data=None, mimestr=None):
    if mimestr:
        return mimetypes.guess_type('file.{0}'.format(mimestr))[0]
    elif data:
        return magic.from_buffer(data, mime=True).decode('utf-8')
    return 'text/plain'

def getPaste(paste_id):
    with paste.Paster(dialect=DATABASE, dbname=DBNAME) as pstr:
        try:
            return pstr.query(id=paste_id)
        except ValueError:
            return None
        try:
            return pstr.query(hashid=paste_id)
        except ValueError:
            return None
    return None
