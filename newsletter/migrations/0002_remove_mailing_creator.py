# Generated by Django 4.2.3 on 2023-09-18 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailing',
            name='creator',
        ),
    ]
