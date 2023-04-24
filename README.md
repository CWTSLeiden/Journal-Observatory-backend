# Journal Observatory backend

## GraphDB

[GraphDB](https://graphdb.ontotext.com/) is the triplestore backend for the [Journal Observatory project](https://www.journalobservatory.org). It can be run on the free-tier. It provides a triplestore, SPARQL endpoint, and a graphical user interface to manage the server.

### Deployment

GraphDB can be deployed using Docker:
```shell
docker run \
    --name graphdb \
    --env GDB_HEAP_SIZE=12G \
    --publish 7200:7200 \
    --volume ./graphdb/graphdb.properties:/opt/graphdb/conf/graphdb.properties \
    --volume ./graphdb_data:/opt/graphdb/data/repositories \
    khaller/graphdb-free
```

Or using Docker Compose and the `docker-compose.yml` file:
```
docker-compose up -d graphdb
```

## PAD API

The PAD API is a [Flask](https://flask.palletsprojects.com) application that serves PADs over a REST API. It is meant to provide simple access to the PADs stored in the triplestore, as a limited alternative to the SPARQL endpoint. The API has two modes:
- `/api/pads`: Get a list of PADs based on an optional search query
- `/pad/<id>`: View a single pad in a `JSON-LD`, `Trig` or Graphical format

The documentation of the api can be found at `/apidocs`

### Deployment

The PAD API is configurable with the following environment variables:

- `APP_ENVIRONMENT`
- `APP_HOST`
- `APP_PORT`
- `APP_SPARQL_HOST`
- `APP_SPARQL_QUERY_PATH`
- `APP_GLOBAL_LIMIT`

The PAD API can be run in a python development environment by installing the requirements and serving the Flask application.
```
pip install -r requirements.txt
PYTHONPATH="./pad_api/src" flask -A api.application:api --debug run --host "${APP_HOST}" --port "${APP_PORT}"
```

It can also be run in a Docker container:
```
cd pad_api
docker build -t pad_api
docker run \
    --name pad_api
    --env APP_ENVIRONMENT=develop
    --env APP_HOST=0.0.0.0
    --env APP_PORT=5001
    --env APP_SPARQL_HOST=http://graphdb:7200
    --env APP_SPARQL_QUERY_PATH=/repositories/pad
    --env APP_GLOBAL_LIMIT=50
    --publish "${APP_PORT}:${APP_PORT}"
    pad_api
```

Or using Docker Compose and the `docker-compose.yml` file:
```
docker-compose up -d pad_api
```
