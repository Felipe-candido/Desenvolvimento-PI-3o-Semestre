from django.db import models

# Create your models here.

class usuario(models.Model):
	escolha_genero = (
        ('F', 'Feminino',),
        ('M', 'Masculino',),
        ('I', 'indefinido',),
    )
	email = models.EmailField(primary_key=True)
	nome = models.CharField(max_length=255)
	senha = models.CharField(max_length=20)
	genero = models.CharField(max_length=1, choices=escolha_genero)
	telefone = models.CharField(max_length=12)






