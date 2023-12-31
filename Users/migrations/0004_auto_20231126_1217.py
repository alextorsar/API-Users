# Generated by Django 3.2 on 2023-11-26 12:17

import Users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='models',
            name='file',
            field=models.FileField(upload_to=Users.models.generate_files_dirname),
        ),
        migrations.AlterField(
            model_name='models',
            name='image',
            field=models.ImageField(upload_to=Users.models.generate_image_dirname),
        ),
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterUniqueTogether(
            name='models',
            unique_together={('id_user', 'name')},
        ),
    ]
