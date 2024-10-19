from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import usuario
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.hashers import make_password


def add_usuario(request):
    if request.method == 'POST':
        name = request.POST.get("nome")
        mail = request.POST.get("email")
        password = request.POST.get("senha")
        gender = request.POST.get("genero")
        phone = request.POST.get("telefone")

        if usuario.objects.filter(email=mail).exists():
            messages.error(request, "E-mail já cadastrado, insira um e-mail válido.")
            return redirect('registro') # Importante lembrar mais tarde de mudar a url para registro.
        
        cripto_senha = make_password(pwd)
        users = usuario(nome=name, email=mail, senha=cripto_senha,genero=gender, telefone=phone)
        users.save()
    
        user = usuario.objects.create_user(username=name, email=mail, password=pwd)
        login(request,user)

        return redirect("/") #Importante lembrar mais tarde de mudar a url aqui também
    
    return redirect(request, 'registro.html') #Importante... ja cansaram de ouvir 

def home(request):
    return render(request, 'home/home.html')