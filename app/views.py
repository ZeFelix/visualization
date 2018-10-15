from astroid import objects
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg
from django.db.models import Q
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from app.models import Classes, Node, Student, StudentInformations
from app.serializer import ActivitySerializer, ClassesSerialzer, \
    NodeSerializer, StudentSerializer


# Create your views here.


class AllList(APIView):
    """
    Classe para listar todas as turmas do curso e seu nó raiz
    Método http permuitido: get
    """

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
            data.append(NodeDetail.format_node_information(node,request))
        return data


class NodeDetail(APIView):
    """
    Classe que contém os detalhes dos nós
    Método http permito: get
    """

    def get(self, request, node_id):
        node_parent = Node.objects.get(pk=node_id)
        nodes = Node.objects.filter(node_parent=node_parent)
        data = []
        for node in nodes:
            if node:
                data.append(self.format_node_information(node, request))
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

    @classmethod
    def format_node_information(self, node, request):
        """
        Método para formatar o as informações de retorno do nó
        Recebe um nó por paramentro
        Recebe o request para verificar se há paramentros de filtro na requisição get
        número -1: indica a cor de um nó que n tem aluno que pertence ao filtro
        """
        node_formatation = None
        try:
            start_ager = int(
                request.GET["start_ager"]) if request.GET["start_ager"] != "null" else 0
            end_ager = int(
                request.GET["end_ager"]) if request.GET["end_ager"] != "null" else 100
            sex_m = request.GET["sex_m"]
            sex_f = request.GET["sex_f"]
            not_married = request.GET["not_married"]
            married = request.GET["married"]
            public = request.GET["public"]
            particular = request.GET["particular"]
            students = node.students.filter(Q(sex=sex_f) | Q(
                sex=sex_m), Q(school_origin=public) | Q(school_origin=particular),
                Q(civil_status=married) | Q(civil_status=not_married), ager__range=(start_ager, end_ager))
        except Exception as a:
            students = node.students.all()
        if students.count():
            # só adciona um nó se o mesmo tiver algum aluno
            students_serializer = StudentSerializer(
                students, many=True)
            data_students = students_serializer.data
            node_formatation = {
                "node_name": node.name,
                "node_id": node.id,
                "node_avg": self.get_node_average(node, students),
                "node_end": node.node_end,
                "node_evaluated": node.evaluated,
                "name": node.activity.first().name,
                "students": students_serializer.data
            }
        elif node.students.count():
            # se não tiver aluno após o filtro
            # porém existem alunos naquele nó, ele adiciona uma média negativa (-1) para indicar a cor do caminho(link)
            node_formatation = {
                "node_name": node.name,
                "node_id": node.id,
                "node_avg": -1,
                "name": node.activity.first().name,
                "students": []
            }
        return node_formatation


class StudentDetail(APIView):

    def get(self, request, node_id):
        nodes = Node.objects.filter(pk=node_id)
        students = []
        for node in nodes:
            students = node.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

@login_required(login_url = "/api/login")
def index(request, template_name="index.html"):
    return render(request, template_name)

def login_user(request, template_name="login.html"):
    nex = request.GET.get("next", "/api")
    if request.user.is_authenticated:
        return HttpResponseRedirect('/api')
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request,username=username, password=password)
            print(user)
            if user is not None:
                if user.is_active:
                    print("aki")
                    login(request, user)
                    print("oi")
                    return HttpResponseRedirect(nex)
                return HttpResponseRedirect("/api/login")
            else:
                return HttpResponseRedirect("/api/login")
        return render(request, template_name, {"redirect_to": nex})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/api/login")
