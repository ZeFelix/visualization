from django.urls import path
from app.views import AllList, index, NodeDetail,StudentDetail

urlpatterns = [
    path("all",AllList.as_view()),
    path("node/<int:node_id>",NodeDetail.as_view()),
    path("node/<int:node_id>/students",StudentDetail.as_view()),
    path("",index),
]
