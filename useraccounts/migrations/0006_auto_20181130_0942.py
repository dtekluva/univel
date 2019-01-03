# Generated by Django 2.0 on 2018-11-30 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useraccounts', '0005_useraccount_has_special_fee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funds',
            name='trader',
        ),
        migrations.DeleteModel(
            name='Global_var',
        ),
        migrations.RemoveField(
            model_name='trader',
            name='cell_leader',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='target_month',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='user',
        ),
        migrations.DeleteModel(
            name='Funds',
        ),
        migrations.DeleteModel(
            name='Months',
        ),
        migrations.DeleteModel(
            name='Trader',
        ),
        migrations.DeleteModel(
            name='Transactions',
        ),
    ]