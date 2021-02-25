import os
from pathlib import Path
import pandas as pd

from celery.utils.log import get_task_logger

from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task
from Import_Export.celery import app
from product.functions import handle_file
from product.models import UploadedFile, Product, Category, Brand, Color

logger = get_task_logger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent
#
# @app.task()
# def send_email_task():
#
#     subject = 'sample email'
#     logger.info("Sent feedback email")
#
#     email_text = f'Hello this is our sample mail.'
#     send_mail(subject, email_text, settings.EMAIL_HOST_USER, ['acquaintdev@gmail.com'], fail_silently=False)
#     msg = "email sent"
#     return msg


@shared_task()
def handle_file_task(file_id):

    logger.info("Sent email")
    handle_file(file_id)
    logger.info('data imported successfully')
    return None
