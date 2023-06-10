from django.shortcuts import render, redirect, get_object_or_404 #Importa las funciones necesarias para renderizar plantillas, redireccionar y obtener objetos o mostrar una página de error 404.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #Importa los formularios de creación de usuario y autenticación de usuario provistos por Django.
from django.contrib.auth import login, logout, authenticate #Importa funciones relacionadas con la autenticación de usuarios, como iniciar sesión, cerrar sesión y autenticar credenciales de usuario.
from django.contrib.auth.models import User #Importa funciones relacionadas con la autenticación de usuarios, como iniciar sesión, cerrar sesión y autenticar credenciales de usuario.
from django.db import IntegrityError #Importa la excepción `IntegrityError` que puede ocurrir al intentar crear un usuario con un nombre de usuario que ya existe.
from django.utils import timezone # Importa la utilidad `timezone` de Django para manejar la fecha y hora con respecto a la zona horaria.
from django.contrib.auth.decorators import login_required #Importa el decorador `login_required` que se utiliza para restringir el acceso a vistas solo a usuarios autenticados.
from .models import Task #Importa el modelo `Task` definido en el archivo `models.py` de la misma aplicación.
from datetime import datetime #Importa la clase `datetime` del módulo `datetime` para trabajar con fechas y horas.
from .forms import TaskForm #Importa el formulario `TaskForm` definido en el archivo `forms.py` de la misma aplicación.

#Estas son las importaciones que se utilizan para importar las dependencias necesarias y definir el comportamiento de las vistas en el archivo `views.py`.

# Create your views here.

# Vista para registrar un nuevo usuario
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:
        # Comprueba si las contraseñas coinciden
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # Crea un nuevo usuario y lo guarda en la base de datos
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                # Inicia sesión con el nuevo usuario y redirige a la página de tareas
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                # Si ocurre un error de integridad (nombre de usuario duplicado), muestra un mensaje de error
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})
        # Si las contraseñas no coinciden, muestra un mensaje de error
        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})

# Vista de inicio para mostrar las tareas del usuario autenticado
@login_required
def tasks(request):
    # Obtiene todas las tareas del usuario que aún no están completadas
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})

# Vista para mostrar las tareas completadas del usuario autenticado
@login_required
def tasks_completed(request):
    # Obtiene todas las tareas del usuario que están completadas y las ordena por la fecha de completado descendente
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})

# Vista para crear una nueva tarea
@login_required
def create_task(request):
    if request.method == "GET":
        # Muestra el formulario vacío para crear una tarea
        form = TaskForm()
        return render(request, 'create_task.html', {"form": form})
    else:
        try:
            form = TaskForm(request.POST)
            if form.is_valid():
                # Crea una instancia de tarea a partir de los datos del formulario y la guarda en la base de datos
                task = form.save(commit=False)
                task.user = request.user
                created_date_str = request.POST.get('datestart')  # Obtiene la fecha de inicio del formulario
                if created_date_str:
                    task.datestart = datetime.strptime(created_date_str, '%Y-%m-%dT%H:%M')
                task.save()
                return redirect('tasks')
        except ValueError:
            # Si ocurre un error al crear la tarea, muestra un mensaje de error
            return render(request, 'create_task.html', {"form": TaskForm, "error": "Error creating task."})


# Vista para crear una nueva tarea
def home(request):
    return render(request, 'home.html')

# Vista para cerrar sesión
def signout(request):
    # Cierra la sesión del usuario y redirige a la página de inicio
    logout(request)
    return redirect('home') 

# Vista para iniciar sesión
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        # Autentica al usuario con las credenciales proporcionadas
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            # Si el usuario no existe o las credenciales son incorrectas, muestra un mensaje de error
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        # Inicia sesión con el usuario autenticado y redirige a la página de tareas
        login(request, user)
        return redirect('tasks')

# Vista para ver los detalles de una tarea y modificar o actualizar su estado 
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        # Obtiene la tarea especificada por su ID y perteneciente al usuario autenticado
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        # Crea un formulario con los datos de la tarea para mostrar y editar los detalles
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            # Obtiene la tarea especificada por su ID y perteneciente al usuario autenticado
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            # Si ocurre un error al actualizar la tarea, muestra un mensaje de error
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task.'})

# Vista para marcar una tarea como completada
@login_required
def complete_task(request, task_id):
    # Obtiene la tarea especificada por su ID y perteneciente al usuario autenticado
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        # Establece la fecha de completado de la tarea como la fecha y hora actual
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


#Vista para eliminar una tarea
@login_required
def delete_task(request, task_id):
    # Obtiene la tarea especificada por su ID y perteneciente al usuario autenticado
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        # Elimina la tarea de la base de datos
        task.delete()
        return redirect('tasks')