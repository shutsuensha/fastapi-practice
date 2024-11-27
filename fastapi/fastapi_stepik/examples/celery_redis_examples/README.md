## Redis
```bash
redis-server
```
## Celery
```bash
celery -A main.celery worker --loglevel=info
```
## Web-server
```bash
uvicorn main:app --reload
```
## Celery Beat
```bash
celery -A main.celery beat --loglevel=info
```
## Celery Flower
```bash
celery -A main.celery flower
```