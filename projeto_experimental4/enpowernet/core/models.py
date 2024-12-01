import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model
from dateutil.relativedelta import relativedelta
from datetime import date
from decimal import Decimal
from bson import Decimal128, ObjectId



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
    UUID = models.CharField(max_length=36, primary_key=True, default=lambda: str(uuid.uuid4()), editable=False) 
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=11, null=True, blank=True)
    data_nascimento = models.DateField()
    last_login = models.DateTimeField(null=True, blank=True)
    descricao = models.CharField(blank=True, null=True, max_length=50)
    cidade = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)
    foto = models.ImageField(upload_to="foto_usuarios/", null=True, blank=True)
    sobre = models.TextField(blank=True, null=True)

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
    escolha_categoria = (
        ('Tecnologia', 'Tecnologia'),
        ('Saude', 'Saúde'),
        ('Educação', 'Educação'),
        ('Meio_Ambiente', 'Meio Ambiente'),
        ('Economia', 'Economia'),
        ('Negocios', 'Negócios'),  
    )
    id_mongo = models.CharField(max_length=24, unique=True, primary_key=True)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(max_length=50)
    user_id = models.CharField(max_length=36)  
    meta_investidor = models.DecimalField(max_digits=10, decimal_places=2)  
    total_investidor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    data_criacao = models.DateTimeField(auto_now_add=True) 
    projeto_logo = models.ImageField(upload_to="projeto/")
    categoria = models.CharField(max_length=20, choices=escolha_categoria)
    sobre = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.titulo

    @property
    def percentual_projeto(self):
        if self.meta_investidor:  
            
            if isinstance(self.meta_investidor, Decimal128):
                meta_investimento = self.meta_investidor.to_decimal() 
            else:
                meta_investimento = self.meta_investidor  

            if isinstance(self.total_investidor, Decimal128):
                total_investido = self.total_investidor.to_decimal()  
            else:
                total_investido = self.total_investidor  

            if meta_investimento > 0:  
                percentual = (total_investido / meta_investimento) * 100
                return round(percentual, 2) 
        return 0  
    
    def save(self, *args, **kwargs):
        if isinstance(self.meta_investidor, Decimal128):
            self.meta_investidor = self.meta_investidor.to_decimal()

        if isinstance(self.total_investidor, Decimal128):
            self.total_investidor = self.total_investidor.to_decimal()

        if not self.id_mongo:
            self.id_mongo = str(ObjectId())
        
        super().save(*args, **kwargs)
        
        
class imagens(models.Model):
    projeto = models.ForeignKey(projeto, related_name="imagens", on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to="projeto/imagens/")
    
    def __str__(self):
        return f"Imagem de {self.projeto.titulo}"
