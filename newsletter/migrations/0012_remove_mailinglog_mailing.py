# Generated by Django 4.2.3 on 2023-09-19 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0011_mailinglog_mailing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailinglog',
            name='mailing',
        ),
    ]
