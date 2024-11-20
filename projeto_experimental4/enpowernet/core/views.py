from django.shortcuts import render, redirect
from bson import ObjectId
from django.http import HttpResponse, JsonResponse
from .models import usuario, projeto
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from datetime import date
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from .services import user_service
from core.forms import cadastro_forms, editar_perfil_forms, projeto_forms, editar_projeto_forms
import uuid
from django.contrib.sessions.models import Session
from enpowernet.settings import MONGO_URI  
from pymongo import MongoClient
from bson import ObjectId, Decimal128 
from PIL import Image

def add_usuario2(request):                 
    if request.method == 'POST':
        form = cadastro_forms(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.UUID = str(uuid.uuid4()) 
            user.set_password(form.cleaned_data['senha'])
            user.save()
            messages.success(request, "Usuário registrado com sucesso!")
            return redirect('/')
        
        context = {'form': form}
        return render(request, 'registro.html', context) 
    
    form = cadastro_forms()
    context = {'form': form}
    return render(request, 'registro.html', context)

def realizar_login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        user = authenticate(request, email=email, password=senha)

        if user is not None:
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            login(request, user)
            return redirect("/")  
        else:
            messages.error(request, "E-Mail ou Senha inválidos, tente novamente!")
            return redirect('realizar_login')  

    return render(request, 'login.html')

def logout(request):
    Session.objects.all().delete()
    return redirect("/")

def home(request):
    return render(request, 'home/home.html', {'user': request.user})

@login_required
def perfil(request):
    
    usuario = request.user
    nome_formatado = user_service.formata_nome(request.user.nome)
    numero_formatado = user_service.formata_numero(request.user.telefone)
    projetos = projeto.objects.filter(user_id=request.user.UUID)
    form = editar_perfil_forms(instance=request.user)
    
    context = {
        'nome': nome_formatado,
        'numero': numero_formatado,
        'projetos': projetos,
        'form': form,
        'usuario': usuario,
    }
 
    return render(request, 'index/perfil.html', context)

@login_required
def criar_projeto(request):
    if request.method == "POST":
        
        project = projeto(user_id=request.user.UUID)
        form = projeto_forms(request.POST, request.FILES, instance=project)
        
        if form.is_valid():
            project = form.save()
            messages.success(request, "Projeto criado com sucesso!")
            return redirect('perfil')

    project = projeto(user_id=request.user.UUID,)
    form = projeto_forms(instance=project)
    context = {'form': form}
    return render(request, 'index/criar_projeto.html', context)  
  

@login_required
def excluir_projeto(request, projeto_id):
    print(f"Buscando projeto com id_mongo={projeto_id}")
    projeto_obj = projeto.objects.filter(id_mongo=projeto_id).first()
    if projeto_obj:
        projeto_obj.delete()
        print("Projeto excluído")
    else:
        print("Projeto não encontrado")
    return redirect('perfil')



@login_required
def editar_usuario(request):
    if request.method == "POST":
        user = request.user
        form = editar_perfil_forms(request.POST, instance=user)
        
        if form.is_valid():
            user = form.save()
            messages.success(request, "Informações alteradas com sucesso!")
            return redirect('perfil')
        
    form = editar_perfil_forms(instance=user)
    context = {'form': form}
    return render(request, 'index/perfil.html', context)

def index(request):
    usuario = request.user
    project = projeto.objects.all()
    context = {
        "projetos": project,
        "usuario": usuario
    }
    return render(request, 'index/index.html', context)


@login_required
def editar_projeto(request, projeto_id):

    projeto_obj = projeto.objects.filter(id_mongo=projeto_id, user_id=request.user.UUID).first()

    if not projeto_obj:
        messages.error(request, "Projeto não encontrado ou você não tem permissão para editá-lo.")
        return redirect('perfil')

    if request.method == 'POST':
        form = editar_projeto_forms(request.POST, instance=projeto_obj)

        if form.is_valid():

            form.save()
            messages.success(request, "Projeto atualizado com sucesso!")
            return redirect('perfil') 
        else:

            messages.error(request, "Houve um erro ao atualizar o projeto. Verifique os dados.")
    else:

        form = editar_projeto_forms(instance=projeto_obj)


    context = {
        'form': form,
        'projeto': projeto_obj
    }
    return render(request, 'index/editar_projeto.html', context)



def detalhes_projeto(request, projeto_id):
    projeto_obj = projeto.objects.filter(id_mongo=projeto_id).first()
    user_obj = usuario.objects.filter(UUID = projeto_obj.user_id)
    if not projeto_obj:
        messages.error(request, "Projeto não encontrado.")
        return redirect('index')
    
    
    context = {
        "projeto": projeto_obj,
        "user": user_obj,
    }
    
    return render(request, 'index/post.html', context)
    



        