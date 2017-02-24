from pbnh.app import app
from pbnh.db import createdb
import yaml
import os

psql_user = os.environ.get('PBNH_PSQL_USER')
psql_pass = os.environ.get('PBNH_PSQL_PASS')
psql_host = os.environ.get('PBNH_PSQL_HOST')
psql_port = os.environ.get('PBNH_PSQL_PORT')
psql_name  = os.environ.get('PBNH_PSQL_NAME')

pbnh_port = os.environ.get('PBNH_PORT')
pbnh_host = os.environ.get('PBNH_HOST')
pbnh_debug = bool(os.environ.get('PBNH_DEBUG'))
pbnh_dialect = 'postgresql'

if not psql_user or not psql_pass or not psql_host or not psql_port or not psql_name or not pbnh_port or not pbnh_host:
    print("Error with database variables")
    exit(-1)

# create a db if there isnt one there
newdb = createdb.CreateDB(dialect=pbnh_dialect, username=psql_user,
        password=psql_pass,host=psql_host,port=psql_port,dbname=psql_name)
try:
    newdb.create()
except:
    pass



app.config['CONFIG'] = {
'database': {
        'dialect': pbnh_dialect,
        'driver': None,
        'username': psql_user,
        'password': psql_pass,
        'host': psql_host,
        'port': psql_port,
        'dbname': psql_name,
        }
}

app.run(pbnh_host, port=int(pbnh_port), debug=pbnh_debug)
