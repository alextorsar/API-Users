# Generated by Django 3.2 on 2024-04-15 16:35

import Users.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0008_alter_submodels_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='models',
            name='file',
            field=models.FileField(upload_to=Users.models.generate_files_dirname, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xmile'])]),
        ),
        migrations.AlterField(
            model_name='submodels',
            name='file',
            field=models.FileField(upload_to=Users.models.get_parent_model_dirname, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xmile'])]),
        ),
    ]
