from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    datestart = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'YYYY-MM-DD HH:MM'}),
        label='Fecha de inicio de la Tarea:',
        input_formats=['%Y-%m-%dT%H:%M']
    )
    class Meta:
        model = Task
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