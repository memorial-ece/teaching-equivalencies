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
* fuzzywuzzy
* levenshtein
* matplotlib
* peewee
* sqlite3


### Initialization

To initialize the database, run:

```sh
teq execute pt c (create)
```

Information about
[courses and course offerings](https://github.com/memorial-ece/course-data)
can then be imported:

```sh
teq intake <calendar_html_files>
teq populate <offering_descriptions>
```

Other steps that require further documentation include:

```sh
teq autovet (if you want it makes life easier for verification)
teq execute deficits
```
