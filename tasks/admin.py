from django.contrib import admin
from .models import Task
#Definimos una clase llamada TaskAdmin que hereda de admin.ModelAdmin. 
# Esta clase se utiliza para personalizar la visualización y el comportamiento del modelo Task
# en el panel de administración.
# Register your models here.
class TaskAdmin(admin.ModelAdmin):
  readonly_fields = ('created', ) #En el panel de administración created del modelo Task se muestre como solo lectura en el panel de administración. 
#Esto significa que el campo no se puede editar desde el panel de administración y solo se muestra para referencia.
admin.site.register(Task, TaskAdmin)

#Registramos el modelo Task en el panel de administración utilizando admin.site.register(). 
# Al pasar Task como primer argumento y TaskAdmin como segundo argumento, 
# le indicamos a Django que utilice la personalización definida en TaskAdmin para el modelo Task en el panel de administración.