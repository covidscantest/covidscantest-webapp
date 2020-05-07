import numpy
import tensorflow as tf
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import ScanUpload
from .datascience import covid as ds_covid
from .datascience import healthy as ds_healthy
from .datascience import pneumonia as ds_pneumonia
import torchvision.transforms as transforms
import tensorflow.keras as ks
from PIL import Image


def get_xray_or_not_model(input_shape):
    model = ks.models.Sequential()
    model.add(ks.layers.Conv2D(32, (3, 3), input_shape=input_shape))
    model.add(ks.layers.Activation('relu'))
    model.add(ks.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(ks.layers.Conv2D(32, (3, 3)))
    model.add(ks.layers.Activation('relu'))
    model.add(ks.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(ks.layers.Conv2D(64, (3, 3)))
    model.add(ks.layers.Activation('relu'))
    model.add(ks.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(ks.layers.Flatten())
    model.add(ks.layers.Dense(64))
    model.add(ks.layers.Activation('relu'))
    model.add(ks.layers.Dropout(0.5))
    model.add(ks.layers.Dense(1))
    model.add(ks.layers.Activation('sigmoid'))
    return model

xray_or_not_model = get_xray_or_not_model(input_shape=(150, 150, 3))
xray_or_not_model.load_weights('./scandetector/weights/xray/xray_or_not_0426.h5')


@method_decorator(csrf_exempt, name='dispatch')
class ScanProcessView(View):
    template_name = 'result.html'

    def post(self, request):
        image_upload = request.FILES['image']
        tf_image = image_upload.file.read()
        tf_image = tf.image.decode_image(tf_image, channels=3, expand_animations=False)
        tf_image = tf.image.convert_image_dtype(tf_image, tf.float32)

        final_result = {}

        xray_prob = float(self.calc_xray_prob(tf_image))
        final_result['xray_prob'] = '%.4f' % xray_prob
        if xray_prob >= 0.5:
            img_with_distortions = self.generate_noizy_set(tf_image)
            rest_prob = 1.0

            healthy_prob = float(ds_healthy.calc_healthy_prob(tf_image))
            final_result['healthy_prob'] = '%.4f' % healthy_prob
            rest_prob -= healthy_prob

            pneumonia_prob = float(ds_pneumonia.calc_pneumo_prob(tf_image))
            final_result['pneumonia_prob'] = '%.4f' % (rest_prob * pneumonia_prob)
            rest_prob -= rest_prob * pneumonia_prob

            covid_prob = float(ds_covid.calc_covid_prob(tf_image))
            final_result['covid_prob'] = '%.4f' % (rest_prob * covid_prob)
            rest_prob -= rest_prob * covid_prob

            final_result['rest_prob'] = '%.4f' % rest_prob
        # transform = transforms.Compose(
        #    [
        #        transforms.Resize(299),
        #        transforms.CenterCrop(299),
        #        transforms.ToTensor(),
        #        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        #    ])
        # norm_img = transform(pil_image)
        # input_tensor = norm_img.view(1, 3, 299, 299)
        # output_tensor = torch_model(input_tensor)
        # predicted_probs_tensor = torch.nn.functional.softmax(output_tensor[0], dim=0)

        new_upload = ScanUpload(scan_file=image_upload)
        new_upload.save()

        # classes_list = predicted_probs_tensor.tolist()

        return JsonResponse(final_result)  # render(request, self.template_name, {'classes': classes_list})

    def generate_noizy_set(self, original_img):
        return [original_img]

    def calc_xray_prob(self, tf_image):
        img = tf.image.resize(tf_image, [150, 150])
        model_input = tf.expand_dims(img, 0)
        model_output = xray_or_not_model.predict_proba(model_input)[0]
        return model_output[0]