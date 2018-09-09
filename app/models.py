from django.db import models
from rest_framework.filters import OrderingFilter


# Create your models here.

class Classes(models.Model):
    name = models.CharField("Nome da Turma", max_length=50)
    course = models.ForeignKey("Course", verbose_name="Curso", on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField("Nome do Aluno", max_length=50)
    classe = models.ForeignKey(Classes, verbose_name="Turma", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField("Atividade", max_length=50)

    def __str__(self):
        return self.name

class Level(models.Model):
    depth = models.IntegerField("Nível")

    def __str__(self):
        return str(self.depth)

class Node(models.Model):
    name = models.CharField("Nome do Nós", max_length=50)
    activity = models.ManyToManyField(Activity, verbose_name="Atividades")
    students = models.ManyToManyField(Student, through="StudentInformations")
    node_parent = models.ForeignKey("self", verbose_name="Nó Pai", on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey("Course", verbose_name="Curso que o nó pertence", on_delete=models.CASCADE, blank=True, null=True)
    node_end = models.BooleanField("Nó fim (Folha)?",default=False)
    node_start = models.BooleanField("Nó inicio",default=False)
    depth = models.ForeignKey(Level, verbose_name=("Nível"), on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        ordering = ["depth"]

    def __str__(self):
        return str(self.name) +"-"+str(self.get_activities())
    
    def get_activities(self):
        return "\n".join([p.name for p in self.activity.all()])
    

    

class StudentInformations(models.Model):
    node = models.ForeignKey(Node, verbose_name="Nome do Nós", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name="Estudantes", on_delete=models.CASCADE)
    notes = models.DecimalField("Nota do Aluno", max_digits=2, decimal_places=2,blank=True, null=True)

class Course(models.Model):
    name = models.CharField("Nome do Curso", max_length=50)

    def __str__(self):
        return self.name
