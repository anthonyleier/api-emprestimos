# Generated by Django 4.2 on 2023-04-28 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('onidata', '0002_pagamento_usuario_alter_emprestimo_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprestimo',
            name='usuario',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
