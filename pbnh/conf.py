import os
import yaml

path = os.path.expanduser(os.path.join('~', '.config', 'pbnh', 'config.yml'))
def get_config():
    with open (path) as config:
        return yaml.load(config)
