pbnh
========
[![MIT License](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Issue Stats](http://issuestats.com/github/bhanderson/pbnh/badge/issue?style=flat)](http://issuestats.com/github/bhanderson/pbnh)
pbnh is our implementation of a pastebin server using flask and postgres or sqlite

It is highly derived from [silverp1's](https://github.com/silverp1) and [buhman's](https://github.com/buhman) project [pb](https://github.com/ptpb/pb) and they deserve the recognition for this idea.

The syntax highlighting is done using [codemirrors](https://github.com/codemirror/codemirror) javascript library.

The icons are from [Font Awesome](https://fortawesome.github.io/Font-Awesome/)

pbnh requires Python3

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

## Installation
Note, psycopg2 is a C extension module for postgres. You can grab the dependencies by either installing python-psycopg2 from your package manager, or grab libpq-dev as well as python3-dev and gcc if you don't already have them.

pycurl (needed for unit tests) seems to depend on libcurl4-gnutls-dev, librtmp-dev, libgnutls-dev

To install the pbnh package:
```
$ git clone https://github.com/bhanderson/pbnh.git
$ cd pbnh
$ pip install .
```

## Configuration
To configure pbnh, copy the sample config to ~/.config/pbnh/config.yml and edit it as desired. You can also use the default config in conf.py.

To configure postgres (assuming debian/ubuntu, other distros should be similar):
```
# apt-get install postgres
# su - postgres
$ createuser -s $USERNAME
python3 db/createdb.py
```

## Usage
You can create pastes with the webui or though the cli using curl. Currently the only way to upload anything other than text or a redirect is through the cli.

Curl has an option for a form id, you can use c or content to specify the contents of a paste.
```
curl -F content=@file.txt servername.com
```
Or you can cat a file
```
cat file.txt | curl -F c=@- servername.com
```
We also support strings
```
curl -F content="hello world!" servername.com
```
To upload a redirect change the form id to r
```
curl -F r="https://www.google.com" servername.com
```
There are three different inputs allowed in a curl command they are content, sunset, and mime. Sunset and Mime are optional.
### content or c
The content is exactly what it sounds like. The content of the file or the string data you want to paste and can be seen in the examples above.
### sunset
The sunset is the amount of time you want this paste to be available. If sunset is specified you may specify for it to last a maximum of 24 hours. If unspecified the sunset value is 0 and the paste will not be removed.

Currently there is no support for deleting pastes after you create them with a sunset. The sunset is set but no process is cleaning them up.
```
curl -F content=@file.txt -F sunset=10 servername.com
```
### mime
The mime type is the type of file. If you want automatic syntax highlighting through the webui or want an image to be displayed you can set the mimetype.
The default is plain text, pbnh uses [python-magic](https://github.com/ahupp/python-magic) to attempt to guess the buffer mimetype if none is specified.
A list of mimetypes can be found [here](http://www.freeformatter.com/mime-types-list.html). Only specify the second half of the mimetype.
For example for the mimetype 'application/pdf' only specify pdf.
```
curl -F content=@file.txt -F mime=plain servername.com
```
## Tests
To install the dependencies required for running tests, simply run
```
pip install -r tests_require.txt
```
Tests can be ran by running nosetests in the pbnh directory or by specifying a specific test

## Dependency
#TODO
