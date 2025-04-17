from celery import shared_task
from django.core.cache import cache
from dash_apps.components.constants import MAKE_MAP
import subprocess


@shared_task
def run_spider_task(seller: str = 'carrefas'):
    cache.set('spider_status', 'running', timeout=3600)  # 1-hour timeout
    try:
        # Run your spider process
        subprocess.run(["make", seller], check=True)
        cache.set('spider_status', 'completed', timeout=300)
    except subprocess.CalledProcessError as e:
        cache.set('spider_status', f'failed: {str(e)}', timeout=60)
    except Exception as e:
        cache.set('spider_status', f'error: {str(e)}', timeout=60)

