from django.urls import path

from app.views import AllList, NodeDetail, StudentDetail, gantt, gantt_detail, \
    index, login_user, logout_user, StudentInformationsDetail, TeacherDetail


urlpatterns = [
    path("all",AllList.as_view()),
    path("node/<int:node_id>",NodeDetail.as_view()),
    path("node/<int:node_id>/students",StudentDetail.as_view()),
    path("",index),
    path("login",login_user),
    path("logout",logout_user, name='logout'),
    path("gantt",gantt, name='gantt'),
    path("gantt/<int:student_id>",gantt_detail, name='gantt_detail'),
    path("gantt/<int:node_id>/<int:student_id>",StudentInformationsDetail.as_view(), name='student_informations'),
    path("gantt/teacher/<int:teacher_id>",TeacherDetail.as_view(), name='teacher')
]
