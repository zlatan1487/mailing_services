# Generated by Django 4.2.3 on 2023-09-21 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0013_mailinglog_mailing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailtext',
            name='topic',
            field=models.CharField(max_length=100, unique=True, verbose_name='Тема рассылки'),
        ),
    ]