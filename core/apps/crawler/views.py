from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.core.cache import cache
from .tasks import run_spider_task
from rest_framework.decorators import api_view
from rest_framework.response import Response


@require_POST
def run_spider(request):
    # Launch Celery task
    run_spider_task.delay()
    return HttpResponse("Spider started!")

@api_view(['GET'])
def spider_status(request):
    status = cache.get('spider_status', 'idle')
    return Response({'status': status})