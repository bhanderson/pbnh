from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=["POST"])
def hello():
    print(request.files)
    print(request.headers)
    print(request.url)
    print(request.url_root)
    fs = request.files.get('c', 'content')
    if fs:
        print(fs.read())
        print(fs.stream)
    return "Hello World!"

if __name__ == "__main__":
        app.run('0.0.0.0', debug=True)
