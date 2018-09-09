from django.contrib import admin
from app.models import *
# Register your models here.

class StudentInformationsInline(admin.TabularInline):  
    model = StudentInformations 
    extra = 1 

class NodestAdmin(admin.ModelAdmin): 
    inlines = (StudentInformationsInline,) 
    list_display = ("name","get_activities","node_parent","depth")

admin.site.register(Classes)
admin.site.register(Student)
admin.site.register(Activity)
admin.site.register(Node,NodestAdmin)
admin.site.register(Course)
