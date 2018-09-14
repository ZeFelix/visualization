from astroid import objects
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Classes, Node, Student
from app.serializer import ActivitySerializer, ClassesSerialzer, \
    NodeSerializer, StudentSerializer


# Create your views here.


class AllList(APIView):

    def get(self, request):
        informations = []
        classes = Classes.objects.all()
        serializer = ClassesSerialzer(classes, many=True)
        for classe in classes:
            students = Student.objects.filter(classe=classe).count()
            informations.append({
                "classe_id":classe.id,
                "name": classe.name,
                "students_quantity" : students,
                "children": self.get_node_start(classe.course)
            })
        #serializer = ClassesSerialzer(classes,many=True)
        return Response(informations)

    def get_node_start(self, course):
        node = Node.objects.filter(course=course, node_start=True).first()
        data_students = []
        if node:
            students = StudentSerializer(node.students, many=True)
            data_students = students.data

        data = []
        if node:
            data.append({
                "node_color" : node.color_representation,
                "node_name": node.name,
                "node_id": node.id,
                "name": node.activity.first().name,
                "students":data_students
            })
        return data


class NodeDetail(APIView):

    def get(self, request, node_id):
        node_parent = Node.objects.get(pk=node_id)
        nodes = Node.objects.filter(node_parent=node_parent)
        data = []
        for node in nodes:
            if node:
                students = StudentSerializer(node.students, many=True)
                data.append({
                    "node_color" : node.color_representation,
                    "node_name": node.name,
                    "node_id": node.id,
                    "name": node.activity.first().name,
                    "students":students.data
                })
        return Response(data)


class StudentDetail(APIView):

    def get(self,request,node_id):
        nodes = Node.objects.filter(pk=node_id)
        students = []
        for node in nodes:
            students = node.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

def index(request, template_name="index.html"):
    return render(request, template_name)
