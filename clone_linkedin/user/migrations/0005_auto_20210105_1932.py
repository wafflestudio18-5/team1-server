# Generated by Django 3.1 on 2021-01-05 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_userprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(upload_to='%Y/%m/%d'),
        ),
    ]
