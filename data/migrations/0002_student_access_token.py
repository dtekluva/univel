# Generated by Django 2.0 on 2019-12-23 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='access_token',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
