from django.urls import path
from . import views

urlpatterns = [
    path('/preprocessImage',views.preprocessImage,name="preprocessImage"),
]