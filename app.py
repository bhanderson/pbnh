from flask import Flask, request, Response, send_file
import io
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == 'POST':
        print(request.files)
        print(request.headers)
        print(request.url)
        print(request.url_root)
        fs = request.files.get('c', 'content')
        if fs:
            #print(fs.stream)
            open('filename', 'wb').write(fs.stream.getbuffer())
        return "Hello World!"
    else:
        filename = 'filename'
        return send_file(io.BytesIO(io.open(filename, 'rb').read()),
                attachment_filename=filename,mimetype='image/png')

if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
