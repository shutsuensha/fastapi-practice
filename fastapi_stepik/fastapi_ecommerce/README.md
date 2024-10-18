## Web-server
```bash
uvicorn app.main:app --reload
```
## Migrations
### alembic.ini:
- sqlalchemy.url = postgresql+asyncpg://evalshine:docent1315@localhost:5432/ecommerce
### app.migrations.env:
```python
from app.backend.db import Base
from app.models import *
target_metadata = Base.metadata
```
```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```