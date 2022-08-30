from django.conf import settings
from django.core.mail import send_mail

from web_store.celery import app


@app.task
def send_mail_order_created(order_name_customer, order_id, order_email):
    subject = f'Order №{order_id}'
    message = f'Dear {order_name_customer}, your order №{order_id} has been created.\nThank you for your purchase!'
    send_mail(subject=subject,
              message=message,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[order_email]
              )
