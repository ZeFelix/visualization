from signal import signal

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


# Create your views here.


class AllList(APIView):
    """
    Classe para listar todas as turmas do curso e seu nó raiz
    Método http permuitido: get
    """

    def get(self, request):
        user_teacher_id = request.query_params.get('user_teacher_id')
        informations = []
        if user_teacher_id == None:
            classes = Classes.objects.all()
        else:
            teacher = Teacher.objects.filter(user=user_teacher_id).first()
            classes = teacher.classe.all()

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
                Q(civil_status=married) | Q(civil_status=not_married), ager__range=(start_ager, end_ager))
        except Exception as a:
            students = node.students.all()
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
                    node_avg = -1    
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
                "student_informations": student_informations_serializer.data              
            }
        elif node.students.count():
            # se não tiver aluno após o filtro
            # porém existem alunos naquele nó, ele adiciona uma média negativa (-1) para indicar a cor do caminho(link)
            node_formatation = {
                "node_name": node.name,
                "node_id": node.id,
                "node_avg": -1,
                "name": node.activity.first().name,
                "students": [],
                "student_informations": []
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
def index(request, template_name="index.html"):
    return render(request, template_name)

def login_user(request, template_name="login.html"):
    """
    Método para realizar login
    """
    nex = request.GET.get("next", "/api")
    if request.user.is_authenticated:
        return HttpResponseRedirect('/api')
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request,username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(nex)
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
    print(context)
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
        response = {
            "teacher" : teacher_serializer.data,
            "students" : student_serializer.data
        }
        return Response(response)

    
def calc_way(request,classe_id):
    """
    Método para calcular o caminho com melhor ou pior desempenho
    cálculo baseado nos nós e estudantes daquela classe
    """
    try:
        way = request.GET["way"]        
        signal = -1 if way == 'best_way' else 1   

        classe = Classes.objects.first()
        
        graph = Graph()

        nodes = Node.objects.filter(course=classe.course)
        node_conextion = nodes.filter(end_node_conexction=True).first()
        node_start = nodes.filter(node_start=True).first()
        students = Student.objects.filter(classe=classe)
        for node in nodes:
            node_parent = node.node_parent
            if not node.node_start and not node.end_node_conexction:
                avg_node = NodeDetail.get_node_average(node,students)
                if avg_node == None:
                    avg_node = 10
                graph.add_edge(node_parent.id,node.id,{'cost':avg_node*signal})
                #print(str(node_parent.id)+"->"+str(node.id)+":"+str(avg_node))
            if node.node_end:
                """
                Conecta todos os nós avaliação a um só nó
                """
                graph.add_edge(node.id,node_conextion.id,{'cost':0})
        
        cost_func = lambda u, v, e, prev_e: e['cost']
        u = node_start.id
        v = node_conextion.id
        node_ids = find_path(graph, u, v, cost_func=cost_func).nodes
        #print(node_ids)
        
        for node in nodes:
            if node.id in node_ids:
                node.is_way = True
            else:
                node.is_way = False
            
            node.save()
        print("calculou")
    except Exception as e:
        pass
        print("não calculou")
    
    return JsonResponse({})