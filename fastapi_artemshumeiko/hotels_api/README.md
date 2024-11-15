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
sudo systemctl start redis-server
sudo systemctl status redis-server

## Celery
celery -A app.tasks.celery_app.celery_instance worker --loglevel=info

## Celery Beat
celery -A app.tasks.celery_app.celery_instance beat --loglevel=info

## Testing
pip3 install pytest
pip3 install pytest-dotenv
pip3 install pytest-asyncio

### Test db
psql -U evalshine -d hotels_db_test