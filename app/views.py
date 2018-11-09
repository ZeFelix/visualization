from astroid.protocols import objects
from dijkstar import Graph, find_path
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.defaultfilters import first
from rest_framework import request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Classes, Course, Node, Student, StudentInformations, \
    Teacher
from app.serializer import ActivitySerializer, ClassesSerialzer, \
    NodeSerializer, StudentInformationsSerializer, StudentSerializer, \
    TeacherSerializer

from app.calc_way_avg import WayAvg


# Create your views here.


class AllList(APIView):
    """
    Classe para listar todas as turmas do curso e seu nó raiz
    Método http permuitido: get
    """

    def get(self, request,classe_id):
        informations = []
        classe = Classes.objects.get(pk=classe_id)
        serializer = ClassesSerialzer(classe)
        students = Student.objects.filter(classe=classe).count()
        informations.append({
            "classe_id": classe.id,
            "name": classe.name,
            "students_quantity": students,
            "children": self.get_node_start(classe, request)
        })
        # serializer = ClassesSerialzer(classes,many=True)
        #print(informations)
        return Response(informations)

    def get_node_start(self, classe, request):
        node = Node.objects.filter(course=classe.course, node_start=True).first()
        data = []

        if node:
            data.append(NodeDetail.format_node_information(node,request,classe.id))
        return data


class NodeDetail(APIView):
    """
    Classe que contém os detalhes dos nós
    Método http permito: get
    """

    def get(self, request, node_id,classe_id):
        node_parent = Node.objects.get(pk=node_id)
        nodes = Node.objects.filter(node_parent=node_parent)
        #print("no pai")
        #print(node_parent)
        
        data = []
        for node in nodes:
            node_information = self.format_node_information(node, request, classe_id)
            if not node_information == None:
                data.append(node_information)
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
    def format_node_information(self, node, request, classe_id):
        """
        Método para formatar o as informações de retorno do nó
        Recebe um nó por paramentro
        Recebe o request para verificar se há paramentros de filtro na requisição get
        número -1: indica a cor de um nó que n tem aluno que pertence ao filtro
        """
        node_formatation = None
        student_all = Student.objects.filter(classe=classe_id)
        
        way = True if not request.query_params.get("way") == None else False

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
                Q(civil_status=married) | Q(civil_status=not_married), ager__range=(start_ager, end_ager), classe=classe_id)
        except Exception as a:
            students = node.students.filter(Q(classe=classe_id))

        if students.count():
            # só adciona um nó se o mesmo tiver algum aluno
            students_serializer = StudentSerializer(
                students, many=True)
            student_informations = StudentInformations.objects.filter(student__in=students,node=node)
            student_informations_serializer = StudentInformationsSerializer(student_informations,many=True)
            if way:
                if node.is_way:
                    node_avg = self.get_node_average(node, students)
                else:
                    node_avg = -3  
            else:
                node_avg = self.get_node_average(node, students)

            node_formatation = {
                "node_name": node.name,
                "node_id": node.id,
                "node_avg": node_avg,
                "node_end": node.node_end,
                "node_evaluated": node.evaluated,
                "name": node.activity.first().name,
                "students": students_serializer.data,
                "student_informations": student_informations_serializer.data,
                "percentage_students" : round(students.count()/student_all.count()*100,2),
                "is_filter" : True    
            }
        elif node.students.filter(Q(classe=classe_id)).count():
            # se não tiver aluno após o filtro
            # porém existem alunos naquele nó, ele adiciona uma média negativa (-1) para indicar a cor do caminho(link)
            #print("não ta no filtro")
            #print(node)
            students = node.students.filter(Q(classe=classe_id))
            students_serializer = StudentSerializer(students, many=True)
            student_informations = StudentInformations.objects.filter(student__in=students,node=node)
            student_informations_serializer = StudentInformationsSerializer(student_informations,many=True)
            node_formatation = {
                "node_name": node.name,
                "node_id": node.id,
                "node_avg": -1,
                "node_end": node.node_end,
                "node_evaluated": node.evaluated,
                "name": node.activity.first().name,
                "students": students_serializer.data,
                "student_informations": student_informations_serializer.data,
                "percentage_students" : round(students.count()/student_all.count()*100,2),
                "is_filter" : False
            }
        return node_formatation


class StudentDetail(APIView):

    def get(self, request, node_id):
        """
        Retorna todos os estudantes daquele nó
        """
        nodes = Node.objects.filter(pk=node_id)
        students = []
        for node in nodes:
            students = node.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

@login_required(login_url = "/api/login")
def index(request,id,template_name="index.html"):
    try:
        teacher = Teacher.objects.get(pk=id)
    except Exception as e:
        teacher = Teacher.objects.filter(user=id).first()

    context = {"classes":teacher.classe.all().order_by("name")}
    return render(request, template_name, context)

def login_user(request, template_name="login.html"):
    """
    Método para realizar login
    """
    nex = request.GET.get("next", "/api/teacher")
    if request.user.is_authenticated:
        teacher = Teacher.objects.filter(user=request.user).first()
        return HttpResponseRedirect('/api/teacher/%s' % str(teacher.id))
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request,username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    teacher = Teacher.objects.filter(user=user).first()
                    return HttpResponseRedirect("/api/teacher/"+str(teacher.id))
                return HttpResponseRedirect("/api/login")
            else:
                return HttpResponseRedirect("/api/login")
        return render(request, template_name, {"redirect_to": nex})

def logout_user(request):
    """
    Método para realizar logout
    """
    logout(request)
    return HttpResponseRedirect("/api/login")

@login_required
def gantt(request, template_name="graph_gantt.html"):
    return render(request, template_name)

@login_required
def gantt_detail(request, student_id=0):
    """
    Método que monsta o grafico do tempo do estudante em relação a suas atividades
    formato da informação = [
        id do nó, nome da atividade,resource da atividade, data de inicio da atividade pelo estudante , data fim,
        duração da atividade, porcentagem completada, dependencias
    ]
    """
    response = []
    student = Student.objects.get(pk=student_id)
    nodes = Node.objects.filter(students=student)
    #print(nodes)
    for node in nodes:
        student_informations = StudentInformations.objects.filter(student=student,node=node).first()
        information_format = [
            str(node.id), node.activity.first().name,None,str(student_informations.start_activity),str(student_informations.end_activity),
            None,student_informations.percentage_completed,None
        ]
        response.append(
            information_format
        )
    
    context = {
        "context":response
    }
    return JsonResponse(context)

class StudentInformationsDetail(APIView):
    """
    Retorna as informações de execução de atividade do aluno
    """

    def get(self,request,node_id,student_id):
        student_informations = StudentInformations.objects.filter(node__pk=node_id,student__pk=student_id).first()
        serializer = StudentInformationsSerializer(student_informations)
        student_serializer = StudentSerializer(Student.objects.get(pk=student_id))
        node_serializer = NodeSerializer(Node.objects.get(pk=node_id))
        context = {
            "student" : student_serializer.data,
            "node" : node_serializer.data,
            "student_informations" :serializer.data
        }
        return Response(context)


class TeacherDetail(APIView):
    """
    Retorna todas as informações do professor
    """
    def get(self,request,user_teacher_id):
        response = {}
        teacher = Teacher.objects.filter(user=user_teacher_id).first()
        teacher_serializer = TeacherSerializer(teacher)
        students = Student.objects.filter(classe__in=teacher.classe.all())
        student_serializer = StudentSerializer(students, many=True)
        classe_serializer = ClassesSerialzer(teacher.classe.all(), many=True)
        response = {
            "teacher" : teacher_serializer.data,
            "students" : student_serializer.data,
            "classes" : classe_serializer.data
        }
        return Response(response)

    
def calc_way(request,classe_id):
    """
    Método para calcular o caminho com melhor ou pior desempenho
    cálculo baseado nos nós e estudantes daquela classe
    """
    response = True
    try:
        way_choice = request.GET["way"]        
        best_way_choice = True if way_choice == 'best_way' else False  

        best_way = None
        classe = Classes.objects.get(pk=classe_id)
        nodes = Node.objects.filter(course=classe.course)
        nodes_end = nodes.filter(node_end=True)
        way = WayAvg(nodes_end[0])
        way.execute()
        best_way = way
        print("way")
        print(way.get_avg())

        for node_end in nodes_end[1:]:
            "Pega os nós folas"
            way = WayAvg(node_end)
            way.execute()
            if best_way_choice:
                print("melhor caminho")
                print(best_way.get_avg())
                if way.get_avg() > best_way.get_avg():
                    best_way = way
            else:
                print("Pior caminho")
                print(best_way.get_avg())
                if way.get_avg() < best_way.get_avg():
                    best_way = way
        
        print(best_way.get_nodes())

        for node in nodes:
            if node in best_way.get_nodes():
                node.is_way = True
            else:
                node.is_way = False
            node.save()
    except Exception as e:
        pass
        #print("não calculou")
        response = False

    return JsonResponse({"context":response})
