from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from PIL import Image
import json
import base64
import io
import requests
# Create your views here.

TARGET_SHAPE = (299,299)

def decodeImage(img):
    encoded_image = img
    decoded_image = base64.b64decode(encoded_image)
    return decoded_image

def encodeImage(img):
    encoded_image=base64.b64encode(img)
    return encoded_image

def preprocessImage(request):
    data = json.loads(request.body.decode('utf-8')) # {"img"}
    decoded_image = decodeImage(data["img"])
    decoded_image = Image.open(io.BytesIO(decoded_image)).resize(TARGET_SHAPE,Image.LANCZOS).convert("RGB")
    buffer = io.BytesIO()
    decoded_image.save(buffer,format="JPEG")
    encoded_image=encodeImage(buffer.getvalue()).decode('utf-8')
    data['img'] = encoded_image
    return JsonResponse(data,safe=False)

def getCalories(request):
    data = json.loads(request.body.decode('utf-8')) # {"label"}
    # TODO: Preprocessing labelnya supaya bisa sesuai dengan query di api nya

    ###
    query = data["label"]
    url = "https://api.calorieninjas.com/v1/nutrition?query="
    response = requests.get(url+query, headers={'X-Api-Key': '3qW+6K0LsbPbCXfiECXYYw==TzROrcI2wUouScOT'})
    outputDict=response.json()
    outputDict['status']=response.status_code
    return JsonResponse(outputDict,safe=False)
