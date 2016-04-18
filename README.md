# pbnh
mix between pb and haste

Note, psycopg2 is a C extension module. You can grab the dependencies by either installing python-psycopg2 from your package manager, or grab libpq-dev as well as python3-dev and gcc if you don't already have them.

pycurl (needed for unit tests) seems to depend on libcurl4-gnutls-dev librtmp-dev

To configure postgres (assuming debian/ubuntu, other distros should be similar):
```
# apt-get install postgres
# su - postgres
$ createuser -s $USERNAME
python3 db/createdb.py -t postgresql -d pastedb
```

To install the pbnh package:
```
$ git clone https://github.com/bhanderson/pbnh.git
$ cd pbnh
$ pip install -e .
```
