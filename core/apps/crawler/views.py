from django.http import JsonResponse
from django.core.cache import cache
from .forms import SellerForm
from .tasks import run_spider_task, run_spider_Task
from target.models import DularEans, Core
from datetime import datetime
from django.views.generic import TemplateView
from target.models import Curva


class index(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SellerForm()
        return context

def run_spider(request):
    if request.method == "POST":
        form = SellerForm(request.POST)
        # Store the start time for progress tracking
        start_time = datetime.now()
        cache.set('spider_start_time', start_time.isoformat(), timeout=3600)

        # Get the total number of EANs to process
        total_eans = DularEans.objects.all().distinct().count()
        cache.set('total_eans', total_eans, timeout=3600)

        if form.is_valid():
            seller = form.cleaned_data['seller']
            #if form.cleaned_data['curva']:
             #   curva = form.cleaned_data['curva']
              #  products = curva.products.all().values_list('ean', flat=True)
               # run_spider_task.delay(seller, tuple(products))

            # Start the spider task
            run_spider_task.delay(seller)
            return JsonResponse({"status": "started"})
    return JsonResponse({"status": "method not allowed"}, status=405)


def spider_status(request):
    status = cache.get('spider_status', 'not_started')

    # Get progress information
    total_eans = cache.get('total_eans', 0)
    start_time_str = cache.get('spider_start_time')

    # Default values
    completed_eans = 0
    percentage = 0

    if status != 'not_started':
        start_time_str = cache.get('spider_start_time')
        start_time = datetime.fromisoformat(start_time_str)
        completed_eans = Core.objects.filter(
            date_now__gt=start_time
        ).values('ean').distinct().count()
        if status == 'running':
            percentage = int((completed_eans / total_eans * 100) if total_eans > 0 else 0)
        elif status == 'completed':
            percentage = 100

    return JsonResponse({
        "status": status,
        "progress": {
            "completed": completed_eans,
            "total": total_eans,
            "percentage": percentage
        }
    })