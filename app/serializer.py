from app.models import *
from rest_framework import serializers

class StudentInformationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentInformations
        fields = ["pk","notes","node","student",'start_activity','end_activity',"amount_access",'percentage_completed']

class ClassesSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = ['pk',"name","course"]

class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = ["pk","name"]
    
class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["pk","name","classe"]
    
class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ["pk","name","activity","students","node_parent","node_end","evaluated","is_way",'avg_access']
    
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["pk","name","course"]

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"
    