from django.db import models

# Create your models here.

class usuario(models.Model):
    escolha_genero = (
        ('F', 'Feminino'),
        ('M', 'Masculino'),
        ('I', 'Indefinido'),  
    )
    email = models.EmailField(primary_key=True)
    nome = models.CharField(max_length=255)
    senha = models.CharField(max_length=255)
    genero = models.CharField(max_length=1, choices=escolha_genero)
    telefona = models.CharField(max_length=12)
