# Generated by Django 4.1.2 on 2022-11-05 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0010_delete_veiculo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Veiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proprietario', models.CharField(max_length=50)),
                ('foto_carro', models.ImageField(upload_to='main/carros/%Y/%m/%d/')),
                ('modelo', models.CharField(max_length=50, verbose_name='Modelo do Veículo')),
                ('pais', models.CharField(max_length=50)),
                ('placa', models.CharField(max_length=7, unique=True)),
                ('num_chassi', models.CharField(max_length=17, unique=True, verbose_name='Número do Chassi')),
                ('utima_localizacao', models.CharField(max_length=20, null=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.empresa')),
            ],
        ),
    ]