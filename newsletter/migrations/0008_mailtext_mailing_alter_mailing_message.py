# Generated by Django 4.2.3 on 2023-09-19 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0007_mailinglog_mailing'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailtext',
            name='mailing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='mailtexts', to='newsletter.mailing', verbose_name='Рассылка'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mailing',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mailing_messages', to='newsletter.mailtext', verbose_name='Сообщение'),
        ),
    ]