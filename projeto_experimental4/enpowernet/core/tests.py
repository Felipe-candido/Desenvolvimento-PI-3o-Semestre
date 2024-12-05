from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from .forms import cadastro_forms
from .models import usuario, projeto
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class UsuarioTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(
            email='gabriel.futurisss@gmail.com',
            nome='Gabriel Schranck',
            telefone='19983492015',
            data_nascimento='2003-06-02',
            cidade='Leme',
            estado='SP',
            password = '123mudar'
        )

        self.client.login(email = 'gabriel.futurisss@gmail.com', password = '123mudar')

    def test_returno_str(self):
         user = User.objects.get(email='gabriel.futurisss@gmail.com')
         self.assertEqual(str(user), 'Gabriel Schranck')
    

class CadastroFormTest(TestCase):

    def setUp(self):
        self.valid_data = {
            'email': 'gabriel.futurisss@gmail.com',
            'nome': 'Gabriel Schranck',
            'telefone': '19983492015',
            'data_nascimento': '2003-06-02',
            'senha': 'macacodasilva23',
            'cidade': 'Leme',
            'estado': 'SP',
        }
       

    def test_valid_form(self):
        form = cadastro_forms(self.valid_data)
        self.assertTrue(form.is_valid())

    def test_email_ja_cadastrado(self):
        usuario.objects.create_user(
            email=self.valid_data['email'],
            nome=self.valid_data['nome'],
            telefone=self.valid_data['telefone'],
            data_nascimento=self.valid_data['data_nascimento'],
            cidade=self.valid_data['cidade'],
            estado=self.valid_data['estado'],
        )
        form = cadastro_forms(self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Esse e-mail já está cadastrado.', form.errors['email'])

    def test_nome_formatado(self):
        data = self.valid_data.copy()
        data['nome'] = 'gabriel schranck'
        form = cadastro_forms(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['nome'], 'Gabriel Schranck')

    def test_data_nascimento_invalida(self):
        data = self.valid_data.copy()
        data['data_nascimento'] = f"{date.today().year + 1}-01-01"  
        form = cadastro_forms(data)
        self.assertFalse(form.is_valid())
        self.assertIn('Data de nascimento não pode estar no futuro.', form.errors['data_nascimento'])

    def test_save_form(self):
       form = cadastro_forms(self.valid_data)
       self.assertTrue(form.is_valid())
       form.save()
       user = usuario.objects.get(email=self.valid_data['email'])
       self.assertTrue(user.check_password(self.valid_data['senha']))




class ViewTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'email': 'gabriel.futurisss@gmail.com',
            'nome': 'Gabriel Schranck',
            'telefone': '19983492015',
            'data_nascimento': '2003-06-02',
            'senha': 'sucodelaranja',
            'cidade': 'Leme',
            'estado': 'SP',
        }
    
    def teste_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')
    
class View_tests_login(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='gabriel.futurisss@gmail.com', password='sucodelaranja')
    
    def teste_perfil_view(self):
        response = self.client.get(reverse('perfil'))
        self.assertRedirects(response, '/login/?next=/perfil/')
    
    def teste_perfil_view_logado(self):
        self.client.login(email='gabriel.futurisss@gmail.com', password='sucodelaranja')
        response = self.client.get(reverse('perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/perfil.html')
    
    # def teste_perfil_publico(self):
    #     self.client.login(email='gabriel.futurisss@gmail.com', password='sucodelaranja')
    #     self.projeto_obj = projeto.objects.create(user_id=self.user.UUID, titulo='Projeto renovado')
    #     response = self.client.get(reverse(f'perfil_publico/{str(self.projeto_obj.id_mongo)}'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'index/perfil_publico.html')

   

class ProjetoTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='gabriel.futurisss@gmail.com',
            nome='Gabriel Schranck',
            telefone='19983492015',
            data_nascimento='2003-06-02',
            cidade='Leme',
            estado='SP',
            password = 'sucodelaranja'
        )
        self.client.login(email='gabriel.futurisss@gmail.com', password='sucodelaranja')
        self.projeto_obj = projeto.objects.create(user_id=User.UUID, titulo = 'Super projeto')


    def test_editar_projeto_view(self):
        projeto_obj = projeto.objects.create(user_id=User.UUID, titulo='Projeto renovado')
        url = reverse('editar_projeto', args=[projeto_obj.id_mongo])
        data = {'titulo': 'Projeto renovado'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        projeto_obj.refresh_from_db()
        self.assertEqual(projeto_obj.titulo, 'Projeto renovado')

    def test_excluir_projeto(self):
        self.assertTrue(projeto.objects.filter(id_mongo=self.projeto_obj.id_mongo).first())
        url = reverse('excluir_projeto', args=[self.projeto_obj.id_mongo])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(projeto.objects.filter(id_mongo=self.projeto_obj.id_mongo).first(), None) 

    

        
