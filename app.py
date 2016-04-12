#!/bin/env/python
from flask import Flask, request, send_file, render_template, redirect
from pygments import highlight, util
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_mimetype, guess_lexer, get_lexer_for_filename
from werkzeug.datastructures import FileStorage
import hashlib
import io
import magic
import validators
import json
from db import paste
app = Flask(__name__)

DATABASE='postgresql'
DEBUG=True

def filedata(fs):
    try:
        buf = fs.stream
        if buf and isinstance(buf, io.BytesIO):
            data = buf.read()
            mime = magic.from_buffer(data, mime=True)
            print(mime)
            with paste.Paster(dialect=DATABASE) as p:
                j = p.create(data,mime=mime.decode('utf-8'))
                if j.get('id') == 'HASH COLLISION':
                    q = p.query(hashid=j.get('hashid'))
                    d = {'id': q.get('id'), 'hashid': q.get('hashid')}
                    return json.dumps(d)
                return json.dumps(j)
        if buf and isinstance(buf, io.BufferedRandom):
            with paste.Paster(dialect=DATABASE) as p:
                return json.dumps(p.create(buf))
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
                           HtmlFormatter(linenos=True, full=True,
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

@app.route("/<int:paste_id>")
def view_paste(paste_id, filetype=None):
    with paste.Paster(dialect=DATABASE) as p:
        query = p.query(id=paste_id)
        if query:
            mime = query.get('mime')
            print(mime)
            if mime[:4] == 'text':
                if not filetype:
                    lexer = get_lexer_for_mimetype(mime)
                else:
                    try:
                        lexer = get_lexer_for_filename(filetype)
                    except util.ClassNotFound:
                        lexer = get_lexer_for_mimetype(mime)
                html = highlight(query.get('data'), lexer,
                HtmlFormatter(style='colorful', full=True, linenos=True))
                return render_template('paste.html', paste=html)
            f = io.BytesIO(query.get('data'))
            return send_file(f, mimetype=mime)
        return 'Error: paste not found'

@app.route("/<int:paste_id>.<string:filetype>")
def view_paste_with_extension(paste_id, filetype):
    return view_paste(paste_id, "file." + filetype)

if __name__ == "__main__":
    app.run('0.0.0.0', port=5001, debug=DEBUG)
