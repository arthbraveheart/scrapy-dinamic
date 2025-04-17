from django.urls import path
from . import views

urlpatterns = [
    path("run-spider/", views.run_spider, name="run-spider"),
    path("spider-status/", views.spider_status, name="spider-status"),
    path("index/", views.index.as_view(), name="index"),
]