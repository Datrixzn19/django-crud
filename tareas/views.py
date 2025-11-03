from django.shortcuts import render
from django.http import HttpResponse


from django.contrib.auth.models import User  

# Create your views here.

from django.contrib.auth.forms import UserCreationForm 

def signup(request):
    #return render(request, 'signup.html', {'form':UserCreationForm}) #el nombre form va a contener lo que devuelva el UserCreat...
    if request.method == 'GET':
        print("Metodo GET")
        return render(request, 'signup.html', {'form':UserCreationForm})
    else:
        print("Metodo POST")
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1']) #este user el el del orm de django 
                user.save()#esto lo guarda dentro de la BD
                return HttpResponse('Usuario guardado con exito')
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