# Generated by Django 3.1 on 2021-01-08 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20210108_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
