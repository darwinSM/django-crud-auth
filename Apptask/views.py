from django.shortcuts import render, redirect, get_object_or_404
# UserCreationForm : crear usuario , AuthenticationForm: comprobar si el usuario existe
from django.contrib.auth. forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.models import User

# manejo de error IntegrityError (la condicion UNIQUE esta siendo afectada, duplicidad de username)
from django.db import IntegrityError

# login : Metodo para crear sesion, a partir del usuario i,e cookies (sesion guardada temporalemnte para el ususraio registrado)
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse

#Importamos formulario de forms
from Apptask.forms import TaskForm

from Apptask.models import Task
#para establecer una fecha y hora en las tareas completadas mediante actualzacion por la pagina
from django.utils import timezone
#proteger las rutas, permitiendo el ingreso a ellas solo cuando se este logueado
from django.contrib.auth.decorators import login_required



# Create your views here.

def home(request):
    return render(request, 'home.html')


# Crear usuario
def signup(request):

    if request.method == "GET":
        print("Mostrando formulario")
        return render(request, 'signup.html',
                      {
                          'form': UserCreationForm
                      }
                      )

    else:
        print(request.POST)
        print("Enviando datos")
        if request.POST["password1"] == request.POST["password2"]:

            # Como dJango puede crear usuarios a traves de la clase "User",
            # tambien nos permite usarla para registrar nuestros usuarios
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                user.save()
                # guadar cookies
                login(request, user)
                return redirect('Home')

            except IntegrityError:  # Error especifico
                return render(request, 'signup.html',
                              {
                                  'form': UserCreationForm,
                                  'alert': "Username already exist"
                              }
                              )

        else:
            return render(request, 'signup.html',
                          {
                              'form': UserCreationForm,
                              'alert': "password do not match"
                          }
                          )

@login_required
def signout(request):
    logout(request)
    return redirect('Home')


# iniciar sesion con usuario ya creado
def signin(request):

    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        print(request.POST)
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'alert' : "username or password is incorrect"
        })
        else:
            login(request, user)
            return redirect ('Home')

       
#Vista para Listar todas las tareas del usuario con la sesion activa
#este decorador se puede aplicar a las funciones que requieren proteccion
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user , datecompleted__isnull=True)
    return render(request, 'tasks.html' , {"tasks" : tasks})

@login_required
def tasks_complete_get(request):
    tasks = Task.objects.filter(user=request.user , datecompleted__isnull=False).order_by("datecompleted")
    return render(request, 'tasks_complete_get.html' , {"tasks" : tasks})


@login_required
def create_task(request):

    if request.method == 'GET':
        return render (request , 'create_task.html' , {
            'form' : TaskForm
    })
    else:
        try:
            print (request.POST)
            form = TaskForm(request.POST)
            #print (form)
            new_task = form.save(commit=False)   # commit= False --> devuelve solo los datos que estan en el formulario
            new_task.user = request.user
            #print (new_task)
            new_task.save()
            return redirect('Tasks')
        
        except ValueError:
            return render (request , 'create_task.html' , {
                'form' : TaskForm,
                'alert' : "Please provide valid data"
            })

      
@login_required       
def task_detail (request, task_id):
    #print(task_id)
    #task = Task.objects.get(id=task_id)
    #Para evitar que el servidor se caiga cuando se busca una tarea con id que no existe en la db, entonces se usa la forma:
    task = get_object_or_404 (Task, id= task_id, user=request.user)
    
    return render(request, 'task_detail.html' , {"task" : task})


@login_required    
def task_detail_update (request, task_id):
    
    if request.method == "GET":

        task = get_object_or_404 (Task, id=task_id, user=request.user)
        #para poder hacer una actualizacion de la tarea, podemos utilizar el fomulario TaskForm
        form= TaskForm(instance=task)
        return render(request, 'task_detail_update.html' , {
            "task" : task ,
            "form" : form
            })

    else:
        try:
            task = get_object_or_404 (Task,id=task_id, user=request.user)
            form= TaskForm(request.POST , instance=task)
            form.save()
            return redirect('Tasks')
        except ValueError:
            return render(request, 'task_detail_update.html' , {
            "task" : task ,
            "alert" : "Please provide valid data"
            })


@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == "POST":
        # si no tiene una fecha , es poruqe la tarea esta incompleta, y la funcion la marca como completa
        if not task.datecompleted:
            task.datecompleted = timezone.now()
            print(task.datecompleted)
            task.save()
            return redirect ('Tasks_complete_get')
        else:
            # si tiene una fecha , es poruqe la tarea esta completa, y la funcion la marca como incompleta
            task.datecompleted=None
            task.save()
            return redirect ('Tasks')


@login_required
def tasks_delete (request, task_id):
    task = get_object_or_404(Task , id=task_id , user=request.user)

    if request.method == "POST":
        task.delete()
        return redirect ("Tasks")



