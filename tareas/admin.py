from django.contrib import admin

from .models import Tareas #para que la tabla tenga acceso al panel de admimm


class taskAdmin(admin.ModelAdmin): #mostrando un "auto_now_add=True" en el panel de admin, antes se ponia solo y no se mostraba
    readonly_fields = ('fecha_creacion', )
    

# Register your models here.

#admin.site.register(Tareas) - antes 
admin.site.register(Tareas, taskAdmin)