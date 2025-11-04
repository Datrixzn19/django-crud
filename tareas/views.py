from django.shortcuts import render, redirect
from django.http import HttpResponse



from django.contrib.auth.models import User #modelo de bd, guarda nombre contras.... etc
from django.contrib.auth import login, logout, authenticate # solo para guardar datos de una sesion en el navegador, validar usuarios  
# Create your views here.

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #crear usuario, comprobar si existe

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
    return render(request, "hello.html")

def tareas(request):
    return render(request, 'tareas.html')

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
            return redirect('tareas')
    
    