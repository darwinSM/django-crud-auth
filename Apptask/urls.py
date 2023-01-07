from django.urls import path
from Apptask import views


urlpatterns = [
    path('', views.home, name='Home'),
    path('signup/', views.signup , name='Signup' ) ,
    path('signout/', views.signout, name="Signout"),
    path('signin/', views.signin , name='Signin'),
    path('tasks/create/', views.create_task, name="Create_tasks"),
    path('tasks/', views.tasks , name="Tasks"),
    path('tasks_complete_get/', views.tasks_complete_get , name="Tasks_complete_get"),
    path('tasks/<int:task_id>/', views.task_detail , name="Task_detail"),
    path('tasks/<int:task_id>/update/', views.task_detail_update , name="Task_detail_update"),
    path('tasks/<int:task_id>/complete/', views.task_complete , name="Task_complete"),
    path('tasks/<int:task_id>/delete/', views.tasks_delete , name="Task_delete"),
]
