from flask import Flask, request, Response, send_file
import magic
import io
import hashlib
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == 'POST':
        fs = request.files.get('c', 'content')
        if fs:
            # save the paste
            bytestream = fs.stream.getbuffer().tobytes()
            open('filename', 'wb').write(bytestream)
            # save the mimetype
            mime = magic.from_buffer(bytestream, mime=True)
            open('mime', 'wb').write(mime)
            return hashlib.sha1(bytestream).hexdigest() + '\n'
        return 'error'
    else:
        filename = 'filename'
        # open the file
        f = open(filename, 'rb').read()
        # read the mimetype of the file we saved
        mime = open('mime', 'r').read()
        # get the bytestream of the file
        binstream = io.BytesIO(f)
        return send_file(binstream, attachment_filename=filename, mimetype=mime)

if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
