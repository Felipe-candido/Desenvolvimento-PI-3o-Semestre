from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from unicodedata import numeric
from django import forms 
from .models import usuario, projeto, imagens, comentarios
from django.core.exceptions import ValidationError
from datetime import date
from bson import Decimal128, ObjectId
from decimal import Decimal, InvalidOperation
from PIL import Image

class cadastro_forms(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Senha',
                'required': 'required',
            }),
            )
    
    class Meta:
        model = usuario
        fields = ["email", "nome", "data_nascimento", "senha"]
        labels = {'email': 'Email',
                  'nome': 'Nome', 
                  'data_nascimento': 'Data de nascimento', 
                  'senha': 'Senha'}
        widgets = {
            'data_nascimento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'required': 'required',
                }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo',
                'required': 'required',
                }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemplo@mail.com',
                'required': 'required',
                }),
        }
        
    def clean_email(self):
        this_email = self.cleaned_data.get('email')
        try:
            if usuario.objects.filter(email=this_email).exists():
                raise ValidationError('Esse e-mail já está cadastrado.')
        except Exception as e:
            raise ValidationError(f'Esse e-mail já está cadastrado.')
        return this_email
        
    def clean_nome(self):
        nome = self.cleaned_data['nome']
        return str(nome).title()
    
    
         
    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data['data_nascimento']
        hoje = date.today()
        if data_nascimento > hoje:
            raise ValidationError('Data inválida')
        return data_nascimento
        
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['senha'])
        if commit:
            user.save()
        return user     
    
    
    

class editar_perfil_forms(forms.ModelForm): 
    class Meta:
        model = usuario
        fields = ["nome", "telefone", "descricao", "cidade", "estado", "foto", "sobre"]
        labels = {
            'nome': 'Nome Completo',
            'telefone': 'Telefone de Contato',
            'descricao': 'Breve descrição',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'foto': 'Foto do perfil',
            'sobre': 'Sobre mim',
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome',
                'required': 'required',
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefone',
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'sobre',
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade',
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Estado',
            }),
            'foto': forms.FileInput(attrs={
            'class': 'form-control',
            }),
            'sobre': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Fale mais sobre você(cursos, formação, etc...)',
            }),
        }
        
        def clean_nome(self):
            nome = self.cleaned_data['nome']
            return str(nome).title()
        
        def clean_cidade(self):
            cidade = self.cleaned_data['cidade']
            return str(cidade).title()
        
        def clean_estado(self):
            estado = self.cleaned_data['estado']
            return str(estado).upper()
        
        def clean_data_nascimento(self):
            data_nascimento = self.cleaned_data['data_nascimento']
            hoje = date.today()
            if data_nascimento > hoje:
                raise ValidationError('Data inválida')
            return data_nascimento
        
        
        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['senha'])
            if commit:
                user.save()
            return user
        
        
        def clean_telefone(self):
            telefone = self.cleaned_data['telefone']
            if telefone.isnumeric():
                if len(telefone) == 11:
                    return telefone
                raise ValidationError('Telefone inválido, verifique a quantidade de digitos e coloque apenas numeros (lembrem-se de colocar o ddd)')
            raise ValidationError('Telefone inválido, verifique a quantidade de digitos e coloque apenas numeros (lembrem-se de colocar o ddd)')
 
 
 
    
class projeto_forms(forms.ModelForm):
    categoria = forms.ChoiceField(
        choices=[('', 'Escolha a categoria'), *projeto.escolha_categoria],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required',
        }),
    )
     
    class Meta:
        model = projeto
        fields = ("titulo", "descricao", "meta_investidor",  "projeto_logo", "categoria", "sobre")
        labels = {
            'titulo': 'Nome do projeto',
            'descrição': 'Sobre o projeto',
            'meta_investidor': 'Meta de investimento',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titulo',
                'required': 'required',
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Breve descrição',
                'required': 'required',
            }),
            'meta_investidor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Meta',
                'step': '0.01',
            }),
            'projeto_logo': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'sobre': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Fale mais sobre o projeto(objetivos, impactos, etc...)',
            }),
        }
        
        def clean_titulo(self):
            titulo = self.cleaned_data['titulo']
            return str(titulo).title()
        
        def clean_categoria(self):
            categoria = self.cleaned_data['categoria']
            return str(categoria).upper()
        
        def save(self, commit=True):
            projeto1 = super().save(commit=False)
            if commit:
                projeto1.save()
            return projeto1
        
        

class imagens_forms(forms.ModelForm):
    class Meta:
        model = imagens
        fields = ['imagem']            
 

class editar_projeto_forms(forms.ModelForm):
    class Meta:
        model = projeto
        fields = ['titulo', 'descricao', 'meta_investidor', 'projeto_logo', 'sobre']
        labels = {
            'titulo': 'Nome do projeto',
            'descrição': 'Sobre o projeto',
            'meta_investidor': 'Meta de investimento',
            'projeto_logo': 'Ilustração do projeto'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titulo do projeto',
                'required': 'required',
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição do projeto',
                'required': 'required',
            }),
            'meta_investidor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Meta de investimento',
                'step': '0.01',
            }),
            'sobre': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Fale mais sobre o projeto(objetivos, impactos, etc...)',
            }),
        }

    def clean_meta_investidor(self):
        meta_investidor = self.cleaned_data.get('meta_investidor')


        if isinstance(meta_investidor, Decimal128):
            return meta_investidor.to_decimal()


        if isinstance(meta_investidor, str):
            meta_investidor = meta_investidor.replace('“', '').replace('”', '') 
            meta_investidor = meta_investidor.strip()  

        try:

            return Decimal(meta_investidor)
        except (ValueError, InvalidOperation):
            raise forms.ValidationError('Valor inválido para meta_investidor. Deve ser um número decimal válido.')

        return meta_investidor
    
    def clean_titulo(self):
        titulo = self.cleaned_data['titulo']
        return str(titulo).title()
    
    
class forms_login(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={'placeholder': 'Digite seu e-mail', 'class': 'form-control'}),
    )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha', 'class': 'form-control'}),
    )   
    
    
class forms_comentarios(forms.ModelForm):
    class Meta:
        model = comentarios
        fields = ['texto']
        widgets = {
        'sobre': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Fale mais sobre o projeto(objetivos, impactos, etc...)',
            }),
        }
            
            
    