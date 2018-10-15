from django.contrib import admin

from app.models import *


# Register your models here.

class StudentInformationsInline(admin.TabularInline):  
    model = StudentInformations 
    extra = 1 

class StudentAdmin(admin.ModelAdmin): 
    list_display = ("name","classe")

class NodesAdmin(admin.ModelAdmin): 
    inlines = (StudentInformationsInline,) 
    list_display = ("name","get_activities","node_parent")

admin.site.register(Classes)
admin.site.register(Student,StudentAdmin)
admin.site.register(Activity)
admin.site.register(Node,NodesAdmin)
admin.site.register(Course)
admin.site.register(Teacher)
