# Generated by Django 4.2.3 on 2023-09-19 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0012_remove_mailinglog_mailing'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailinglog',
            name='mailing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='mailing_logs', to='newsletter.mailing'),
            preserve_default=False,
        ),
    ]
