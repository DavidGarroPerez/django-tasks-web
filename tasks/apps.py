from django.apps import AppConfig


class TasksConfig(AppConfig): #Definimos una clase llamada TasksConfig que hereda de AppConfig. Esta clase representa la configuración específica de la aplicación "tasks".
    default_auto_field = 'django.db.models.BigAutoField'#Establecemos el valor de default_auto_field para especificar el tipo de campo automático predeterminado utilizado para las claves primarias en los modelos de esta aplicación.
    name = 'tasks'#Especificamos el nombre de la aplicación como 'tasks'. Este nombre se utiliza para identificar y referenciar la aplicación dentro de Django.
