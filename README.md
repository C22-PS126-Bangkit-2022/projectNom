# Backend Repo for Project Nom Capstone Bangkit 2022 by Team C22-PS126

This repository contains the backend code for Project Nom application. We're using Django as for the backend to communicate with Android and the Google Cloud.

---

Table of Contents
1. About the project
2. Backend/Cloud Computing documentation
3. Usage

---

## About the Project

To achieves a healthy life and dream body, a neatly structured meal tracking is important to keep track of fulfilled nutrition. We present an android application used to classify food items from images taken by users from their own mobile devices, return its prediction result and the nutrition facts, and log it into the applications. Now, users can neatly structured their meal everyday without hassle.

## Backend/CLoud COmputing Documentation

1. Write the Django server app using Python
    - If you have local development purpose, save the model in the same directory as `manage.py`
    - Load the model and tun the server with `python manage.py runserver`
    - Send the input images to the `preprocessImage` url
2. Setting up Google Storage Bucket
    - To do this, create a GCP account and project. Go to `Cloud Storage` and create Bucket Storages.
    - Enable cloud run and install GCloud SDK
    - Copy local model into the Google Bucket Storages with `gsutil cp -r /your/path/model gs://yourbucketname`
3. Setting up Google AI Platform Prediction
    - Go to `AI Platform` and enable AI API.
    - Go to `Models` tabs and create one for your model.
    - After done with previous step, create a versioning for your model.
    - Copy the snippet code provided by Google AI Platform to connect to the deployed model into the backend code.
