from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from itertools import chain #allow for merging multiple querysets frorm different models
from django.core import serializers
import math, datetime, pytz, json
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required, permission_required
from snippet import helpers
from .choices import *
from main.models import Carousel, Global, Category, Course, Take_away, Testimonials, Requirement, Center_section, Center_section_cards

# from rest_framework import serializers
# Create your views here.

host = 'http://localhost:8000/'

#General model is being sent for general data in render

def index(request):
    page = 'index'
    carousel = Carousel.objects.all()[0]
    general = Global.objects.all()[0]
    footer_courses = Course.objects.all()[:4] #COURSES TO SHOW AT FOOTER
    testimonials = Testimonials.objects.all()
    center_section = Center_section.objects.all()[0]
    center_section_cards = Center_section_cards.objects.all()[:3]
    upcoming_courses = Course.objects.filter(is_upcoming = True)

    return render(request, 'index.html', { 'page': page, 'general':general, 'carousel':carousel, 'footer_courses':footer_courses, 'testimonials' : testimonials, 'center_section':center_section, 'center_section_cards':center_section_cards, 'upcoming_courses':upcoming_courses })


def courses(request):
    page = 'courses'
    carousel = Carousel.objects.all()[0]
    general = Global.objects.all()[0]
    categories = Category.objects.all()
    footer_courses = Course.objects.all()[:4] #COURSES TO SHOW AT FOOTER

    return render(request, 'courses.html', { 'page': page, 'general':general, 'carousel':carousel, 'categories':categories, 'footer_courses':footer_courses})


def course_list(request,id):
    page = 'course_list'
    general = Global.objects.all()[0]
    courses = Course.objects.filter(category_id = id)
    footer_courses = Course.objects.all()[:4] #COURSES TO SHOW AT FOOTER
    

    return render(request, 'course_list.html', { 'page': page, 'general':general, 'courses':courses, 'footer_courses':footer_courses })


def form(request, course_id):
    page    = 'form'
    general = Global.objects.all()[0]
    footer_courses = Course.objects.all()[:4] #COURSES TO SHOW AT FOOTER
    course      = Course.objects.get(pk = course_id)
    return render(request, 'form.html', { 'page': page, 'general':general, 'footer_courses':footer_courses, 'course':course })


def detailed_course_view(request, id):#ID ---> course__id
    page        = 'detailed_course_view'
    category    = Category.objects.get(course__id = id)
    general     = Global.objects.all()[0]
    course      = Course.objects.get(pk = id)
    takeaways   = Take_away.objects.filter(course_id = course.id)
    requirements = Requirement.objects.filter(course_id = course.id)
    footer_courses = Course.objects.all()[:4] #COURSES TO SHOW AT FOOTER

    return render(request, 'detailed_course_view.html', { 'page': page, 'general':general, 'course':course, 'category':category, 'takeaways': takeaways, 'requirements':requirements, 'footer_courses':footer_courses })


def about_us(request):
    page = 'about_us'
    general = Global.objects.all()[0]
    footer_courses = Course.objects.all()[:4] #COURSES TO SHOW AT FOOTER

    return render(request, 'about_us.html', { 'page': page, 'general':general, 'footer_courses':footer_courses })


def apply(request, course_id):
    print((request.POST))

    exempted_fields = ["address", "full_name", "coupon"]
    cleaned_form = helpers.clean(request.POST, exempted_fields)

    full_name   = cleaned_form['full_name']
    email       = cleaned_form['email']
    address     = cleaned_form['address']
    phone       = cleaned_form['phone']
    coupon      = cleaned_form['coupon']
    payment     = dict(PAYMENT_CHOICES)[cleaned_form['choice']]
    message     = "success"

    
    return HttpResponse(json.dumps({"response":message}))



























# from django.shortcuts import render
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from main.models import Herdsman, Bound, Location, Farmland
# import json
# from itertools import chain #allow for merging multiple querysets frorm different models
# from django.core import serializers
# import math
# import datetime
# from snippet import helpers
# from datetime import datetime, timezone
# import pytz
# from django.contrib.auth.decorators import login_required, permission_required


# # from rest_framework import serializers
# # Create your views here.

# host = 'http://localhost:8000/'

# @login_required
# def index(request):
#     locations = Location.objects.all().order_by('-id')[:10]
#     page = 'index'
#     return render(request, 'resolute/main/index.html', {'posts':locations, 'page': page})


# def detail_view(request):

#     herdsman = Herdsman.objects.all()

#     return render(request, 'resolute/skin-compact.html', {"herdsman":herdsman})

# @login_required
# def table(request):

#     locations = Location.objects.all().order_by('-date')
#     page = 'table'
#     return render(request, 'resolute/main/table.html', {'posts':locations, 'page': page})


# @csrf_exempt
# def locationpost(request):
# # Create your views here.
#     tz = pytz.timezone('Africa/Lagos')
#     lagos = datetime.now(tz)
#     formatedDate = lagos.strftime("%Y-%m-%d %H:%M:%S")

#     # print(request.body)
#     if request.method == 'POST':    

#         reqPOST = (json.loads(request.body))
#         cleaned_json_post = dict(reqPOST['resource'][0])

#         devid = cleaned_json_post["devid"] 
#         time  = cleaned_json_post["time"]
#         etype = cleaned_json_post["etype"]
#         engine = cleaned_json_post["engine"]
#         lat = cleaned_json_post["lat"]
#         lng = cleaned_json_post["lon"]
#         vbat = cleaned_json_post["vbat"]
#         speed = cleaned_json_post["speed"][0:5]
#         pint = cleaned_json_post["pInt"]
#         try:        
#             if lat != '0' and lng != '0' :
#                 clean_address = helpers.get_address(lat,lng)
#                 address = clean_address['address']
#                 state = clean_address['state']
#                 herdsman = Herdsman.objects.get(userid = devid)
#                 herdsman.lng = lng
#                 herdsman.lat = lat
#                 herdsman.state = state
#                 print(state)
#                 herdsman.address = address
#                 herdsman.save()
#                 new_location = Location(state = state, herdsman = herdsman, lat = lat, lng = lng, speed = speed, address = address, date = formatedDate)
#                 new_location.save()
#                 print(devid,time, etype, engine, lat, lng, vbat, speed)

#         except:
#             return HttpResponse(json.dumps('No user with id {} found in data base please confirm'.format(devid)))   
    

#     locations = Location.objects.all() # for iteration
#     # result = serializers.serialize("json", locations )


#     return HttpResponse(json.dumps({'Success' : 'success'}))
    
# # @csrf_exempt
# # def end(request):

    
# #     if request.method == 'GET':
# #         post = (request.GET)
# #         target = Customer.objects.get(id = post["device"])
# #         target.lng = post['ln']
# #         target.lat = post['lt']
# #         target.address  = helpers.get_address(post['lt'],post['ln'])
# #         target.is_panicking = True
# #         target.panicked = datetime.datetime.now()
# #         target.save()

# #         new_location = Location.objects.create(lat = target.lat, lng = target.lng, address = target.address, customer_id = target.id,
# #                                                 speed = post['sog'], accuracy = post['hdop'])

# #         return HttpResponse(json.dumps({'success':'success', "panic_status":target.is_panicking}))

        
# #     return HttpResponse('Unrecognisable request method, cannot understand')


# def check(request, slug):

#     herdsman = Herdsman.objects.get(slug = slug) #for filtering get just one customer 
#     herdsmen = Herdsman.objects.filter(slug = slug) # for iteration
#     locations = serializers.serialize("json", list(chain(Location.objects.filter(herdsman_id = herdsman.id)[:40], herdsmen)) )



#     return HttpResponse(locations)


# @login_required
# def track(request, slug):

#     return render(request, 'resolute/realtracking.html', {"slug":slug})

# @login_required
# def mapping(request, slug):

#     herdsman = Herdsman.objects.get(slug = slug) #for filtering get just one customer 
#     page = 'map'
    
#     return render(request, 'resolute/main/map.html', {"herdsman":herdsman, 'slug':slug,  'page': page})

# @login_required
# def trail(request, slug):

#     return render(request, 'resolute/trail.html', {"slug":slug})

# def check_distance(old_coord, new_coord):

#     a =  old_coord[0] - new_coord[0] #lat difference as opposite
#     b =  old_coord[1] - new_coord[1] #lng difference as adjacent
#     c = a **2 + b **2 #hypothenus as distance between two points

#     c = math.sqrt(c)
#     print(c)
#     # 0.0009 = "100m"
#     # 0.009 = "1km"
#     if c >= 0.00001:
#         return True
    
#     else:
#         return False