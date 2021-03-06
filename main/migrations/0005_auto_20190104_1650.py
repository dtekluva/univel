# Generated by Django 2.0 on 2019-01-04 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190104_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.FileField(null=True, upload_to='uploads/course_imgs/'),
        ),
        migrations.AlterField(
            model_name='carousel',
            name='image1',
            field=models.FileField(upload_to='uploads/carousel_imgs/'),
        ),
        migrations.AlterField(
            model_name='carousel',
            name='image2',
            field=models.FileField(upload_to='uploads/carousel_imgs/'),
        ),
        migrations.AlterField(
            model_name='carousel',
            name='image3',
            field=models.FileField(upload_to='uploads/carousel_imgs/'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.FileField(upload_to='uploads/course_imgs/'),
        ),
        migrations.AlterField(
            model_name='global',
            name='logo',
            field=models.FileField(upload_to='uploads/logos/'),
        ),
        migrations.AlterField(
            model_name='testimonials',
            name='image',
            field=models.FileField(upload_to='uploads/testimonial_imgs/'),
        ),
    ]
