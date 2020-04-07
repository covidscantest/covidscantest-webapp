from django.shortcuts import render
from django.views import View
from .models import ScanUpload


class ScanProcessView(View):
    template_name = 'result.html'

    def post(self, request):
        new_upload = ScanUpload(scan_file=request.FILES['image'])
        new_upload.save()
        return render(request, self.template_name)
