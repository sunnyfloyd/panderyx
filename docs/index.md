# panderyx

[![Build Status](https://travis-ci.org/sunnyfloyd/panderyx.svg?branch=master)](https://travis-ci.org/sunnyfloyd/panderyx)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Panderyx is a web app prepared for self-hosting. It lets you build automated ETL pipelines and analytical workflows on tabular data.. Check out the project's [documentation](http://sunnyfloyd.github.io/panderyx/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)

# Initialize the project

Start the dev server for local development:

```bash
docker-compose up
```

Create a superuser to login to the admin:

```bash
docker-compose run --rm web ./manage.py createsuperuser
```
