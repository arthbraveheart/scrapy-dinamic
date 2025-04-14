from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("run-spider/", views.run_spider, name="run-spider"),
    path("index/", TemplateView.as_view(template_name="pages/index.html"), name="index"),
]