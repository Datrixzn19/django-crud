from django.db import models

from django.contrib.auth.models import User #para la FK
# Create your models here.


class Tareas(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True) #si no me pasan nada por defecto va a estar vacio 
    #fecha en la que fue creada
    fecha_creacion = models.DateTimeField(auto_now_add=True) # al crearla se agregara la fecha actual si no le pasamos 
    #fecha en la que la tarea se marco como completada  
    dia_completada = models.DateTimeField(null=True, blank=True)#permite valores nulos, campo es opcional durante la validación del formulario
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # le indicamos con quien se va a realacionar 

    def __str__(self): #cuando lo usen como un string..
        return self.titulo + ' por: ' + self.user.username