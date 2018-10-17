from django.contrib.auth.models import User
from django.db import models
from rest_framework.filters import OrderingFilter
from django.utils import timezone


# Create your models here.

class Classes(models.Model):
    name = models.CharField("Nome da Turma", max_length=50)
    course = models.ForeignKey(
        "Course", verbose_name="Curso", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Teacher(User):

    classe = models.ManyToManyField('Classes')

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"


class Student(models.Model):
    SEX_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminio'),
    )
    CIVIL_STATUS_CHOICES = (
        ('C', 'Casado'),
        ('S', 'Solteiro'),
    )
    SCHOLL_ORIGIN_CHOICES = (
        ('PB', 'Pública'),
        ('PA', 'Particular'),
    )

    name = models.CharField("Nome do Aluno", max_length=50)
    sex = models.CharField("Sexo", max_length=2,
                           choices=SEX_CHOICES, default="M")
    ager = models.IntegerField("Idade", default=0)
    civil_status = models.CharField(
        "Estado civil", max_length=2, choices=CIVIL_STATUS_CHOICES, default="S")
    school_origin = models.CharField(
        "Origem Escolar", max_length=2, choices=SCHOLL_ORIGIN_CHOICES, default="PB")
    classe = models.ForeignKey(
        Classes, verbose_name="Turma", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField("Atividade", max_length=50)
    start_date = models.DateField(
        "inicio da atividade", auto_now=False, auto_now_add=False, blank=True, null=True)
    end_date = models.DateField(
        "Fim da atividade", auto_now=False, auto_now_add=False, blank=True, null=True)
    

    def __str__(self):
        return self.name


class Node(models.Model):
    name = models.CharField("Nome do Nós", max_length=50)
    activity = models.ManyToManyField(Activity, verbose_name="Atividades")
    students = models.ManyToManyField(Student, through="StudentInformations")
    node_parent = models.ForeignKey(
        "self", verbose_name="Nó Pai", on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey("Course", verbose_name="Curso que o nó pertence",
                               on_delete=models.CASCADE, blank=True, null=True)
    node_end = models.BooleanField("Nó fim (Folha)?", default=False)
    node_start = models.BooleanField("Nó inicio", default=False)
    evaluated = models.BooleanField("Esse nó é avaliado?", default=True)

    def __str__(self):
        return str(self.name) + "-"+str(self.get_activities())

    def get_activities(self):
        return "\n".join([p.name for p in self.activity.all()])


class StudentInformations(models.Model):
    node = models.ForeignKey(
        Node, verbose_name="Nome do Nós", on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, verbose_name="Estudantes", on_delete=models.CASCADE)
    notes = models.DecimalField(
        "Nota do Aluno", max_digits=4, decimal_places=2, blank=True, null=True)
    start_activity = models.DateField("Iniciou a atividade", auto_now=False, auto_now_add=False, blank=True, null=True)
    end_activity = models.DateField("Iniciou a atividade", auto_now=False, auto_now_add=False, blank=True, null=True)
    amount_access = models.IntegerField("quantidade de acesso",default=0)
    percentage_completed = models.IntegerField(
        "Porcentagem concluida", default=0)


class Course(models.Model):
    name = models.CharField("Nome do Curso", max_length=50)

    def __str__(self):
        return self.name
