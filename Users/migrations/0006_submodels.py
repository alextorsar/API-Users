# Generated by Django 3.2 on 2023-12-23 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_alter_models_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubModels',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.models')),
            ],
        ),
    ]
