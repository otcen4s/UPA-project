# UPA-project: COVID-19

UPA BUT FIT project 2021/22

## Requirements
- Docker engine
- Docker compose

## Build services
```docker-compose build```

## Run services
Firstly is necessary to run service for initialization of influx db (username, password, ...):

```docker-compose up influxdb```

Then is necessary to run service for filling the database:

```docker-compose up scraper```

Before generating of graphs is required to export:

```LOCAL_PROJECT_DIR=PATH```
where PATH is local path to downloaded repository.

For generating graphs from DB data is necessary to run:


```docker-compose up visualizer```

### Detached mode
All services can run in detached mode by adding option ```-d``` to ```docker-compose``` command

### Access DB directly
Influx DB service can be accessed directly and there can be performed all valid influx DB commands.

```
docker exec -it influxdb bash
influx
```

## Stop all running services
```docker-compose down```

## Authors
- Bc. Matej Otcenas (xotcen01)
- Bc. Jan Jakub Kubik (xkubik32)
- bc. Jan Kacur (xkacur04)
