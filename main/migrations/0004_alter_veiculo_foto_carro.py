# Generated by Django 4.1.2 on 2022-11-02 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_estado_veiculo_pais_veiculo_foto_carro_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='veiculo',
            name='foto_carro',
            field=models.ImageField(upload_to='main/carros/%Y/%m/%d/'),
        ),
    ]