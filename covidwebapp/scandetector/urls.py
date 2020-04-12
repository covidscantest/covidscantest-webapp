from django.urls import path
from django.views.generic import TemplateView

from .views import ScanProcessView

app_name = 'scandetector'
urlpatterns = [
    path('', TemplateView.as_view(template_name='upload.html'), name='index'),
    path('result/', ScanProcessView.as_view(), name='result'),
    path('team/', ScanProcessView.as_view(), name='teams'),
]
