# pbnh
pbnh is our implementation of a pastebin server using flask and postgres or sqlite

It is highly derived from [silverp1's](https://github.com/silverp1) and [buhman's](https://github.com/buhman) project [pb](https://github.com/ptpb/pb) and they deserve the recognition for this idea.

## Table of Contents
 * [pbnh](#pbnh)
 * [Table of contents](#table-of-contents)
 * [Installation](#installation)
 * [Usage](#usage)
    * [Post](#post)
        * [Content](#content)
        * [Sunset](#sunset)
        * [Mime](#mime)
 * [Tests](#tests)
 * [Dependency](#dependency)
 * 

## Installation
Note, psycopg2 is a C extension module. You can grab the dependencies by either installing python-psycopg2 from your package manager, or grab libpq-dev as well as python3-dev and gcc if you don't already have them.

pycurl (needed for unit tests) seems to depend on libcurl4-gnutls-dev, librtmp-dev, libgnutls-dev

To configure postgres (assuming debian/ubuntu, other distros should be similar):
```
# apt-get install postgres
# su - postgres
$ createuser -s $USERNAME
python3 db/createdb.py -t postgresql -n pastedb
```

To install the pbnh package:
```
$ git clone https://github.com/bhanderson/pbnh.git
$ cd pbnh
$ pip install -e .
```

## Usage
Currently the only way to use pbnh is with curl
```
curl -F content=@file.txt servername.com
```
Or you can cat a file
```
cat file.txt | curl -F content=@- servername.com
```
We also support strings
```
curl -F content="hello world!" servername.com
```
There are three different inputs allowed in a curl command they are content, sunset, and mime. Sunset and Mime are optional.
### Content
Content is exactly what it sounds like. The content of the file or the string data you want to paste and can be seen in the examples above.
### Sunset
Sunset is the amount of time you want this paste to be available. If sunset is specified you may specify for it to last a maximum of 24 hours. If unspecified the sunset value is 0 and the paste will not be removed.
```
curl -F content=@file.txt -F sunset=10 servername.com
```
### Mime
The mime type is how the file should be displayed. If text with highlighting, or if a file as an image. The default is plain text. A list of mimetypes can be found [here](http://www.freeformatter.com/mime-types-list.html). only specify the second half of the mimetype.
For example for the mimetype 'application/pdf' only specify pdf.
```
curl -F content=@file.txt -F mime=plain servername.com
```
## Tests
Tests can be ran by running nosetests in the pbnh directory or by specifying a specific test

## Dependency
#TODO
