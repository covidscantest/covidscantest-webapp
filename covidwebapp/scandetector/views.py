from django.shortcuts import render
from django.views import View
from .models import ScanUpload
# import tensorflow as tf
import numpy
from PIL import Image


# model = tf.keras.models.load_model('./scandetector/weights/DenseNet121_model.hdf5')
model = False
input_size = (224, 224)

class ScanProcessView(View):
    template_name = 'result.html'

    def post(self, request):
        image_upload = request.FILES['image']
        pil_image = Image.open(image_upload.file)
        resized_image = pil_image.resize(input_size)

        img_as_arr = numpy.asarray(resized_image)
        img_input = numpy.expand_dims(img_as_arr, axis=0)
        predicted_probs = model.predict_proba(img_input)

        new_upload = ScanUpload(scan_file=image_upload)
        new_upload.save()

        classes_list = predicted_probs.tolist()

        return render(request, self.template_name, {'classes': classes_list})
