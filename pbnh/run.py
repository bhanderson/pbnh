from pbnh.app import app
import yaml

config = {}
with open('secrets.yml') as f:
    config = yaml.load(f)

app.config['CONFIG'] = config
if config:
    app.run(config.get('server').get('bind_ip'),
    port=config.get('server').get('bind_port'))
else:
    exit(1)
