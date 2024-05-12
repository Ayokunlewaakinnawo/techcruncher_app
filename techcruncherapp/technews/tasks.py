from celery import shared_task
from .views import scrape

@shared_task
def scrape_task():
    scrape()
