# Generated by Django 2.2.6 on 2019-11-12 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpage',
            name='email',
            field=models.EmailField(default='360383464@qq.com', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactpage',
            name='phone',
            field=models.CharField(default='15821062024', max_length=20),
            preserve_default=False,
        ),
    ]
