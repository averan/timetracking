from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechacompletada = models.DateTimeField(null=True)
    horastotales = models.IntegerField(default=0, null=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)  
    
    #on_delete=models.CASCADE)...esto si queremos borrar en cascada la tabla de tareas si se borra un usario

    def __str__(self):
        return self.titulo + '- by ' + self.user.username


