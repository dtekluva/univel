from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import date, datetime

# Create your models here.
class Global(models.Model):
    logo            = models.FileField(null = True, upload_to='uploads/logos/')
    phone           = models.IntegerField(null = True, unique=False, default = "")
    location        = models.TextField(null = True, default="")
    email           = models.EmailField(null = True, default="", max_length=200)
    about_title     = models.CharField(null = True, default="", max_length=200)
    about_text      = models.CharField(null = True, default="", max_length=200)
    about_body      = models.TextField(null = True, default="", blank= True)
    facebook        = models.CharField(null = True, default="", max_length=200)
    twitter         = models.CharField(null = True, default="", max_length=200)
    insta           = models.CharField(null = True, default="", max_length=200)

    def __str__(self):              # __unicode__ on Python 2
        return 'Global Settings'

class Carousel(models.Model):
    image1          = models.FileField(null = True, upload_to='uploads/carousel_imgs/')
    image2          = models.FileField(null = True, upload_to='uploads/carousel_imgs/')
    image3          = models.FileField(null = True, upload_to='uploads/carousel_imgs/')
    message1        = models.CharField(null = True, max_length=255, default = "")
    message2        = models.CharField(null = True, max_length=255, default = "")
    message3        = models.CharField(null = True, max_length=255, default = "")

    def __str__(self):              # __unicode__ on Python 2
        return 'Carousel Settings'

class Category(models.Model):
    image           = models.FileField(null = True, upload_to='uploads/course_imgs/')
    title           = models.CharField(null = True, max_length=255, default = "")
    description     = models.TextField(null = True,  default = "")

    def __str__(self):              # __unicode__ on Python 2
        return self.title
    
    class Meta:
        verbose_name_plural = "Categories"

class Course(models.Model):
    image  = models.FileField(null = True, upload_to='uploads/course_imgs/')
    header = models.FileField(null = True, upload_to='uploads/course_imgs/')
    title           = models.CharField(null = True, max_length=40, default="")
    category        = models.ForeignKey('Category', on_delete=models.CASCADE, default = 1, related_name= 'course')
    about           = models.IntegerField(null = True, unique=False, default = "")
    date            = models.DateField(null = True, default="")
    time            = models.CharField(null = True, max_length=30, default="")
    duration        = models.IntegerField(null = True, default="")
    address         = models.TextField(null = True, default="")
    about           = models.TextField(null = True, default="")
    price           = models.IntegerField(null = True, default="")
    is_upcoming     = models.BooleanField(default = False)
    is_active       = models.BooleanField(default = False)

    def __str__(self):              # __unicode__ on Python 2
        return self.title

class Requirement(models.Model):
    course          = models.ForeignKey('Course', on_delete=models.CASCADE, default = 1, related_name = 'requirement')
    text            = models.TextField(null = True, default="")

    def __str__(self):              # __unicode__ on Python 2
        return self.text

class Take_away(models.Model):
    course          = models.ForeignKey('Course', on_delete=models.CASCADE, default = 1, related_name= 'take_away')
    text            = models.CharField(null = True, max_length=255, default="")

    def __str__(self):              # __unicode__ on Python 2
        return self.text

class Center_section(models.Model):
    title           = models.CharField( null = True, max_length=50, default = "")
    description     = models.CharField( null = True, max_length=255, default = "")

    def __str__(self):              # __unicode__ on Python 2
        return self.description

class Center_section_cards(models.Model):
    center_section          = models.ForeignKey('Center_section', on_delete=models.CASCADE, default = 1, related_name='center_section_cards')
    title           = models.CharField( null = True, max_length=255, default = "")
    description     = models.TextField( null = True, default = "")

    def __str__(self):              # __unicode__ on Python 2
        return self.title

    class Meta:
        verbose_name_plural = "Center_section_cards"

class Testimonials(models.Model):
    image           = models.FileField(upload_to='uploads/testimonial_imgs/')
    first_name      = models.CharField(null = True, max_length=255, default="")
    last_name       = models.CharField(null = True, max_length=255, default="")
    text            = models.TextField(null = True, default="")
    starts_here     = models.BooleanField(default = True)
    is_active       = models.BooleanField(default = True)

    def __str__(self):              # __unicode__ on Python 2
        return '{}-{}'.format(self.first_name, self.last_name)














    # name            = models.CharField(max_length=40,unique=False)
    # surname         = models.CharField(max_length=40,unique=False)
    # userid          = models.IntegerField(default=0)
    # lng             = models.FloatField(max_length=100,blank=True, default=0)
    # lat             = models.FloatField(max_length=100,blank=True, default=0)
    # slug            = models.SlugField(blank=True,unique=True)
    # state           = models.TextField(default=0)
    # last_post       = models.DateField(auto_now_add=True, blank=True)
    # date            = models.DateField(auto_now_add=True)
    # db_id           = models.CharField(max_length=40, unique=True, null = True, blank=True)
    # no_of_cattle    = models.IntegerField(unique=False, default = "0")
    # details         = models.TextField(max_length=200, default="", null = True, blank=True)
    # is_trespassing  = models.BooleanField(se, )
    # is_panicking    = models.BooleanField(se)


    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Herdsman, self).save(*args, **kwargs)
    #     self.db_id = 'hd{:03d}'.format(self.id)
    #     super(Herdsman, self).save(*args, **kwargs)

    # def __str__(self):              # __unicode__ on Python 2
    #     return self.slug

    # class Meta:
    #     ordering = ('slug',)
    #     verbose_name_plural = "Herdsmen"
