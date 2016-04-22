import io
import re
import pygments

from flask import request, send_file, render_template, Response
from pygments import highlight, util, formatters
from pygments.lexers import get_lexer_for_mimetype, get_lexer_for_filename
from sqlalchemy import exc
from werkzeug.datastructures import FileStorage
from datetime import datetime, timezone, timedelta


from pbnh import conf
from pbnh.db import paste
from pbnh.app import app
from pbnh.app import util

config = conf.get_config()
DATABASE = config.get('database').get('dialect')
DBNAME = config.get('database').get('dbname')

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == 'POST':
        addr = request.remote_addr
        # First check c for paste content
        inputstr = request.form.get('c')
        sunsetstr = request.form.get('sunset')
        sunset = None
        if sunsetstr:
            sunset = int(sunsetstr)
        if sunset and isinstance(sunset, int):
            sunset = datetime.now(timezone.utc) + timedelta(seconds=sunset)
        if inputstr and isinstance(inputstr, str): # we didn't get a file we got a string
            return util.stringdata(inputstr, addr=addr, sunset=sunset)

        files = request.files.get('c')
        if files and isinstance(files, FileStorage): # we got a file
            return util.filedata(files, addr=addr, sunset=sunset)
        print(request.form.get('r'))
        # Next check r for redirect info. this should only be string info, not a
        # file
        redirect = request.form.get('r')
        if redirect:
            return util.redirectdata(redirect, addr=addr, sunset=sunset)
    else:
        return 'welcome try to curl a paste:<br>cat filename | curl -F c=@- server'
    print(request.form)
    print(request.files)
    print('fell through')
    return 'fell through'

@app.route("/<string:paste_id>", methods=["GET"])
def view_paste(paste_id, filetype=None, hashid=False):
    if not re.match("^[A-Za-z0-9_-]*$", str(paste_id)):
        return "invalid extension"
    with paste.Paster(dialect=DATABASE, dbname=DBNAME) as pstr:
        try:
            query = pstr.query(id=paste_id)
        except ValueError:
            query = pstr.query(hashid=paste_id)
        if query:
            mime = query.get('mime')
            data = query.get('data')
            if mime == 'redirect':
                return redirect(data)
            if mime[:4] == 'text':
                print(mime[5:])
                if not filetype:
                    lexer = get_lexer_for_mimetype(mime)
                else:
                    try:
                        lexer = get_lexer_for_filename(filetype)
                    except pygments.util.ClassNotFound:
                        return Response(data, mimetype='text/plain')
                html = highlight(data, lexer,
                                 formatters.HtmlFormatter(style='colorful',
                                                          full=True,
                                                          linenos=True))
                #return render_template('paste.html', paste=html)
                return render_template('paste.html', paste=data.decode('utf-8'), mime=mime[5:])
            data = io.BytesIO(query.get('data'))
            return send_file(data, mimetype=mime)
        if not hashid:
            return view_paste(paste_id, filetype, hashid=True)
        return 'Error: paste not found'

@app.route("/<int:paste_id>.<string:filetype>")
def view_paste_with_extension(paste_id, filetype):
    return view_paste(paste_id, "file." + filetype)

