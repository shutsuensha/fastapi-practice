## Web server
```bash
uvicorn app.main:app --reload
```


## Postgres
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
sudo -i -u postgres
psql
```
### Create db
```bash
CREATE DATABASE mydatabase;
CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
```
### Connection
```bash
psql -U evalshine -d hotels_db
```


## Migrations
```bash
alembic init -t async app/migrations
```
### edit `app/migrations/env.py`
```python
from alembic import context
#------------------------------
<PASTE CODE BELOW HERE>
#------------------------------
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
```
```python
from app.config import settings
from app.database.db import Base
from app.models.hotels import HotelsOrm
from app.models.rooms import RoomsOrm
from app.models.users import UsersOrm

config = context.config

config.set_main_option("sqlalchemy.url", f"{settings.DB_URL}")

target_metadata = Base.metadata
```
### generate and upgrade
```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

## Redis
```bash
sudo systemctl start redis-server
sudo systemctl status redis-server
```

## Celery
```bash
celery -A app.tasks.celery_app.celery_instance worker --loglevel=info
```

## Celery Beat
```bash
celery -A app.tasks.celery_app.celery_instance beat --loglevel=info
```

## Testing
```bash
pip3 install pytest
pip3 install pytest-dotenv
pip3 install pytest-asyncio
```

### Test db
```bash
psql -U evalshine -d hotels_db_test
```


## Docker
```bash
docker network create myNetwork

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:15

docker run --name booking_cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:7.4


docker build -t fastapi .

docker run --name booking_back \
    -p 7777:8000 \
    --network=myNetwork \
    fastapi


docker run --name booking_celery_worker \
    --network=myNetwork \
    fastapi \
    celery -A app.tasks.celery_app.celery_instance worker --loglevel=info


docker run --name booking_celery_beat \
    --network=myNetwork \
    fastapi \
    celery -A app.tasks.celery_app.celery_instance beat --loglevel=info


docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --network=myNetwork \
    --rm -p 80:80 nginx
```

## Docker compose
```bash
docker compose build - (build image from Dockerfile)
docker compose up
```