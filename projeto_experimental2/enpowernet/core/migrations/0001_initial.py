# Generated by Django 4.1.13 on 2024-10-23 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='usuario',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('senha', models.CharField(max_length=255)),
                ('genero', models.CharField(choices=[('F', 'Feminino'), ('M', 'Masculino'), ('I', 'Indefinido')], max_length=1)),
                ('telefone', models.CharField(max_length=12)),
                ('data_nascimento', models.DateField(default=None, max_length=8)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
