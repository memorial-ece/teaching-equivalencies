# teq: teaching equivalencies database

This software is used to track teaching loads and course equivalencies for
instructors at Memorial University.

## Getting started

### Dependencies

The following Python packages are required dependencies:

* beautifulsoup
* colorama
* docopt
* flask
* flask-bootstrap
* flask-nav
* flask-wtf
* Flask-DotEnv
* fuzzywuzzy
* levenshtein
* matplotlib
* numparser
* peewee
* psycopg2
* python-dotenv (*not* `dotenv`)
* requests
* sqlite3


### Initialization

To initialize the database, run:

```sh
teq initdb
```

Information about instructors,
[courses and course offerings](https://github.com/memorial-ece/course-data)
can then be imported:

```sh
teq import people http://www.mun.ca/engineering/about/people
teq import courses <calendar_html_files>
teq import offerings <offering_descriptions>
```


### Web server

To run the Web server in local (debug) mode, run:

```sh
teq serve
```

In production, the Web server should be run as a WSGI application.
