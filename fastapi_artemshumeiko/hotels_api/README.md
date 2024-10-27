## Web server
```bash
python3 src/main.py
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
psql -U myuser -d mydatabase
```
## Migrations
```bash
alembic init -t async src/migrations
```
### edit `src/migrations/env.py`
```python
from src.config import settings
from src.database import Base
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm

config.set_main_option("sqlalchemy.url", f"{settings.DB_URL}?async_fallback=True")

target_metadata = Base.metadata
```
### generate and upgrade
```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```