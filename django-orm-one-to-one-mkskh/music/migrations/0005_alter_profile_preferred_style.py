# Generated by Django 5.0.2 on 2024-02-13 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='preferred_style',
            field=models.CharField(choices=[('Indie', 'Indie'), ('Pop', 'Pop'), ('Rock', 'Rock'), ('Funky', 'Funky'), ('Reggaeton', 'Reggaeton'), ('Classic', 'Classic'), ('Orquestra', 'Orquestra'), ('Folk', 'Folk')], max_length=20),
        ),
    ]
