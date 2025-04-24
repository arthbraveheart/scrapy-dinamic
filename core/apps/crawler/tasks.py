from typing import Optional
from celery import shared_task
from django.core.cache import cache
from dash_apps.components.constants import MAKE_MAP
import subprocess
from .crawlers.triggers import SpiderRunner
from .crawlers.spiders.ml_curva import MLNewSpider

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


@shared_task
def run_spider_Task(seller: str = 'ml_curva', curva : Optional[str] = None):
    cache.set('spider_status', 'running', timeout=3600)  # 1-hour timeout
    try:
        runner = SpiderRunner()
        runner.run(MLNewSpider, curva)  # Pass `curva` to runner
        cache.set('spider_status', 'completed', timeout=300)
    except Exception as e:
        cache.set('spider_status', f'error: {str(e)}', timeout=60)