# Generated by Django 5.0.6 on 2024-06-02 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='measurement',
            old_name='measurements',
            new_name='bust',
        ),
    ]
