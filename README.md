# JournalObservatory Database

## Graphdb

GraphDB [(website)](https://graphdb.ontotext.com/) is the triple-store backend for the JournalObservatory Project. It can be run on the free-tier. It provides a triple-store, sparql-endpoint and a graphical interface to manage the server.

### Deployment

GraphDB can be deployed using docker:
```shell
docker run \
    --name graphdb \
    --env GDB_HEAP_SIZE=4G \
    --publish 7200:7200 \
    --volume ./graphdb/graphdb.properties:/opt/graphdb/conf/graphdb.properties \
    --volume ./graphdb_data:/opt/graphdb/data/repositories \
    khaller/graphdb-free
```

Or using docker-compose and the `docker-compose.yml` file:
```
docker-compose up -d graphdb
```

### Configuration

`GDB_HEAP_SIZE` is the amount of memory that GraphDB may reserve for operations. If this property is set to too high a value, GraphDB can segfault on heavy queries. It is recommended to not set this to more than 2/3 of the total memory available on the server (less if there are more processes taking up memory besides the OS and GraphDB).

`graphdb_data` is the place where the database files are stored, if this mount-bind is not present, data will only be stored as long as the graphdb docker container is not removed or rebuilt.

`graphdb.properties` contains specific configuration variables for GraphDB (see [Documentation](https://graphdb.ontotext.com/documentation/10.2/directories-and-config-properties.html?highlight=properties#what-s-in-this-document)). In particular, to make the interface available on a custom domain, the `graphdb.vhosts` and `graphdb.external-url` properties need to be set to the url where the graphdb interface is available. `graphdb.workbench.cors.enable` needs to be enabled and `graphdb.workbench.cors.origin` set to the ip-adresses of hosts that can reach the interface (`*` for all adresses).

GraphDB

## PAD API

The PAD API is a [Flask](https://flask.palletsprojects.com) App that serves PADs over a REST API. It is meant to provide simple access to the PADs stored in the triple store, as a limited alternative to the SPARQL endpoint. The API has 2 modes:
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

The PAD API can be run in a python development environment by installing the requirements and serving the flask application.
```
pip install -r requirements.txt
PYTHONPATH="./pad_api/src" flask -A api.application:api --debug run --host "${APP_HOST}" --port "${APP_PORT}"
```

It can also be run in a docker container:
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
    --env APP_PAD_PREFIX=https://journalobservatory.org/pad/
    --publish "${APP_PORT}:${APP_PORT}"
    pad_api
```

Or using docker-compose and the `docker-compose.yml` file:
```
docker-compose build pad_api
docker-compose up -d pad_api
```

### Configuration

The app is configured with the `APP_` environment variables:

- `APP_ENVIRONMENT`: 'development' or 'production', when 'development' the app runs with `flask --debug` otherwise gunicorn is used. (default 'development')
- `APP_HOST`: On which interface the app is available. (default '0.0.0.0' - all interfaces)
- `APP_PORT`: On which port the app is available (default 5000)
- `APP_SPARQL_HOST`: Host part of the SPARQL endpoint (if the full SPARQL endpoint is 'http://sparqlserver.example/sparql/query' this should be 'http://sparqlserver.example')
- `APP_SPARQL_QUERY_PATH`: Path part of the SPARQL endpoint (if the full SPARQL endpoint is 'http://sparqlserver.example/sparql/query' this should be '/sparql/query')
- `APP_GLOBAL_LIMIT`: Maximum number of PADs on a single api page for the /pads path (default: 50)
- `APP_PAD_PREFIX`: Prefix for the pads that will be served by the api (default: 'https://journalobservatory.org/pad/')
