from django.http import HttpResponse
from django.views.decorators.http import require_POST
import subprocess

@require_POST
def run_spider(request):
    try:
        # Run spider and stream logs to stdout/stderr
        subprocess.run(
            ["make", "mercado_livre"],
            check=True
        )
        return HttpResponse("Spider completed successfully!")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"Spider failed: {str(e)}", status=500)