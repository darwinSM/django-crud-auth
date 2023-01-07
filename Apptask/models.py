from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task (models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    datecompleted = models.DateField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta():
        verbose_name = 'task'
        verbose_name_plural = 'tasks'


    def __str__(self):
        return self.titulo + " -  by  user: " + self.user.username