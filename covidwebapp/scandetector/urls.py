from django.urls import path
from django.views.generic import TemplateView

from .views import ScanProcessView

app_name = 'scandetector'
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('how-it-works', TemplateView.as_view(template_name='how-it-works.html'), name='how'),
    path('team', TemplateView.as_view(template_name='team.html'), name='team'),
]