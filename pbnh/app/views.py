import io
import json
import yaml

from datetime import datetime, timezone, timedelta
from docutils.core import publish_parts
from flask import abort, redirect, render_template, Response, request
from flask import send_file, send_from_directory
from os.path import realpath, dirname, join, expanduser
from sqlalchemy import exc
from werkzeug.datastructures import FileStorage

from pbnh.app import app
from pbnh.app import util

SITE_ROOT = realpath(dirname(__file__))


CONFIG = {}
try:
    # This is basically the dev config file, this is the path
    # that docker-compose is using for secrets
    with open(expanduser('~/.config/.pbnh.yml')) as f:
        CONFIG = yaml.load(f)
except OSError:
    try:
        # This is basically the prod config file, this is the path that a
        # docker container will pull its config from if secrets are
        # configured right.
        with open('/run/secrets/secrets.yml') as f:
            CONFIG = yaml.load(f)
    except OSError:
        try:
            # As a final fallback, try checking the local dir
            with open('secrets.yml') as f:
                CONFIG = yaml.load(f)
        except OSError:
            # should probalt log instead of print. Whatever
            print('no configuration files found')

app.config['CONFIG'] = CONFIG


@app.route("/", methods=["GET"])
def hello():
    return render_template('index.html')


@app.route("/about.md", methods=["GET"])
def about():
    with open(join(SITE_ROOT, 'static', 'about.md'), 'r') as aboutfile:
        data = aboutfile.read()
    return render_template('markdown.html', paste=data)


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory('static', path)


@app.route("/", methods=["POST"])
def post_paste():
    if request.headers.getlist("X-Forwarded-For"):
        addr = request.headers.getlist("X-Forwarded-For")[0]
    else:
        addr = request.remote_addr
    sunsetstr = request.form.get('sunset')
    mimestr = request.form.get('mime')
    sunset = util.getSunsetFromStr(sunsetstr)
    redirectstr = request.form.get('r') or request.form.get('redirect')
    if redirectstr:
        j = util.stringData(redirectstr, addr=addr, sunset=sunset,
                            mime='redirect')
        if j:
            if isinstance(j, str):
                return j
            j['link'] = request.url + str(j.get('hashid'))
        return json.dumps(j), 201
    inputstr = request.form.get('content') or request.form.get('c')
    # we got string data
    if inputstr and isinstance(inputstr, str):
        try:
            j = util.stringData(inputstr, addr=addr, sunset=sunset,
                                mime=mimestr)
            if j:
                j['link'] = request.url + str(j.get('hashid'))
            return json.dumps(j), 201
        except (exc.OperationalError, exc.InternalError):
            abort(500)
    files = request.files.get('content') or request.files.get('c')
    # we got file data
    if files and isinstance(files, FileStorage):
        try:
            j = util.fileData(files, addr=addr, sunset=sunset, mimestr=mimestr)
            if j:
                if isinstance(j, str):
                    return j
                j['link'] = request.url + str(j.get('hashid'))
            return json.dumps(j), 201
        except (exc.OperationalError, exc.InternalError):
            abort(500)
    abort(400)


@app.route("/<string:paste_id>", methods=["GET"])
def view_paste(paste_id):
    """
    If there are no extensions or slashes check if the mimetype is text, if it
    is text attempt to highlight it. If not return the data and set the
    mimetype so the browser can attempt to render it.
    """
    query = util.getPaste(paste_id)
    if not query:
        abort(404)
    mime = query.get('mime')
    data = query.get('data')
    if mime == 'redirect':
        return redirect(data.decode('utf-8'), code=302)
    if mime.startswith('text/'):
        return render_template('paste.html', paste=data.decode('utf-8'),
                               mime=mime)
    else:
        data = io.BytesIO(query.get('data'))
        return send_file(data, mimetype=mime)


@app.route("/<string:paste_id>.<string:filetype>")
def view_paste_with_extension(paste_id, filetype):
    query = util.getPaste(paste_id)
    if not query:
        abort(404)
    if filetype == 'md':
        data = query.get('data').decode('utf-8')
        return render_template('markdown.html', paste=data)
    if filetype == 'rst':
        data = query.get('data').decode('utf-8')
        return Response(publish_parts(data, writer_name='html')['html_body'])
    if filetype == 'asciinema':
        # Prepare query params such that
        # {{params|tojson}} produces a valid JS object:
        params = {}
        for key, value in request.args.to_dict().items():
            try:
                params[key] = json.loads(value)
            except json.JSONDecodeError:
                params[key] = str(value)
        return render_template(
            'asciinema.html',
            pasteid=paste_id,
            params=params,
        )
    data = io.BytesIO(query.get('data'))
    mime = util.getMime(mimestr=filetype)
    return Response(data, mimetype=mime)


@app.route("/<string:paste_id>/<string:filetype>")
def view_paste_with_highlighting(paste_id, filetype):
    if not filetype:
        filetype = 'txt'
    query = util.getPaste(paste_id)
    if not query:
        abort(404)
    data = query.get('data')
    try:
        return render_template('paste.html', paste=data.decode('utf-8'),
                               mime=filetype)
    except UnicodeDecodeError:
        return abort(500)


@app.route("/error")
@app.errorhandler(404)
def fourohfour(e=None):
    return render_template('404.html'), 404
