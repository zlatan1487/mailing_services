# Generated by Django 4.2.3 on 2023-09-21 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0016_remove_customer_mailing_mailingcustomer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='Почта'),
        ),
        migrations.DeleteModel(
            name='MailingCustomer',
        ),
    ]
