from django import forms
from .models import Task

class TaskForm(forms.ModelForm): #Definimos una clase llamada TaskForm que hereda de forms.ModelForm. Esta clase representa un formulario basado en un modelo para crear o editar una tarea.
    datestart = forms.DateTimeField( #Definimos un campo de formulario llamado datestart que representa la fecha de inicio de tareas.
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'YYYY-MM-DD HH:MM'}),
        label='Fecha de inicio de la Tarea:',
        input_formats=['%Y-%m-%dT%H:%M']
    )
    class Meta: #Definimos la clase interna Meta que proporciona metadatos adicionales para el formulario.
        model = Task #especifica que el modelo asociado al formulario es la clase Task.
        fields = ['title', 'description', 'important']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'important': 'Tarea Importante',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribir un Título'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribir una descripción'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'})
        }