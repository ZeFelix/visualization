from django.db.models import Avg, Q
from app.models import StudentInformations, Classes, Student

class WayAvg:
    """
    Classe para calcular média de um caminho de atividades
    a partir de um nó folha ele soma e faz os calculos da média
    """

    def __init__(self,node_end):
        classe = Classes.objects.filter(course=node_end.course)
        self.cont = 0
        self.node = node_end
        self.students = Student.objects.filter(classe=classe.first())
        self.amount = 0
        self.nodes = []
    
    def execute(self):
        self.amount = self.sum(self.node, self.students)
        return True

    def get_count(self):
        return self.cont
    
    def get_avg(self):
        return self.amount/self.cont
    
    def get_nodes(self):
        return self.nodes

    def sum(self,node, students):
        if node == None:
            return 0
        else:
            self.nodes.append(node)
            avg = self.get_node_average(node,students)
            if not avg == None:
                self.cont += 1
                return avg + self.sum(node.node_parent, students)
            else:
                return 0 + self.sum(node.node_parent, students)

    def get_node_average(self, node, students):
        """
        calcula a média das notas dos alunos naquele nó para aquela atividade
        """
        students_ids = list(students.values_list("id", flat=True))
        average = StudentInformations.objects.filter(
            node=node.id, student__in=students_ids).aggregate(Avg('notes'))
 
        return average["notes__avg"]
    
