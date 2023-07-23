from django import forms
from .models import Task
#from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput

class DateInput(forms.DateInput):
    input_type = 'date'

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titulo', 'descripcion', 'fechacompletada', 'horastotales']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa el nombre de la Tarea'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingresa breve detalle de la Tarea'}),
            'fechacompletada': DateInput(),
            'horastotales': forms.NumberInput(attrs={'class': 'form-control'})
        }

