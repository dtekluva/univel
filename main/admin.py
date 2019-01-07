from django.contrib import admin

# Register your models here.
from main.models import Course, Carousel, Category, Center_section_cards, Center_section, Global, Requirement, Testimonials, Take_away, Application
# Register your models here.

class GlobalAdmin(admin.ModelAdmin):
    list_display = ('email',)

class CarouselAdmin(admin.ModelAdmin):
    list_display = ('id',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','description',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title','category','date')

class RequirementAdmin(admin.ModelAdmin):
    list_display = ('course','text',)

class Take_awayAdmin(admin.ModelAdmin):
    list_display = ('course','text',)

class Center_sectionAdmin(admin.ModelAdmin):
    list_display = ('id','title',)

class Center_section_cardsAdmin(admin.ModelAdmin):
    list_display = ('id','title',)

class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name', 'text',)

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name','payment','course')



admin.site.register(Global, GlobalAdmin)
admin.site.register(Carousel, CarouselAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Requirement, RequirementAdmin)
admin.site.register(Take_away, Take_awayAdmin)
admin.site.register(Center_section, Center_sectionAdmin)
admin.site.register(Center_section_cards, Center_section_cardsAdmin)
admin.site.register(Testimonials, TestimonialsAdmin)
admin.site.register(Application, ApplicationAdmin)
