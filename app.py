from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=["POST"])
def hello():
    print(request.data)
    print(request.form)
    print(request.stream)
    print(request.files)
    print(request.method)
    print(request.values)
    return "Hello World!"

if __name__ == "__main__":
        app.run('0.0.0.0', debug=True)
