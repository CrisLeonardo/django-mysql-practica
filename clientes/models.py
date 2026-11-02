from django.db import models


class Cliente(models.Model):
    nombre = models.CharField('Nombre', max_length=255)
    correo = models.EmailField('Correo', unique=True)

    def __str__(self):
        return f'{self.nombre} ({self.correo})'
