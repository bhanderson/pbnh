from app import app
import conf
conf = conf.get_config().get('server')
app.run(conf.get('bind_ip'), port=conf.get('bind_port'), debug=conf.get('debug'))
