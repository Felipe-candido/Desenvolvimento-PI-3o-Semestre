from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import usuario, projeto
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from datetime import date
from django.utils import timezone
from core.forms import cadastro_forms
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

def perfil(request):
    user = request.user
    return render(request, 'index/perfil.html', {'user': user})

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
        messages.success(request, "Projeto foi criado")
        return redirect("perfil/")

    return render(request, 'index/perfil.html')

@login_required
def buscar_projetos(request):
    project = projeto.objects.filter(user_id=request.user.UUID)
    return render(request, 'index/projetos.html', {'projetos': project})