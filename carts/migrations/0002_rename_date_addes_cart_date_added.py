# Generated by Django 5.0.6 on 2024-06-15 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='date_addes',
            new_name='date_added',
        ),
    ]
