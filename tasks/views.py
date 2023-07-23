from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login,logout, authenticate
from django.utils import timezone
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    #return HttpResponse('<h1>Hola Mundillo</h1>')
    if request.method   == 'GET':
            return render(request, 'signup.html', {
        'form': UserCreationForm     
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
             #registrar usuario
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                #return HttpResponse('Usario grabado correctamente')
                return redirect('tasks')
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,     
                    "error": 'Usuario ya existe'
                })
                #return HttpResponse('Usuario ya existe')
    return render(request, 'signup.html', {
        'form': UserCreationForm,     
        "error": 'Password no coincide'
    })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user).order_by('-fechacompletada')#, fechacompletada__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})
    #return render(request, 'tasks.html')

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task':task, 'form':form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except:
            return render(request, 'task_detail.html', {'task':task, 'form':form,
                          'error': 'Algo salio mal con el Update'})
            
@login_required    
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.fechacompletada = timezone.now()
        print(timezone.now())
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required    
def tasks_completed(request):
    #tasks = Task.objects.filter(user=request.user, fechacompletada__isnull=False).order_by('-fechacompletada')
    tasks = Task.objects.filter(user=request.user).order_by('-fechacompletada')
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save() 
            return redirect('tasks')
        except:
            print(form)
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Error en los datos ingresados'
            })      

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form': AuthenticationForm
    })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,    
                'error': 'Usuario o Password incorrecto'   
            })
        else:
            login(request, user)
            return redirect('tasks')
        