# Generated by Django 5.0.2 on 2024-02-13 20:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0014_alter_profile_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='profile',
            constraint=models.UniqueConstraint(fields=('user',), name='unique_user_profile'),
        ),
    ]
