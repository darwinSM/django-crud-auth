from django import forms
from Apptask.models import Task
from django.contrib.auth.models import  User

class TaskForm (forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titulo' , 'descripcion' , 'important']

        #Las siguinetes lineas de codigo permiten añadir clases en el fomulario html para poder modificar su apariencia.
        # Este diccionar es para especificar otros atributos de los inputs que generados, pues mo hay acceso al html

        # attrs (atributos)
        # class (es la clase de html) 
        # form-control es la clase de bustrack
        #form-check-input (es una clase de bootstrap (toggle buttons))

        widgets = {
            "titulo" : forms.TextInput (attrs= {"class":'form-control' , "placeholder": "Write a title"}),
            "descripcion" : forms.Textarea (attrs= {"class":'form-control' , "placeholder" : "Write a description"}),
            "important" : forms.CheckboxInput (attrs= {"class":'form-check-input m-auto'})
        }
        


   