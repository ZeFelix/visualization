from django.contrib import admin
from app.models import *
# Register your models here.

class ActivityAdmin(admin.ModelAdmin):
    list_filter = ('student', 'step')
    list_display = ('name', 'get_students')

admin.site.register(Step)
admin.site.register(Classes)
admin.site.register(Student)
admin.site.register(Activity,ActivityAdmin)
