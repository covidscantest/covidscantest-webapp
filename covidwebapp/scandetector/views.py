from django.shortcuts import render
from django.views import View
from .models import ScanUpload
import pickle
import torch
import torchvision.models as torchmodels
import torchvision.transforms as transforms
import tensorflow.keras as ks
from PIL import Image

def get_xray_ornot_model(input_shape):
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

model_obj = pickle.load(open('./scandetector/weights/googlenet_final_0423_cpu.pckl', 'rb'))
torch_model = torchmodels.googlenet(num_classes=3)
torch_model.load_state_dict(model_obj['model_state_dict'])
torch_model.eval()

xray_ornot_model = get_xray_ornot_model(input_shape=(150, 150, 3))


class ScanProcessView(View):
    template_name = 'result.html'

    #this function should generate bunch of images with minor distortions
    def generate_noizy_set(self, original_img):
        return [original_img]

    def calc_notxray_prob(self, img):
        return 0.2

    def calc_healthy_prob(self, img_set):
        return 0.7

    def calc_pneumo_prob(self, img_set):
        return 0.3

    def calc_covid_prob(self, img_set):
        return 0.01

    def post(self, request):
        image_upload = request.FILES['image']
        pil_image = Image.open(image_upload.file).convert('RGB')
        final_result = {}

        if self.calc_notxray_prob(pil_image) > 0.5:
            final_result['not_xray'] = True

        transform = transforms.Compose(
            [
                transforms.Resize(299),
                transforms.CenterCrop(299),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
        norm_img = transform(pil_image)
        input_tensor = norm_img.view(1, 3, 299, 299)
        output_tensor = torch_model(input_tensor)
        predicted_probs_tensor = torch.nn.functional.softmax(output_tensor[0], dim=0)

        new_upload = ScanUpload(scan_file=image_upload)
        new_upload.save()

        classes_list = predicted_probs_tensor.tolist()

        return render(request, self.template_name, {'classes': classes_list})
