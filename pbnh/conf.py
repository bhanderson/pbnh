import copy
import os
import yaml

PATH = (os.getcwd(),
        os.path.expanduser(os.path.join('~', '.config', 'pbnh')),
        os.path.join('etc', 'pbnh'))

DEFAULTS = {
    "server": {
        "bind_ip": "127.0.0.1",
        "bind_port": 8080,
        "debug": True,
    },
    "database": {
        "dbname": "pastedb",
        "dialect": "sqlite",
        "driver": None,
        "host": None,
        "password": None,
        "port": None,
        "username": None
    }
}

class FileNotFound(Exception):
    pass


def find_file(filename):
    for directory in PATH:
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            return filepath
    raise FileNotFound(filename, PATH)


def get_config():
    try:
        with open(find_file('config.yml'), 'r') as config:
            return yaml.load(config)
    except FileNotFound:
        return copy.copy(DEFAULTS)
