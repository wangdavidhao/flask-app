# PDF Storage & Text extraction

## Project structure

    .
    ├── static                  #Basic styles
    │   └── styles.css
    │
    └── templates               #HTML templates
    │   ├── error.html
    │   ├── index.html
    │   ├── pdf_info.html
    │   └── pdf_text.html
    │
    └── tests                   #Tests
    │
    ├── __init__.py             #App entrypoint & modules
    ├── app.py
    ├── db.py
    ├── models.py
    └── routes.py

## Requirements

- Inside the requirements.txt file with the version dependencies

## Installation & Running

```bash
#With Docker
$ docker build -t flask-app .
$ docker run -p 5000:5000 flask-app
```

```bash
#With python3 locally
$ pip install -r requirements.txt
$ export FLASK_APP=__init__ #use SET for Windows machine
$ flask run
```

## Author

- WANG David - SIO CentraleSupélec david.wang@student-cs.fr
