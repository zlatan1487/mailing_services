# Generated by Django 4.2.3 on 2023-09-19 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newsletter', '0005_remove_mailing_creator_alter_customer_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='mailings', to=settings.AUTH_USER_MODEL, verbose_name='Создатель'),
            preserve_default=False,
        ),
    ]
