# Generated by Django 4.1.2 on 2022-11-12 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veiculos', '0006_alter_veiculohistorico_horario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='veiculohistorico',
            name='horario',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]