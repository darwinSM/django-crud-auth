from django.contrib import admin
from Apptask.models import Task


class TaskAdmin (admin.ModelAdmin):
    readonly_fields = ['created',]



# Register your models here.
admin.site.register(Task, TaskAdmin)
