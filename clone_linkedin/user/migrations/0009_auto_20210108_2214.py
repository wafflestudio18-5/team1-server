# Generated by Django 3.1 on 2021-01-08 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_merge_20210108_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, upload_to='%Y/%m/%d'),
        ),
    ]