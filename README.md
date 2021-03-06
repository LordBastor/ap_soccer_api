# Django DRF Boilerplate

Boilerplate project using Django and Django REST Framework.
Currently supporting only Python 3.x.

**IMPORTANT**:
Docker Compose is used _just_ for development environment. The Dockerfile works without it.

## How to install with Pyenv

```bash
$ pyenv virtualenv 3.8.0 <project_name>
$ pyenv activate <project_name>
$ pip install Django==2.2.7
$ django-admin.py startproject \
  --template=https://github.com/CheesecakeLabs/django-drf-boilerplate/archive/master.zip \
  <project_name> .
$ pip install -r requirements/dev.txt
$ python src/manage.py runserver
```

## How to install with Docker Compose

```bash
$ django-admin.py startproject \
  --template=https://github.com/CheesecakeLabs/django-drf-boilerplate/archive/master.zip \
  <project_name> .
$ docker-compose up
```

## Install Black code formatter to your editor

Check code syntax and style before committing changes.

Or run it manually:

```bash
$ black .
```

## Database

Running database on latest PostgreSQL Docker container running in the port `5432`. The connection is defined by the `dj-database-url` package. There's a race condition script to avoid running Django before the database goes up.

## Docs

Let's face it, human memory sucks. Will you remember every detail that involves your project 6 months from now? How about when the pressure is on? A project with good documentation that explains all the facets, interactions and architectural choices means you and your teammates won't have to spend hours trying to figure it out later. You can find a template to get started [here](https://github.com/CheesecakeLabs/django-drf-boilerplate/wiki/Docs-Template).
