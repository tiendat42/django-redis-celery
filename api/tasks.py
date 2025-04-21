import time
from celery import shared_task


@shared_task
def add(x, y):
    print(f"Tính {x} + {y}")
    time.sleep(3)
    return x + y
