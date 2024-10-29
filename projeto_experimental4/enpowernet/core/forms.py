from unicodedata import numeric
from django import forms 
from .models import usuario
from django.core.exceptions import ValidationError
from datetime import date

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
        fields = ["email", "nome", "genero", "telefone", "data_nascimento", "senha"]
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