# Generated by Django 4.2.3 on 2023-09-21 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0015_customer_mailing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='mailing',
        ),
        migrations.CreateModel(
            name='MailingCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsletter.customer', verbose_name='Клиент')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsletter.mailing', verbose_name='Рассылка')),
            ],
        ),
    ]
