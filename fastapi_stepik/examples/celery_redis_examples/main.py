from fastapi import FastAPI
from celery import Celery
from task import call_background_task

app = FastAPI()

celery = Celery(
    __name__,
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/0',
    broker_connection_retry_on_startup=True
)



@app.get("/")
async def hello_world(message: str):
    call_background_task.apply_async(args=[message], expires=3600)
    return {'message': 'Hello World!'}


celery.conf.beat_schedule = {
    'run-me-background-task': {
        'task': 'task.call_background_task',
        'schedule': 5.0,
        'args': ('Test text message',)
    }
}