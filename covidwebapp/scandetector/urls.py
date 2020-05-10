from django.urls import path
from django.views.generic import TemplateView

from .views import ScanProcessView

app_name = 'scandetector'
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('result/', ScanProcessView.as_view(), name='result'),
    path('how-it-works', TemplateView.as_view(template_name='how.html'), name='how'),
    path('team', TemplateView.as_view(template_name='team.html'), name='team'),
    path('privacy', TemplateView.as_view(template_name='privacy.html'), name='privacy')
]
