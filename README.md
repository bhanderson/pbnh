# pbnh
mix between pb and haste

Note, psycopg2 is a C extension module. You can grab the dependencies by either installing python-psycopg2 from your package manager, or grab libpq-dev as well as python3-dev and gcc if you don't already have them.

To configure postgres (assuming debian/ubuntu, other distros should be similar):
```
# apt-get install postgres
# su - postgres
$ createuser -s $USERNAME
python3 db/createdb.py -t postgresql -d testdb
```
