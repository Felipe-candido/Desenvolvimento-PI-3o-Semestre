import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model
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
    UUID = models.CharField(max_length=36, primary_key=True, default=lambda: str(uuid.uuid4()), editable=False) 
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255)
    genero = models.CharField(max_length=1, choices=escolha_genero)
    telefone = models.CharField(max_length=11)
    data_nascimento = models.DateField()
    last_login = models.DateTimeField(null=True, blank=True)
    sobre = models.CharField(null=True, max_length=500)

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

class projeto(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    user_id = models.CharField(max_length=36)  
    meta_investidor = models.DecimalField(max_digits=10, decimal_places=2)  
    total_investidor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    data_criacao = models.DateTimeField(auto_now_add=True)  
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    @property
    def percentual_projeto(self):
        if self.meta_investidor > 0:
            return (self.total_investidor / self.meta_investidor) * 100
        return 0