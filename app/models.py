from django.db import models

# Create your models here.

class Step(models.Model):
    name = models.CharField("Nome da passo", max_length=50)

    def __str__(self):
        return self.name

class Classes(models.Model):
    name = models.CharField("Nome da Turma", max_length=50)
    step = models.ManyToManyField(Step, verbose_name="Passos")

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField("Nome do Aluno", max_length=50)
    classe = models.ForeignKey(Classes, verbose_name="Turma", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField("Atividade", max_length=50)
    student = models.ManyToManyField(Student, verbose_name="Estudantes")
    step = models.ManyToManyField(Step, verbose_name="Passos")

    class Meta():
        ordering = ['step__name']


    def __str__(self):
        return self.name

    def get_students(self):
        return "\n".join([p.name for p in self.student.all()])



