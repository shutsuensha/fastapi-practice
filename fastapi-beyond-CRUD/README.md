# TO DO
## сделать тестирование и описать в readme

# Main functionality
- User Registration
- Email Verification via a Link
- User Authentication and Authorization using JWT Token and JWT Token Revocation
- User Role Management
- Password Reset via Email Link
- Book Management
- Review Management for Books
- Tag Management for Books

# Developing locally

## Create virtual env, activate it and install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## Install and start redis server
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl status redis-server
(for stop service) sudo systemctl stop redis-server
```
### Connection
```bash
redis-cli
```
### Add `REDIS_URL` to `.env`:
REDIS_URL=redis://localhost:6379/0`

## Install, start postgresql server, first connect
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl status postgresql
(for stop service) sudo systemctl stop postgresql
sudo -i -u postgres
psql
```
### Create database
```sql
CREATE DATABASE mydatabase;
CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
```
### Connection
```bash
psql -U myuser -d mydatabase
```
### Add `DATABASE_URL` to `.env`:
DATABASE_URL=postgresql+asyncpg://myuser:mypassword@localhost:5432/mydatabase

## Setup rest of `.env` file
MAIL_PASSWORD - generate

## Start celery
```bash
sh runworker.sh
```

## Run fastapi server and create tables in database
```bash
fastapi dev src
```

## OpenAPI Swagger UI
http://127.0.0.1:8000/api/v1/docs

## Flower: monitoring real-time celery
http://127.0.0.1:5555


## (For learning purpose) init and set up alembic for migrations
```bash
alembic init -t async migrations
```
### Edit migrations/env.py
Add
```python
from sqlmodel import SQLModel
from src.config import Config

database_url = Config.DATABASE_URL
config = context.config
config.set_main_option("sqlalchemy.url", database_url)

target_metadata = SQLModel.metadata
```
### Edit migrations/script.py.mako
Add
```python
import sqlmodel
```
### Now u can modify your models, generate migration and apply them
```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

## Stop all services
```bash
sh stop-services.sh
```

## Quick start
```bash
sh start-services.sh
sh runworker.sh
fastapi dev src
```
http://127.0.0.1:8000/api/v1/docs



# Developing in docker

## Edit `.env` file
    > redis url: REDIS_URL=redis://redis:6379/0
    > DATABASE_URL=postgresql+asyncpg://postgres:docent1315@db:5432/bookly
    > MAIL_PASSWORD - generate
```bash
docker compose up
```
http://127.0.0.1:8000/api/v1/docs

## Now u can modify your models, connect to container, generate migration and apply them
```bash
sudo docker exec -it <hash web container> /bin/bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```