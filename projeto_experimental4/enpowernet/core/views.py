from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import usuario, projeto
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from datetime import date
from django.utils import timezone
from .services import user_service
from core.forms import cadastro_forms, editar_perfil_forms
import uuid
from django.contrib.sessions.models import Session

def add_usuario2(request):                 
    if request.method == 'POST':
        form = cadastro_forms(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.UUID = str(uuid.uuid4())  # Gepeteco decidiu isso, se der errado me avisa
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
        title = request.POST.get("titulo")
        description = request.POST.get("descricao")
        meta = request.POST.get("meta_investidor")

    
        project = projeto(
            titulo=title,
            descricao=description,
            user_id=request.user.UUID,
            meta_investidor=meta
        )

        project.save()
        messages.success(request, "Projeto foi criado com sucesso!")
        return redirect("perfil")  

    return render(request, 'index/criar_projeto.html')  

# @login_required
# def buscar_projetos(request):
#     project = projeto.objects.all()
#     return render(request, 'index/projetos.html', {'projetos': project})


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
        
        