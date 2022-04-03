# Wobbly.BDNA
(Big-data news analyz)

Tool, for analyz for huge amount of news

## Installation

You need to have installed Docker, and some containers. Below will be commands:
```
docker run --hostname localhost -p 15672:15672 -p 5672:5672 rabbitmq:3-management
docker run --name postgres -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -d postgres:13.3
```
Also, you need to create DB in PostgreSQL, and after, you can run script, that create tables
```
python /db/create_db.py
```

## Configuring
You need also to add links, to feautures sites, to scan it. You can do it through the SQL just inserting new records

Also, you need create CRON(linux) for all scripts
```
/link_extractor/main.py
all files in nlp_modules
```

After that, you can view info through web-interface
```
python web/main.py
```

Open browser and enter localhost with 5000 port