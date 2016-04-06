#!/bin/env/python
from flask import Flask, request, send_file, render_template, redirect
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_mimetype
from werkzeug.datastructures import FileStorage
import hashlib
import io
import magic
import validators
import json
from db import paste
app = Flask(__name__)

def filedata(fs):
    try:
        buf = fs.stream
        print(type(buf))
        if buf and isinstance(buf, io.BytesIO):
            data = buf.read()
            mime = magic.from_buffer(data, mime=True)
            with paste.Paster() as p:
                return json.dumps(p.create(data, mime=mime))
        return None
        if buf and isinstance(buf, io.BufferedRandom):
            with paste.Paster() as p:
                return json.dumps(p.create(buf))
            return 'working'
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
        print("get")
        return returnfile()
    print(request.form)
    print(request.files)
    print('fell through')
    return 'fell through'

@app.route("/a")
def getthisshit():
    with paste.Paster() as p:
        return p.query(id=1).get('data')

"""
    if request.method == 'POST':
    else:
        filename = 'filename'
        # open the file
        f = open(filename, 'rb').read()
        # read the mimetype of the file we saved
        mime = open('mime', 'r').read()
        # get the bytestream of the file
        binstream = io.BytesIO(f)
        if mime == 'text/plain':
            lexer = guess_lexer(f.decode("utf-8"))
            #print(lexer)
            html = highlight(f, lexer, HtmlFormatter(style='colorful'))
            print(html)
            return render_template('paste.html', paste=html)
            pass
        else:
            return send_file(binstream, attachment_filename=filename, mimetype=mime)
"""
if __name__ == "__main__":
    app.run('0.0.0.0', port=5001, debug=True)
