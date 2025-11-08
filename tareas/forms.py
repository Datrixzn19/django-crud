#creado manualmente 

from django.forms import ModelForm

from .models import Tareas

class TaskForm(ModelForm):
    class Meta:
        model = Tareas 
        fields = ['titulo', 'descripcion', 'important'] #pongo los campos que quiero traer de mi modelo  