# Generated by Django 2.2.19 on 2023-02-19 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20230203_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]