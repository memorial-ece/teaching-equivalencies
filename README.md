# teq: teaching equivalencies database

This software is used to track teaching loads and course equivalencies for
instructors at Memorial University.

## Getting started

To initialize the database, run:

```sh
./Startup.py execute pt c (create)
```

Information about
[courses and course offerings](https://github.com/memorial-ece/course-data)
can then be imported:

```sh
./Startup.py intake <calendar_html_files>
./Startup.py populate <offering_descriptions>
```

Other steps that require further documentation include:

```sh
./Startup.py autovet (if you want it makes life easier for verification)
./Startup.py execute deficits
```
