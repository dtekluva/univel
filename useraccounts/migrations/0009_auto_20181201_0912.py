# Generated by Django 2.0 on 2018-12-01 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useraccounts', '0008_auto_20181201_0904'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccount',
            old_name='occupation',
            new_name='agency',
        ),
    ]
