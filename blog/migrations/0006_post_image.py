# Generated by Django 3.1.1 on 2020-09-16 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='users/%Y/%m/%d/'),
        ),
    ]