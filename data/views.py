from django.shortcuts import render
from django.db import models
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from itertools import chain #allow for merging multiple querysets frorm different models
from django.core import serializers
import math, datetime, pytz, json
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required, permission_required
from data.models import *
from snippet import helpers
from django.db.models import Count, F
from django.db.models.functions import Cast


host = 'http://localhost:8000/'

@csrf_exempt
def register(request):
    
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            exempted_fields = ["details",]
            cleaned_form = helpers.clean(data, exempted_fields)
            
            username    = cleaned_form['username']
            firstname   = cleaned_form['firstname']
            lastname    = cleaned_form['lastname']
            email       = cleaned_form['email']
            phone       = cleaned_form['phone']
            details     = cleaned_form['details']
            password    = cleaned_form['password']#

            # print(username, firstname , lastname , email, password, phone, details)

            new_user = Student.create_new(username, firstname , lastname , email, password, phone, details)

            response =  HttpResponse(json.dumps({"response":"success", "message": f"Successfully added user -->  {new_user.first_name}", "data": {"access_token":f" {new_user.access_token}"}}))
            response = CORS.allow_all(response, new_user.access_token)
            return response


        except:
            status     = "fail"
            message    = "unknown error occured, Either the username is already exists or the datetype is not correct. if using python requests make sure you used the json module to 'json.dumps()' the data"
            return HttpResponse(json.dumps({"response":status, "message": message}))

@csrf_exempt
def view_users(request):

    students = Student.objects.annotate(joined =( Cast('date_joined', models.CharField()))).annotate(Count('lyric')).values("id", "joined", username = F('user__username'), lyrics = F('lyric__count'))

    response =  HttpResponse(json.dumps({"response":"success", "message": {"data": list(students)}}))
    response = CORS.allow_all(response)
    return response
    
    

@csrf_exempt
def add_lyrics(request):

    if request.method == "POST":

        # try:
        data = json.loads(request.body)
        
        username   = data["details"]['username']
        access_token  = data["details"]['access_token']
        lyrics = data["data"]

        student = User.objects.get(username = username).student
        all_lyrics  = []
        
        if student.verify_token(access_token):

            for lyric in lyrics:
                most_occuring_word = lyric['most_occuring_word']
                vowel_a         = lyric['vowel_a']
                vowel_e         = lyric['vowel_e']
                vowel_i         = lyric['vowel_i']
                vowel_o         = lyric['vowel_o']
                vowel_u         = lyric['vowel_u']
                title           = lyric['title']
                artist          = lyric['artist']
                lyrics          = lyric['lyrics']                
                    
                new_lyrics = student.create_lyrics(most_occuring_word , vowel_a, vowel_e, vowel_i, vowel_o, vowel_u, title  , artist , lyrics)
                all_lyrics.append(title)

            response =  HttpResponse(json.dumps({"response":"success", "message": f"Successfully added lyrics data -->  {str(all_lyrics)} to account {student.user.username}"}))
            response = CORS.allow_all(response, student.access_token)
            return response
        else:

            response =  HttpResponse(json.dumps({"response":"Failed", "message": f"Failed adding lyrics data -->  {title} invalid access token"}))
            response = CORS.allow_all(response, student.access_token)
            return response

    else:
        response =  HttpResponse(json.dumps({"response":"failed", "message": f"Invalid request method (should be post.!!!)"}))
        response = CORS.allow_all(response, student.access_token)
        return response

@csrf_exempt
def view_lyrics(request):

    if request.method == "POST":

        # try:
        data = json.loads(request.body)
        
        username   = data["details"]['username']
        access_token  = data["details"]['access_token']

        student = User.objects.get(username = username).student
        all_lyrics  = []
        
        if student.verify_token(access_token):
            
            lyrics = student.lyric_set.all().values("id", "most_occuring_word" , "vowel_a", "vowel_e", "vowel_i", "vowel_o", "vowel_u", "title"  , "artist" , "lyrics")

            response =  HttpResponse(json.dumps({"response":"success", "message": {"data": list(lyrics)}}))
            response = CORS.allow_all(response, student.access_token)
            return response
        else:

            response =  HttpResponse(json.dumps({"response":"Failed", "message": f"Failed --> invalid access token"}))
            response = CORS.allow_all(response, student.access_token)
            return response

    else:
        response =  HttpResponse(json.dumps({"response":"failed", "message": f"Invalid request method (should be post.!!!)"}))
        response = CORS.allow_all(response, student.access_token)
        return response


@csrf_exempt
def delete_lyrics(request):

    if request.method == "POST":

        
        data = json.loads(request.body)
        
        username   = data["details"]['username']
        access_token  = data["details"]['access_token']
        id            = data["data"]['id']

        student = User.objects.get(username = username).student

        try:
            
            if student.verify_token(access_token):
                
                lyrics = student.lyric_set.get(id = id)
                lyrics.delete()

                response =  HttpResponse(json.dumps({"response":"success", "message": f"deleted {lyrics.title} - {lyrics.artist}"}))
                response = CORS.allow_all(response, student.access_token)
                return response

            else:

                response =  HttpResponse(json.dumps({"response":"Failed", "message": f"Failed --> invalid access token"}))
                response = CORS.allow_all(response, student.access_token)
                return response
        except:

            response =  HttpResponse(json.dumps({"response":"Failed", "message": f"Failed --> lyrics does not exist"}))
            response = CORS.allow_all(response, student.access_token)
            return response

    else:
        response =  HttpResponse(json.dumps({"response":"failed", "message": f"Invalid request method (should be post.!!!)"}))
        response = CORS.allow_all(response, student.access_token)
        return response



class CORS:

    @staticmethod
    def allow_all(response, access_token = ""):
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        response["Content-Type"] = "application/json"
        response["Access-Token"] = access_token

        return response














#General model is being sent for general data in render

# def index(request):
#     page = 'index'
#     carousel = Carousel.objects.all()[0]
#     general = Global.objects.all()[0]
#     footer_courses = Course.objects.filter(is_active = True)[:4] #COURSES TO SHOW AT FOOTER
#     testimonials = Testimonials.objects.all()
#     center_section = Center_section.objects.all()[0]
#     center_section_cards = Center_section_cards.objects.all().order_by('-id')[:3]
#     upcoming_courses = Course.objects.filter(is_upcoming = True, is_active = True).order_by('-id')

#     return render(request, 'index.html', { 'page': page, 'general':general, 'carousel':carousel, 'footer_courses':footer_courses, 'testimonials' : testimonials, 'center_section':center_section, 'center_section_cards':center_section_cards, 'upcoming_courses':upcoming_courses })


# def courses(request):
#     page = 'courses'
#     carousel = Carousel.objects.all()[0]
#     general = Global.objects.all()[0]
#     categories = Category.objects.all()
#     footer_courses = Course.objects.filter(is_active = True)[:4] #COURSES TO SHOW AT FOOTER

#     return render(request, 'courses.html', { 'page': page, 'general':general, 'carousel':carousel, 'categories':categories, 'footer_courses':footer_courses})


# def course_list(request,id):
#     page = 'course_list'
#     general = Global.objects.all()[0]
#     courses = Course.objects.filter(category_id = id, is_active = True)
#     footer_courses = Course.objects.filter(is_active = True) #COURSES TO SHOW AT FOOTER

#     return render(request, 'course_list.html', { 'page': page, 'general':general, 'courses':courses, 'footer_courses':footer_courses })


# def form(request, course_id):
#     page    = 'form'
#     general = Global.objects.all()[0]
#     footer_courses = Course.objects.all()[:4] #COURSES TO SHOW AT FOOTER
#     course      = Course.objects.get(pk = course_id)

#     return render(request, 'form.html', { 'page': page, 'general':general, 'footer_courses':footer_courses, 'course':course })


# def detailed_course_view(request, id):#ID ---> course__id
#     page        = 'detailed_course_view'
#     category    = Category.objects.get(course__id = id)
#     general     = Global.objects.all()[0]
#     course      = Course.objects.get(pk = id)
#     takeaways   = Take_away.objects.filter(course_id = course.id)
#     requirements = Requirement.objects.filter(course_id = course.id)
#     footer_courses = Course.objects.filter(is_active = True)[:4] #COURSES TO SHOW AT FOOTER

#     return render(request, 'detailed_course_view.html', { 'page': page, 'general':general, 'course':course, 'category':category, 'takeaways': takeaways, 'requirements':requirements, 'footer_courses':footer_courses })


# def about_us(request):
#     page = 'about_us'
#     general = Global.objects.all()[0]
#     footer_courses = Course.objects.filter(is_active = True) #COURSES TO SHOW AT FOOTER

#     return render(request, 'about_us.html', { 'page': page, 'general':general, 'footer_courses':footer_courses })


# def apply(request, course_id):
    
#     try:

#         exempted_fields = ["address", "full_name", "coupon"]
#         cleaned_form = helpers.clean(request.POST, exempted_fields)

#         full_name   = cleaned_form['full_name']
#         email       = cleaned_form['email']
#         address     = cleaned_form['address']
#         phone       = cleaned_form['phone']
#         coupon      = cleaned_form['coupon']
#         course_id   = cleaned_form['_course_id']
#         payment     = int(cleaned_form['choice']) #get choice and convert to integer
        
#         status     = "success"
#         message     = "added application successfully"

#         new_application = Application(full_name= full_name, email= email, address= address, phone= phone, coupon= coupon, payment= payment, course_id = course_id)

#         new_application.save()

#         return HttpResponse(json.dumps({"response":status, "message": message}))

#     except:
#         status     = "fail"
#         message    = "unknown error occured"
#         return HttpResponse(json.dumps({"response":status, "message": message}))


# def upcoming_courses(request):

#     upcoming_courses_query = Course.objects.filter(is_upcoming = True, is_active = True).order_by('-id')
#     courses = serializers.serialize("json", list(upcoming_courses_query) )

#     return HttpResponse(courses)






















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