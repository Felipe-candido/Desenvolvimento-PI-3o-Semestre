from unicodedata import numeric
from django import forms 
from .models import usuario, projeto
from django.core.exceptions import ValidationError
from datetime import date
from bson import Decimal128, ObjectId
from decimal import Decimal, InvalidOperation

class cadastro_forms(forms.ModelForm):
    genero = forms.ChoiceField(
            choices=[('', 'Escolha o gênero'), *usuario.escolha_genero],
            widget=forms.Select(attrs={
                'class': 'form-control',
                'required': 'required',
            }),
            )
    senha = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Senha',
                'required': 'required',
            }),
            )
    
    class Meta:
        model = usuario
        fields = ["email", "nome", "genero", "telefone", "data_nascimento", "senha", "cidade", "estado"]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Nome',
                'required': 'required',
                }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome',
                'required': 'required',
                }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'required': 'required',
                }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefone',
                'required': 'required',
                }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade',
                'required': 'required',
                }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Estado',
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
        
        
    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if telefone.isnumeric():
            if len(telefone) == 11:
                return telefone
            raise ValidationError('Telefone inválido, verifique a quantidade de digitos e coloque apenas numeros (lembrem-se de colocar o ddd)')
        raise ValidationError('Telefone inválido, verifique a quantidade de digitos e coloque apenas numeros (lembrem-se de colocar o ddd)')
    
        
        
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
        fields = ["nome", "telefone", "sobre", "cidade", "estado"]
        labels = {
            'nome': 'Nome Completo',
            'telefone': 'Telefone de Contato',
            'sobre': 'Sobre Você',
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
                'required': 'required',
            }),
            'sobre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'sobre',
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade',
                'required': 'required',
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Estado',
                'required': 'required',
            }),
        }
        
        
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
     
    class Meta:
        model = projeto
        fields = ("titulo", "descricao", "meta_investidor",  "projeto_img")
        labels = {
            'titulo': 'Nome do projeto',
            'descrição': 'Sobre o projeto',
            'meta_investidor': 'Meta de investimento',
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
            'projeto_img': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }
        
        def save(self, commit=True):
            projeto1 = super().save(commit=False)
            if commit:
                projeto1.save()
            return projeto1
            
 

class editar_projeto_forms(forms.ModelForm):
    class Meta:
        model = projeto
        fields = ['titulo', 'descricao', 'meta_investidor', 'projeto_img']
        labels = {
            'titulo': 'Nome do projeto',
            'descrição': 'Sobre o projeto',
            'meta_investidor': 'Meta de investimento',
            'projeto_img': 'Ilustração do projeto'
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