# Create your models here.
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import date, datetime
import secrets


# Create your models here.


class Student(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, default = 1)
    logo            = models.FileField(null = True, upload_to='uploads/logos/')
    first_name      = models.CharField(null = True, default="", max_length=200)
    last_name      = models.CharField(null = True, default="", max_length=200)
    phone           = models.IntegerField(null = True, unique=False, default = "")
    lyrics_count    = models.IntegerField(null = True, unique=False)
    email           = models.EmailField(null = True, default="", max_length=200)
    details         = models.TextField(null = True, default="")
    date_joined     = models.DateTimeField(null = True, blank = True)
    access_token    = models.CharField(null = True, default="", max_length=200)
    
    

    def __str__(self):              # __unicode__ on Python 2
        return 'Students'

    class Meta:
        verbose_name_plural = "Global Settings"

    @staticmethod
    def create_new(username, firstname , lastname , email, password, phone, details = " "):

        new_user = User(first_name = firstname, last_name = lastname, email = email, username = username)
        new_user.save()
        new_user.set_password(password)

        new_student = Student(user = new_user, phone = phone, first_name = firstname, last_name = lastname, email = email, details = details)
        new_student.date_joined = datetime.now()
        new_student.save()
        print(new_student.date_joined)

        new_student.add_token()

        return new_student

    def create_lyrics(self, most_occuring_word , vowel_a, vowel_e, vowel_i, vowel_o, vowel_u, title  , artist , lyrics):

        new_lyrics = Lyric(student = self, most_occuring_word = most_occuring_word , vowel_a = vowel_a, vowel_e = vowel_e, vowel_i = vowel_i, vowel_o = vowel_o, vowel_u = vowel_u, title = title  , artist = artist , lyrics = lyrics) 

        new_lyrics.date_added = datetime.now()
        new_lyrics.save()

        return new_lyrics

    def get_lyrics_count(self):

        lyrics_count = self.lyric_set.all().count()

        return lyrics_count


    def add_token(self):

        token = Token_man().generate_token()
        self.access_token = token
        self.save()

    def verify_token(self, token):

        if self.access_token == token:
            return True
        else:
            return False


class Lyric(models.Model):

    student     = models.ForeignKey(Student, on_delete=models.CASCADE, default = 1)
    most_occuring_word  = models.CharField(null = True, default="", max_length=200)
    vowel_a     = models.IntegerField(null = True, unique=False, default = 0)
    vowel_e     = models.IntegerField(null = True, unique=False, default = 0)
    vowel_i     = models.IntegerField(null = True, unique=False, default = 0)
    vowel_o     = models.IntegerField(null = True, unique=False, default = "")
    vowel_u     = models.IntegerField(null = True, unique=False, default = "")
    date_added  = models.DateTimeField(null = True, blank = True)
    title       = models.CharField(null = True, default="", max_length=200)
    artist      = models.CharField(null = True, default="", max_length=200)
    lyrics      = models.TextField(null = True, default="")

    


#USER ACTUALLY REFERS TO USERACCOUNT MODEL OR OBJECT JUST USED USER FOR BETTER UNDERSTANDING 
class Token_man():

    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(40)




# class Global(models.Model):
#     logo            = models.FileField(null = True, upload_to='uploads/logos/')
#     phone           = models.IntegerField(null = True, unique=False, default = "")
#     location        = models.TextField(null = True, default="")
#     email           = models.EmailField(null = True, default="", max_length=200)
#     about_title     = models.CharField(null = True, default="", max_length=200)
#     about_text      = models.CharField(null = True, default="", max_length=200)
#     about_body      = models.TextField(null = True, default="", blank= True)
#     facebook        = models.CharField(null = True, default="", max_length=200)
#     twitter         = models.CharField(null = True, default="", max_length=200)
#     insta           = models.CharField(null = True, default="", max_length=200)

#     def __str__(self):              # __unicode__ on Python 2
#         return 'Global Settings'

#     class Meta:
#         verbose_name_plural = "Global Settings"

# class Carousel(models.Model):
#     image1          = models.FileField(null = True, upload_to='uploads/carousel_imgs/')
#     image2          = models.FileField(null = True, upload_to='uploads/carousel_imgs/')
#     image3          = models.FileField(null = True, upload_to='uploads/carousel_imgs/')
#     message1        = models.CharField(null = True, max_length=255, default = "")
#     message2        = models.CharField(null = True, max_length=255, default = "")
#     message3        = models.CharField(null = True, max_length=255, default = "")

#     def __str__(self):              # __unicode__ on Python 2
#         return 'Carousel Settings'

# class Category(models.Model):
#     image           = models.FileField(null = True, upload_to='uploads/course_imgs/')
#     title           = models.CharField(null = True, max_length=255, default = "")
#     description     = models.TextField(null = True,  default = "")

#     def __str__(self):              # __unicode__ on Python 2
#         return self.title
    
#     class Meta:
#         verbose_name_plural = "Categories"

# class Course(models.Model):
#     image           = models.FileField(null = True, upload_to='uploads/course_imgs/')
#     header          = models.FileField(null = True, upload_to='uploads/course_imgs/')
#     title           = models.CharField(null = True, max_length=40, default="")
#     category        = models.ForeignKey('Category', on_delete=models.CASCADE, default = 1, related_name= 'course')
#     about           = models.IntegerField(null = True, unique=False, default = "")
#     date            = models.DateField(null = True, default="")
#     time            = models.CharField(null = True, max_length=30, default="")
#     duration        = models.IntegerField(null = True, default="")
#     address         = models.TextField(null = True, default="")
#     about           = models.TextField(null = True, default="")
#     price           = models.IntegerField(null = True, default="")
#     is_upcoming     = models.BooleanField(default = False)
#     is_active       = models.BooleanField(default = False)

#     def __str__(self):              # __unicode__ on Python 2
#         return self.title

# class Requirement(models.Model):
#     course          = models.ForeignKey('Course', on_delete=models.CASCADE, default = 1, related_name = 'requirement')
#     text            = models.TextField(null = True, default="")

#     def __str__(self):              # __unicode__ on Python 2
#         return self.text

# class Take_away(models.Model):
#     course          = models.ForeignKey('Course', on_delete=models.CASCADE, default = 1, related_name= 'take_away')
#     text            = models.CharField(null = True, max_length=255, default="")

#     def __str__(self):              # __unicode__ on Python 2
#         return self.text

# class Center_section(models.Model):
#     title           = models.CharField( null = True, max_length=50, default = "")
#     description     = models.CharField( null = True, max_length=255, default = "")

#     def __str__(self):              # __unicode__ on Python 2
#         return self.description

# class Center_section_cards(models.Model):
#     center_section          = models.ForeignKey('Center_section', on_delete=models.CASCADE, default = 1, related_name='center_section_cards')
#     title           = models.CharField( null = True, max_length=255, default = "")
#     description     = models.TextField( null = True, default = "")

#     def __str__(self):              # __unicode__ on Python 2
#         return self.title

#     class Meta:
#         verbose_name_plural = "Center_section_cards"

# class Testimonials(models.Model):
#     image           = models.FileField(upload_to='uploads/testimonial_imgs/')
#     first_name      = models.CharField(null = True, max_length=255, default="")
#     last_name       = models.CharField(null = True, max_length=255, default="")
#     text            = models.TextField(null = True, default="")
#     starts_here     = models.BooleanField(default = True)
#     is_active       = models.BooleanField(default = True)

#     class Meta:
#         verbose_name_plural = "Testimonials"

#     def __str__(self):              # __unicode__ on Python 2
#         return '{}-{}'.format(self.first_name, self.last_name)


# class Application(models.Model):
#     full_name      = models.CharField(null = True, max_length=255, default="")
#     email          = models.EmailField(null = True, default="", max_length=200)
#     phone          = models.CharField(null = True, max_length=255, default="")
#     address        = models.TextField(null = True, default="")
#     coupon         = models.CharField(null = True, max_length=255, default="")
#     payment        = models.IntegerField(choices=PAYMENT_CHOICES, default=1) 
#     course         = models.ForeignKey('Course', on_delete=models.CASCADE, default = 1, related_name = 'application')

#     def __str__(self):              # __unicode__ on Python 2
#         return '{}'.format(self.full_name)











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
