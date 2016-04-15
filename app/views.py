import re

from flask import request, send_file, render_template, Response
import pygments
from pygments import highlight, util, formatters
from pygments.lexers import get_lexer_for_mimetype, get_lexer_for_filename
from sqlalchemy import exc
from werkzeug.datastructures import FileStorage

from db import paste
from app import app
from app import util

# we really need to put these into a config file
DATABASE = 'postgresql'
DBNAME = 'pastedb'

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == 'POST':
        inputstr = request.form.get('c')
        if inputstr and isinstance(inputstr, str): # we didn't get a file we got a string
            return util.stringdata(inputstr)

        files = request.files.get('c')
        if files and isinstance(files, FileStorage): # we got a file
            return util.filedata(files)
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
        except exc.DataError:
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
                    except pygments.util.ClassNotFound:
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

