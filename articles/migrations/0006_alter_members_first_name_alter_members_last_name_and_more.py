# Generated by Django 4.2.4 on 2024-06-08 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_members_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members',
            name='first_name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='members',
            name='last_name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='members',
            name='phone',
            field=models.TextField(),
        ),
    ]