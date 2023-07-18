## installation

initial setup virtual environment:
```bash
$ python3 -m venv venv
$ . venv/bin/activate

$ pip install -r requirements.txt
```

## run venv

```bash
$ . venv/bin/activate
```

## setup config file

```bash
$ mkdir instance
$ cp config.example.json instance/config.json
```
edit instance/config.json and change SECRET_KEY value


## setup database

```bash
$ alembic upgrade head
```

## add migration

```bash
$ alembic revision -m "describe migration here" --autogenerate
```


## running server

```bash
$ flask --app src run --debug
```
