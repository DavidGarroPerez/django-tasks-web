from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=1000)
  created = models.DateTimeField(auto_now_add=True)
  datestart = models.DateTimeField(null=True, blank=True)
  datecompleted = models.DateTimeField(null=True, blank=True)
  important = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE) # on_delete=models.CASCADE hace que si se elimina un usuario, se elimine todas las tareas creadas relacionadas al usuario. 

  def __str__(self):
    return self.title + ' - ' + self.user.username
#Sobrescribimos el método __str__() para proporcionar una representación legible de la tarea. 
# Devuelve una cadena que combina el título de la tarea con el nombre de usuario del usuario asociado.