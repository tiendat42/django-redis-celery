# shop/tasks.py
from celery import shared_task
import time


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
