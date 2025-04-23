# shop/tasks.py
from celery import shared_task
import time
from datetime import datetime


@shared_task
def send_invoice_email(order_id):
    # Imagine this sends an email
    time.sleep(5)
    return (f"Sending invoice email for order {order_id}")


@shared_task
def send_notify(order_id):
    # Imagine this sends an email
    time.sleep(10)
    return (f"Sending notify for order {order_id}")


@shared_task(bind=True, max_retries=2)
def test_retry(self, id):
    try:
        # logic here
        raise Exception('error')
    except Exception as exc:
        raise self.retry(exc=exc, countdown=6)


@shared_task
def cron_task():
    print(f"[{datetime.now()}] Xin chào từ Celery Beat!")
