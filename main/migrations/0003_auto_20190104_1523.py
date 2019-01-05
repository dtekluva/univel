# Generated by Django 2.0 on 2019-01-04 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_course_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='center_section_cards',
            options={'verbose_name_plural': 'Center_section_cards'},
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.FileField(upload_to='uploads/course_imgs'),
        ),
        migrations.AlterField(
            model_name='testimonials',
            name='image',
            field=models.FileField(upload_to='uploads/testimonial_imgs'),
        ),
    ]
