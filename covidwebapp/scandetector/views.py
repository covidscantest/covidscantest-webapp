from django.shortcuts import render
from django.views import View
from .models import ScanUpload
import tensorflow as tf
import numpy
from PIL import Image


model = tf.keras.models.load_model('./scandetector/weights/DenseNet121_model.hdf5')

class ScanProcessView(View):
    template_name = 'result.html'

    def post(self, request):
        image_file = request.FILES['image']

        img_as_arr = numpy.asarray(Image.open(image_file.file))
        img_input = numpy.expand_dims(img_as_arr, axis=0)
        predicted_classes = model.predict_classes(img_input)

        new_upload = ScanUpload(scan_file=image_file)
        new_upload.save()

        classes_list = predicted_classes.tolist()

        return render(request, self.template_name, {'classes': classes_list})
