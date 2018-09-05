from app.models import *
from rest_framework import serializers

class StepSerializer(serializers.ModelSerializer):

    class Meta:
        model = Step
        fields = ["pk","name"]


class ClassesSerialzer(serializers.ModelSerializer):
    step = StepSerializer(many=True)

    class Meta:
        model = Classes
        fields = ['pk',"name","step"]

class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = ["pk","name"]
    
class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["pk","name"]