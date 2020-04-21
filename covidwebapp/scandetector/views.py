from django.shortcuts import render
from django.views import View
from .models import ScanUpload
import pickle
import torch
import torchvision.models as torchmodels
import torchvision.transforms as transforms
import numpy
from PIL import Image

model_obj = pickle.load(open('./scandetector/weights/pytorch_inceptionv3_final.pckl', 'rb'))
torch_model = torchmodels.inception.inception_v3(num_classes=3)
torch_model.load_state_dict(model_obj['model_state_dict'])
torch_model.eval()


class ScanProcessView(View):
    template_name = 'result.html'

    def post(self, request):
        image_upload = request.FILES['image']
        pil_image = Image.open(image_upload.file).convert('RGB')
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
