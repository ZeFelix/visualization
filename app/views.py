from django.shortcuts import render
from rest_framework.views import APIView
from app.serializer import ClassesSerialzer, StepSerializer, ActivitySerializer, StudentSerializer
from app.models import *
from rest_framework.response import Response
from django.shortcuts import render

# Create your views here.


class AllList(APIView):

    def get(self, request):
        informations = []
        classes = Classes.objects.all()

        for i in range(len(classes)):
            steps = classes[i].step.all()
            informations.insert(i, {
                "pk" : classes[i].pk,
                "name": classes[i].name,
                "children": self.builder_steps(classes[i], steps)
            })

        #serializer = ClassesSerialzer(classes,many=True)
        return Response(informations)

    def builder_steps(self, classe, steps):
        activity_steps_list = []
        students = Student.objects.filter(classe=classe)
        for i in range(steps.count()-1, 0, -1):
            list_nodes = []
            list_children = []
            """adicionando o primeiro da lista"""
            if len(activity_steps_list) == 0:
                activity_object_children =Activity.objects.filter(step=steps[i])
                
                for activity_children in activity_object_children:
                    list_students = []
                    for student in students:
                        if student in activity_children.student.all():
                            list_students.append(
                                StudentSerializer(student).data
                                )
                    list_children.append(
                        {
                        "pk":activity_children.pk,
                        "name":activity_children.name,
                        "steps":steps[i].name,
                        "students": list_students
                        }
                    )
                    

                activity_object_parent = Activity.objects.filter(step=steps[i-1])

                for activity_parent in activity_object_parent:
                    students_list = []
                    for student in students:
                        """
                        retorna todos os estudantes de uma turma naquela atividade
                        """
                        if student in activity_parent.student.all():
                            students_list.append(
                                StudentSerializer(student).data,
                            )

                    list_nodes.append(
                        {
                            "pk": activity_parent.pk,
                            "name": activity_parent.name,
                            "steps":steps[i-1].name,
                            "students": students_list,
                            "children": list_children
                        }
                    )

                activity_steps_list = list_nodes
            else:
                activity_object_parent = Activity.objects.filter(step=steps[i-1])

                for activity_parent in activity_object_parent:
                    students_list = []
                    for student in students:
                        """
                        retorna todos os estudantes de uma turma naquela atividade
                        """
                        if student in activity_parent.student.all():
                            students_list.append(
                                StudentSerializer(student).data,
                            )

                    list_nodes.append(
                        {
                            "pk": activity_parent.pk,
                            "name": activity_parent.name,
                            "steps":steps[i-1].name,
                            "students": students_list,
                            "children": activity_steps_list
                        }
                    )
                activity_steps_list = list_nodes
#            print(activity_steps_list)
        return activity_steps_list


def index(request, template_name="index.html"):
    return render(request,template_name)