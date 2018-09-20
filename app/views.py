from astroid import objects
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg
from django.db.models import Q

from app.models import Classes, Node, Student, StudentInformations
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
                "classe_id": classe.id,
                "name": classe.name,
                "students_quantity": students,
                "children": self.get_node_start(classe.course, request)
            })
        # serializer = ClassesSerialzer(classes,many=True)
        return Response(informations)

    def get_node_start(self, course, request):
        node = Node.objects.filter(course=course, node_start=True).first()
        data = []

        if node:
            try:
                color_blind = True if request.GET["color_blind"] == "true" else False
                start_ager = int(request.GET["start_ager"]) if request.GET["start_ager"] != "null" else 0
                end_ager = int(request.GET["end_ager"]) if request.GET["end_ager"] != "null" else 100 
                sex_m = request.GET["sex_m"]
                sex_f = request.GET["sex_f"]
                not_married = request.GET["not_married"]
                married = request.GET["married"]
                public = request.GET["public"]
                particular = request.GET["particular"]
                students = node.students.filter(Q(color_blind=color_blind), Q(sex=sex_f) | Q(
                    sex=sex_m), Q(school_origin=public) | Q(school_origin=particular),
                    Q(civil_status=married) | Q(civil_status=not_married),ager__range=(start_ager,end_ager))
            except Exception as a:
                print(a)
                students = node.students.all()

            if students.count():
                # só adciona um nó se o mesmo tiver algum aluno
                students_serializer = StudentSerializer(
                    students, many=True)
                data_students = students_serializer.data
                data.append({
                    "node_name": node.name,
                    "node_id": node.id,
                    "node_end": node.node_end,
                    "node_avg": NodeDetail.get_node_average(node, students),
                    "name": node.activity.first().name,
                    "students": students_serializer.data
                })
            elif node.students.count():
                # se não tiver aluno após o filtro
                # porém existem alunos ele adiciona uma média negativa para indicar
                data.append({
                    "node_name": node.name,
                    "node_id": node.id,
                    "node_end": node.node_end,
                    "node_avg": -1,
                    "name": node.activity.first().name,
                    "students": []
                })
        return data


class NodeDetail(APIView):

    def get(self, request, node_id):
        node_parent = Node.objects.get(pk=node_id)
        nodes = Node.objects.filter(node_parent=node_parent)
        data = []
        for node in nodes:
            if node:
                try:
                    color_blind = True if request.GET["color_blind"] == "true" else False
                    start_ager = int(request.GET["start_ager"]) if request.GET["start_ager"] != "null" else 0
                    end_ager = int(request.GET["end_ager"]) if request.GET["end_ager"] != "null" else 100 
                    sex_m = request.GET["sex_m"]
                    sex_f = request.GET["sex_f"]
                    not_married = request.GET["not_married"]
                    married = request.GET["married"]
                    public = request.GET["public"]
                    particular = request.GET["particular"]
                    students = node.students.filter(Q(color_blind=color_blind), Q(sex=sex_f) | Q(
                    sex=sex_m), Q(school_origin=public) | Q(school_origin=particular),
                    Q(civil_status=married) | Q(civil_status=not_married),ager__range=(start_ager,end_ager))
                except Exception as a:
                    print(a)
                    students = node.students.all()

                if students.count():
                    # só adciona um nó se o mesmo tiver algum aluno
                    students_serializer = StudentSerializer(
                        students, many=True)
                    data_students = students_serializer.data
                    data.append({
                        "node_name": node.name,
                        "node_id": node.id,
                        "node_end": node.node_end,
                        "node_avg": self.get_node_average(node, students),
                        "name": node.activity.first().name,
                        "students": students_serializer.data
                    })
                elif node.students.count():
                    # se não tiver aluno após o filtro
                    # porém existem alunos ele adiciona uma média negativa para indicar
                    data.append({
                        "node_name": node.name,
                        "node_id": node.id,
                        "node_end": node.node_end,
                        "node_avg": -1,
                        "name": node.activity.first().name,
                        "students": []
                    })

        return Response(data)

    @classmethod
    def get_node_average(self, node, students):
        """
        calcula a média das notas dos alunos naquele nó para aquela atividade
        """
        students_ids = list(students.values_list("id", flat=True))
        average = StudentInformations.objects.filter(
            node=node.id, student__in=students_ids).aggregate(Avg('notes'))
        return average["notes__avg"]


class StudentDetail(APIView):

    def get(self, request, node_id):
        nodes = Node.objects.filter(pk=node_id)
        students = []
        for node in nodes:
            students = node.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


def index(request, template_name="index.html"):
    return render(request, template_name)
