from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from PIL import Image
import json
import base64
import io
import requests
import tensorflow as tf

# Google Cloud Library
import googleapiclient.discovery
from google.api_core.client_options import ClientOptions
# Create your views here.

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'project-nom-351311-a6e5d5ac5601.json'
PROJECT = "project-nom-351311"
REGION = "asia-southeast1"

TARGET_SHAPE = (299, 299)
# MODEL = tf.keras.model.load_model(
#     "preprocessing\model\checkpoint_icv3_30epochs.hdf5", compile=False)
with open("./classes.txt") as file:
    lines = file.readlines()
    LABELS = [line.rstrip() for line in lines]

preprocessLabelDict = {
    "beignets": "pastry",
    "beef carpaccio": "carpaccio",
    "croque madame": "sandwich",
    "fried calamari": "calamari",
    "takoyaki": "dumplings",
    "spaghetti carbonara": "carbonara",
    "lobster roll sandwich": "sandwich",

}

# """
# Ingredient:
# Recipes : baklava
# """

# recipes_dict = {
#     'baklava': 631783,
# }

id_dictionary = {
    # Alphabet A
    "apple_pie": 19312,

    # Alphabet B
    "baby_back_ribs": 10192, "baklava": 631783, "beef_carpaccio": 23572, "beef_tartare": 23572, "beet_salad": 1, "pastry": 1, "bibimbap": 1, "bread_pudding": 10119206, "breakfast_burrito": 10118364, "bruschetta": 99251,

    # Alphabet C
    # Carrot cake, crab cake
    "caesar_salad": 43015, "cannoli": 98983, "caprese_salad": 93670, "carrot_cake": 10018137, "ceviche": 1, "cheesecake": 98951, "cheese_plate": 1, "chicken_curry": 93605, "chicken_quesadilla": 98973, "chicken_wings": 5100, "chocolate_cake": 18099, "chocolate_mousse": 1, "churros": 1, "clam_chowder": 1, "club_sandwich": 18353, "crab_cakes": 10018137, "creme_brulee": 1, "sandwich": 98940, "cup_cakes": 18139,

    # Alphabet D
    "deviled_eggs": 1, "donuts": 1, "dumplings": 99034,

    # Alphabet E
    "edamame": 11212, "eggs_benedict": 1, "escargots": 90560,

    # Alphabet F
    "falafel": 1, "filet_mignon": 10013926, "fish_and_chips": 1, "foie_gras": 1005150, "french_fries": 11408, "french_onion_soup": 6354, "french_toast": 18070, "calamari": 15175, "fried_rice": 93721, "frozen_yogurt": 93629,

    # Alphabet G
    "garlic_bread": 1, "gnocchi": 98853, "greek_salad": 1, "grilled_cheese_sandwich": 1, "grilled_salmon": 10015076, "guacamole": 1009037, "gyoza": 1,

    # Alphabet H
    "hamburger": 23569, "hot_and_sour_soup": 1, "hot_dog": 21118, "huevos_rancheros": 1, "hummus": 16158,

    # Alphabet I
    "ice_cream": 19095,

    # Alphabet L
    "lasagna": 10620420, "lobster_bisque": 1, "lobster_roll_sandwich": 1,

    # Alphabet M
    "macaroni_and_cheese": 1, "macarons": 1, "miso_soup": 1, "mussels": 15164,

    # Alphabet N
    "nachos": 1,

    # Alphabet O
    "omelette": 1, "onion_rings": 93709, "oysters": 15167,

    # Alphabet P
    "pad_thai": 1, "paella": 1, "pancakes": 18292, "panna_cotta": 1, "peking_duck": 1, "pho": 1, "pizza": 98924, "pork_chop": 10010062, "poutine": 1, "prime_rib": 1, "pulled_pork_sandwich": 1,

    # Alphabet R
    "ramen": 1, "ravioli": 93832, "red_velvet_cake": 10018099, "risotto": 1,

    # Alphabet S
    "samosa": 1, "sashimi": 1, "scallops": 10015172, "seaweed_salad": 1, "shrimp_and_grits": 1, "spaghetti_bolognese": 12520420, "spaghetti_carbonara": 12520420, "spring_rolls": 1, "steak": 23232, "strawberry_shortcake": 99065, "sushi": 10220054,

    # Alphabet T
    "tacos": 1, "takoyaki": 1, "tiramisu": 1, "tuna_tartare": 10015121,

    # Alphabet W
    "waffles": 28015,

}


def decodeImage(img):
    encoded_image = img
    decoded_image = base64.b64decode(encoded_image)

    return decoded_image


def encodeImage(img):
    encoded_image = base64.b64encode(img)

    return encoded_image


def predict_json(project, region, model, instances, version=None):
    """Send json data to a deployed model for prediction.

    Args:
        project (str): project where the Cloud ML Engine Model is deployed.
        region (str): regional endpoint to use; set to None for ml.googleapis.com
        model (str): model name.
        instances ([Mapping[str: Any]]): Keys should be the names of Tensors
            your deployed model expects as inputs. Values should be datatypes
            convertible to Tensors, or (potentially nested) lists of datatypes
            convertible to tensors.
        version: str, version of the model to target.
    Returns:
        Mapping[str: any]: dictionary of prediction results defined by the
            model.
    """
    # Create the ML Engine service object.
    # To authenticate set the environment variable
    # GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_file>
    prefix = "{}-ml".format(region) if region else "ml"
    api_endpoint = "https://{}.googleapis.com".format(prefix)
    client_options = ClientOptions(api_endpoint=api_endpoint)

    service = googleapiclient.discovery.build(
        'ml', 'v1', client_options=client_options, cache_discovery=False)  # cache_discovery needed to bypass oauth2client unavailable error
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)

    instances_list = instances.tolist()
    response = service.projects().predict(
        name=name,
        body={'instances': instances_list}
    ).execute()

    input_data_json = {'instances': instances_list}

    # print(
    #     len(json.dumps(input_data_json))
    # )  # Get the size of json object

    response = service.projects().predict(
        name=name,
        body=input_data_json
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']


def runInference(image, model, label_list):
    # TODO: Function to call cloud endpoint
    # ...

    # Create dict key "label" to store the prediction result
    result = predict_json(
        project=PROJECT,
        region=REGION,
        model=model,
        instances=image
    )
    # result = model.predict(image)

    # Get the result
    result_class = label_list[np.argmax(result)]
    result_confidence = np.amax(result)

    return result_class, result_confidence


def preprocessImage(request):
    data = json.loads(request.body.decode('utf-8'))  # {"img"}
    decoded_image = decodeImage(data["img"])

    decoded_image = Image.open(io.BytesIO(decoded_image)).resize(
        TARGET_SHAPE, Image.LANCZOS).convert("RGB")

    # Get the prediction
    data['label'], data['conf'] = runInference(decoded_image, MODEL, LABELS)

    buffer = io.BytesIO()
    decoded_image.save(buffer, format="JPEG")

    encoded_image = encodeImage(buffer.getvalue()).decode('utf-8')

    data['img'] = encoded_image

    return JsonResponse(data, safe=False)


def getCalories(request):
    data = json.loads(request.body.decode('utf-8'))  # {"label"}
    # TODO: Preprocessing labelnya supaya bisa sesuai dengan query di api nya

    ###
    food_label = data["label"].lower()
    if preprocessLabelDict.get(food_label) != None:
        food_label = preprocessLabelDict.get(food_label)
    # query = food_label
    food_id = id_dictionary[food_label]

    # api_key = "b6625ab853074827b7278198eef71ae7"
    api_key = "d4e160b3da9a4359b964f89a89db54e6"
    # url = f"https://api.spoonacular.com/food/ingredients/{food_id}/information?amount=1&apiKey={api_key}"
    url = f"https://api.spoonacular.com/food/ingredients/{food_id}/information?amount=1&apiKey={api_key}"

    # response = requests.get(
    #     url + query, headers={'X-Api-Key': '3qW+6K0LsbPbCXfiECXYYw==TzROrcI2wUouScOT'})
    response = requests.get(url)

    outputDict = response.json()
    outputDict['status'] = response.status_code
    return JsonResponse(outputDict, safe=False)
