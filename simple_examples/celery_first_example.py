from celery import Celery
import datetime

app = Celery('tasks')
app.config_from_object('simple_examples.celeryconfig')


@app.task(name='what-time-is-it')
def now_time():
    return datetime.datetime.now()


@app.task(name='what-amount')
def amount(x, y):
    return x + y