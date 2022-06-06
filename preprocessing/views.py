from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from PIL import Image
import json
import base64
import io
# Create your views here.

TARGET_SHAPE = (299,299)

def decodeImage(img):
    encoded_image = img
    decoded_image = base64.b64decode(encoded_image)
    return decoded_image

def encodeImage(img):
    decoded_image = bytes(str(img),"utf-8")
    encoded_image = base64.b64encode(decoded_image)
    return encoded_image

def preprocessImage(request):
    data = json.loads(request.body.decode('utf-8'))
    decoded_image = decodeImage(data["img"])
    decoded_image = Image.open(io.BytesIO(decoded_image)).resize(TARGET_SHAPE,Image.LANCZOS).convert("RGB")
    encoded_image = encodeImage(decoded_image)#.decode('utf-8')

    print(encoded_image)
    data['img'] = encoded_image
    return JsonResponse(data,safe=False)