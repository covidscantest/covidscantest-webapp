from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='upload.html'), name='index'),
    path('result/', TemplateView.as_view(template_name='result.html'), name='result'),
]
