import uuid
from bson.binary import Binary
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from dateutil.relativedelta import relativedelta
from datetime import date

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class usuario(AbstractBaseUser):
    escolha_genero = (
        ('F', 'Feminino'),
        ('M', 'Masculino'),
        ('I', 'Indefinido'),  
    )
    UUID = models.BinaryField(primary_key=True, editable=False) 
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255)
    genero = models.CharField(max_length=1, choices=escolha_genero)
    telefone = models.CharField(max_length=11)
    data_nascimento = models.DateField(max_length=8, null=False, default=None)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'telefone', 'genero', 'data_nascimento']

    @property
    def idade(self):
        hoje = date.today()
        delta = relativedelta(hoje, self.data_nascimento)
        return delta.years

    def __str__(self):
        return self.nome  

    def save(self, *args, **kwargs):
        if not self.UUID:
             self.UUID = Binary(uuid.uuid4().bytes)
        super().save(*args, **kwargs)