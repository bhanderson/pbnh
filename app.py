#!/bin/env/python
import hashlib
import io
import json
import magic
import validators
import re

from flask import Flask, request, send_file, render_template, redirect, Response
from pygments import highlight, util, formatters
from pygments.lexers import get_lexer_for_mimetype, get_lexer_for_filename
from sqlalchemy import exc
from werkzeug.datastructures import FileStorage

from db import paste

app = Flask(__name__)

DATABASE = 'postgresql'
DBNAME = 'pastedb'
DEBUG = True

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
    if validators.url(inputstr): # the string is a url return a redirect
        return redirect(inputstr, code=302)
    encoded = inputstr.encode('utf-8')
    return hashlib.sha1(encoded).hexdigest()

def returnfile():
    f = open('outfile', 'rb').read()
    mime = open('mime', 'r').read()
    if mime.split('/')[0] == 'text':
        result = highlight(f, get_lexer_for_mimetype(mime),
                           formatters.HtmlFormatter(linenos=True, full=True,
                                                    style='colorful'))
        return render_template('paste.html', paste=result)
    binstream = io.BytesIO(f)
    return send_file(binstream, mimetype=mime)

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == 'POST':
        inputstr = request.form.get('c')
        if inputstr and isinstance(inputstr, str): # we didn't get a file we got a string
            return stringdata(inputstr)

        files = request.files.get('c')
        if files and isinstance(files, FileStorage): # we got a file
            return filedata(files)
    else:
        return 'welcome try to curl a paste:<br>cat filename | curl -F c=@- server'
    print(request.form)
    print(request.files)
    print('fell through')
    return 'fell through'

@app.route("/<string:paste_id>")
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
            if mime[:4] == 'text':
                if not filetype:
                    lexer = get_lexer_for_mimetype(mime)
                else:
                    try:
                        lexer = get_lexer_for_filename(filetype)
                    except util.ClassNotFound:
                        return Response(data, mimetype='text/plain')
                html = highlight(data, lexer,
                                 formatters.HtmlFormatter(style='colorful',
                                                          full=True,
                                                          linenos=True))
                return render_template('paste.html', paste=html)
            data = io.BytesIO(query.get('data'))
            return send_file(data, mimetype=mime)
        if not hashid:
            return view_paste(paste_id, filetype, hashid=True)
        return 'Error: paste not found'

@app.route("/<int:paste_id>.<string:filetype>")
def view_paste_with_extension(paste_id, filetype):
    return view_paste(paste_id, "file." + filetype)

if __name__ == "__main__":
    app.run('0.0.0.0', port=5001, debug=DEBUG)
