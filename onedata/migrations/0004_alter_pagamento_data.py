# Generated by Django 4.2 on 2023-04-28 20:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('onedata', '0003_alter_emprestimo_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
