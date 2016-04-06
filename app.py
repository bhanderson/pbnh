#!/bin/env/python
from flask import Flask, request, Response, send_file, render_template, redirect
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer
from pygments.lexers import guess_lexer
import hashlib
import io
import magic
from urllib.parse import urlparse
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == 'POST':
        fs = request.files.get('c', 'content')
        if fs and not type(fs) is str:
            # save the paste
            bytestream = fs.stream.getbuffer().tobytes()
            open('filename', 'wb').write(bytestream)
            # save the mimetype
            mime = magic.from_buffer(bytestream, mime=True)
            open('mime', 'wb').write(mime)
            print(mime)
            return hashlib.sha1(bytestream).hexdigest() + '\n'
        else:
            url = request.form.get('c', 'content')
            o = urlparse(url)
            print(o.geturl())
            pass
            return redirect(o.geturl(), code=302)
        return 'error'
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

if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
