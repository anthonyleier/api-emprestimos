# Generated by Django 4.2 on 2023-04-29 20:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('onedata', '0005_alter_emprestimo_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]