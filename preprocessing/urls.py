from django.urls import path
from . import views

urlpatterns = [
    path('',views.preprocessImage,name="preprocessImage"),
]