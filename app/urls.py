from django.urls import path
from app.views import AllList, index

urlpatterns = [
    path("all",AllList.as_view()),
    path("",index),
]
