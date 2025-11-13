from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse



from django.contrib.auth.models import User #modelo de bd, guarda nombre contras.... etc
from django.contrib.auth import login, logout, authenticate # solo para guardar datos de una sesion en el navegador, validar usuarios  
# Create your views here.

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #crear usuario, comprobar si existe


from .forms import TaskForm # mi modelo de formulario creado a partir de una tabla 


from .models import Tareas # para listarlas 

from django.utils import timezone

def signup(request):#crear una sesion
    if request.method == 'GET':
        print("Metodo GET")
        return render(request, 'signup.html', {'form':UserCreationForm})#el nombre form va a contener lo que devuelva el UserCreat...
    else:
        print("Metodo POST")
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1']) #este user el el del orm de django 
                user.save()#esto lo guarda dentro de la BD
                login(request, user) #pasamos el usuario para que guarde la sesion 
                return redirect('tareas')
            except:
                return render(request, 'signup.html', {
                    'form':UserCreationForm,
                    "error": 'este ususario ya existe'}) 
        
        
        return render(request, 'signup.html', {
                    'form':UserCreationForm,
                    "error": 'las contraseñas no coinciden'})
        

def home(request):
    return render(request, "home.html")

def hello(request):
    return render(request, 'hello.html')

def dashboard(request):
    return render(request, 'dashboard.html')



def signout(request):#cerrar la sesion actual ---cuidado con ponerle de nombre logout pq puede haber conflictos 
    logout(request)
    return redirect('home')

def signin(request): #logearse con una cuenta ya creada 
    if request.method=='GET':
        return render(request, 'signin.html', {'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password']) #si es valido devuelve un user, sino pues estara vacio 
        print(user)
        if user is None:
            return render(request, 'signin.html', 
                          {'form':AuthenticationForm, 
                          'error':'Credenciales incorrectas'})
        else:
            login(request, user)#guardamos su sesion porque sus credenciales son validas 
            return redirect('dashboard')
    



# C R U D
def tareas(request):
    #listar = Tareas.objects.all() # todas las tareass de la BDD, pero aqui incluso veo las tareas de otros usuarios 
    listar = Tareas.objects.filter(user=request.user, dia_completada__isnull=True)#solo muestra las tareas que sean del usuario actual
    # listar = Tareas.objects.filter(user=request.user, dia_completada__isnull=True) se puede poner otros filtros, aqui ponemos solo las tareas no completadas 


    return render(request, 'tareas.html', {'listar_tareas':listar})


def crear_tarea(request):
    if request.method == 'GET':
        return render(request, 'crear_tarea.html', {'form': TaskForm})#TaskForm es un form que creé a partir de una tabla
    else:
        #print(request.POST) imprime los datos que pusimos 
        try:
            form = TaskForm(request.POST) # le pasamos el form a TaskForm para que el cree el formulario 
            new_task = form.save(commit=False)#save es para guardar en una instacia de BD, pero al pasar commit false ya no lo hace, pq aqui solo quiero que me devuelva los datos que estan dentro del formulario 
            new_task.user = request.user # necesitamos pasarle un usuario para completar todos los datos 
            new_task.save() #ahora si lo guardamos dentro de la BD
            return redirect('tareas')
        except ValueError:
            return render(request, 'crear_tarea.html', {
                'form': TaskForm, 
                "error":'Datos no validos'}
                )



def tarea_detalles(request, id_tarea):
    if request.method=='GET':
        #tarea = Tareas.objects.get(pk=id_tarea) si no encuentra cae en servidor
        tarea = get_object_or_404(Tareas, pk=id_tarea) # hay que pasarle a cual modelo consultar 
        form = TaskForm(instance=tarea) # instance=tarea le dice al formulario que se precargue con los datos de la tarea obtenida.
        return render(request, 'tarea_unica.html', {'tarea':tarea, 'form':form})
    else:
        tarea = get_object_or_404(Tareas, pk=id_tarea) # hay que pasarle a cual modelo consultar 
        form = TaskForm(request.POST, instance=tarea) #instance=tarea vincula el formulario a la tarea existente, asegurando que los cambios se apliquen a este objeto en la base de datos es actualización, no nueva creación)
        form.save()
        return redirect('tareas')

def tarea_completada(request, id_tarea):
    tarea = get_object_or_404(Tareas, user=request.user, pk=id_tarea)
    if request.method == 'POST':
        tarea.dia_completada = timezone.now() # es para al ponerle ya una fecha sepamos que ha sido completada
        tarea.save()
        # tarea.delete() si la quisieramos borrar 
        return redirect('tareas')