# Generated by Django 5.0.2 on 2024-02-13 20:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_alter_profile_preferred_style_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='created_by',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='song',
            name='last_modified_by',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='l_modified_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
