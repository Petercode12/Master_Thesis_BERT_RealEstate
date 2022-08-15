from ast import Not, Str
from django.shortcuts import render
import django
from django.contrib.auth.decorators import login_required
from django import template
from django.http import HttpResponse, JsonResponse
from django.template import loader
from jobsfb.models import (
    Facebook_Post_Job_Scraper,
    Facebook_User_Profile_Job_Scraper
)
from django_serverside_datatable.views import ServerSideDatatableView
from django.conf import settings
from django.db import connection, reset_queries
from facebook_scraper import get_profile, get_posts
import os
import subprocess
import sys
import time
from django.contrib.postgres.aggregates import StringAgg
from django.db.models import Count
from django.shortcuts import render
from django_serverside_datatable import datatable
from django.db.models.functions import RowNumber
from django.db.models import F, Func, CharField, DateField, Max
from django.db.models.expressions import Window
from configuration.config import Config
import json
from jobsfb import resource
cfg = Config("configuration/config.json")

# Viec Lam From FB
@login_required(login_url="/login/")
def vieclamfb_scraper(request):
    context = {}
    context["segment"] = "vieclamfb-scraper"

    html_template = loader.get_template("vieclamfb-scraper.html")
    return HttpResponse(html_template.render(context, request))

class FacebookUserProfileListJobListView(ServerSideDatatableView):
    queryset = Facebook_User_Profile_Job_Scraper.objects.all().order_by('id')
    columns = [
        "id",
        "user_id_job",
        "user_name_job",
        "post_id",
        "group_id",
        "name",
        "work",
        "education",
        "friend_count",
        "follower_count",
        "following_count",
        "cover_photo",
        "profile_picture",
    ]


class FacebookPostItemJobListView(ServerSideDatatableView):
    queryset = Facebook_Post_Job_Scraper.objects.all().order_by('id')
    columns = [
        "id",
        "group_id",
        "post_id",
        "post_user_id",
        "post_message",
        "post_image_link",
        "post_image_alt",
        "post_total_reactions",
        "post_total_comments",
        "post_total_shares",
        "timestamp",
        "created_at",
        "updated_at",
    ]

@login_required(login_url="/login/")
def facebook_post_job_get_data(request):
    if request.method == "POST":
        # hard code
        pages = int(3)
        group_lists = load_groups()
        for test_group in group_lists: 
            test_group_id = list(filter(None, test_group.split('/')))[-1]
            if test_group_id is not None:
                path = str(settings.CORE_DIR) + "/facebook_splash_scraper/" + cfg.get_facebook_cookie_prefix() + str(request.user.id) + ".json"
                for post in get_posts(
                    group=test_group_id, 
                    cookies=load_cookies(path, str(request.user.id)),
                    pages = pages,
                    options={"allow_extra_requests": False}):
                        Facebook_Post_Job_Scraper.objects.create(
                            post_message = post['text'],
                            post_image_link = post['image'],
                            post_total_reactions = post['likes'],
                            post_total_comments = post['comments'],
                            post_total_shares = post['shares'],
                            group_id = test_group_id,
                            post_id =  post['post_id'],
                            post_user_id = post['user_id'],
                            timestamp  = post['time'].timestamp()
                            )
                        queryset = Facebook_User_Profile_Job_Scraper.objects.filter(user_id_job=post['user_id']).all()
                        data = list(queryset.values())
                        if len(data) == 0:
                            try:
                                facebook_user_profile_get_data(post['user_id'], post['post_id'], test_group_id,  str(request.user.id))
                            except:
                                pass
                        
                time.sleep(20)
        return JsonResponse({"success": True})

def facebook_user_profile_get_data(user_id, post_id, group_id,cookieId):
    if user_id == '':
        return
    path = str(settings.CORE_DIR) + "/facebook_splash_scraper/" + cfg.get_facebook_cookie_prefix() + str(cookieId) + ".json"
    profile = get_profile(
            user_id,
            cookies=load_cookies(path, cookieId))
    work = ""
    education = ""
    cover_photo = ""
    profile_picture = ""
    friend_count = 0
    follower_count = 0
    following_count = 0
    if "Work" in profile:
        work = profile["Work"]
    if "Education" in profile:
        education = profile["Education"]
    if "cover_photo" in profile:
        cover_photo = profile["cover_photo"]
    if "profile_picture" in profile:
        profile_picture = profile["profile_picture"]
    if "friend_count" in profile:
        result = profile["friend_count"]
        if result is not None:
            friend_count = int(result)
    if "Follower_count" in profile:
        result = profile["Follower_count"]
        if result is not None:
            friend_count = int(result)
    if "Following_count" in profile:
        result = profile["Following_count"]
        if result is not None:
            following_count = int(result)
    Facebook_User_Profile_Job_Scraper.objects.create(
            post_id = post_id,
            group_id = group_id,
            user_id_job=profile["id"],
            user_name_job= profile["Name"],
            name=profile["Name"],
            work=work,
            education=education,
            friend_count=friend_count,
            follower_count=follower_count,
            following_count=following_count,
            cover_photo=cover_photo,
            profile_picture=profile_picture,
        )
    time.sleep(10)

@login_required(login_url="/login/")
def facebook_post_job_delete_data(request):
    if request.method == "POST":
        id_array = request.POST["id_array"].split(",")
        Facebook_Post_Job_Scraper.objects.filter(id__in=id_array).delete()
        return JsonResponse({"success": True})

@login_required(login_url="/login/")
def facebook_user_profile_job_delete_data(request):
    if request.method == "POST":
        id_array = request.POST["id_array"].split(",")
        Facebook_User_Profile_Job_Scraper.objects.filter(id__in=id_array).delete()
        return JsonResponse({"success": True})

@login_required(login_url="/login/")
def vieclamfb_user_profile_scraper(request):
    context = {}
    context["segment"] = "vieclamfb-user-profile-scraper"

    html_template = loader.get_template("vieclamfb-user-profile-scraper.html")
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def facebook_user_profile_job_auto_data(request):
    if request.method == "POST":
        queryset = Facebook_User_Profile_Job_Scraper.objects.order_by("-updated_at").all()
        data = list(queryset.values())
        return JsonResponse({"data": data})

@login_required(login_url="/login/")
def facebook_post_job_auto_data(request):
    if request.method == "POST":
        queryset = Facebook_Post_Job_Scraper.objects.filter(
            timestamp__gte=request.POST["timestamp"]
        ).all()
        data = list(queryset.values())
        return JsonResponse({"data": data})

@login_required(login_url="/login/")
def facebook_user_profile_job_get_data(request):
    if request.method == "POST":
        queryset = Facebook_Post_Job_Scraper.objects.all()
        data = list(queryset.values())
        firstData = data[:30]
        for item in firstData:
            user_id = item["post_user_id"]
            post_id = item["post_id"]
            group_id = item["group_id"]
            userQuerySet = Facebook_User_Profile_Job_Scraper.objects.filter(user_id_job=user_id).all()
            newData = list(userQuerySet.values())
            if len(newData) == 0:
                try:
                    facebook_user_profile_get_data(user_id, post_id, group_id,  str(request.user.id))
                except:
                    pass
        return JsonResponse({"success": True})
    
def load_groups():
    # Opening JSON file
    path = str(settings.CORE_DIR) + '/jobsfb/resource/groups.json'
    f = open(path)
    groups = []
    data = json.load(f)
    for item in data["groups"]:
        if len(item) > 0:
            groups.append(item)
    f.close
    return groups

def load_cookies(path, cookieId):
    f = open(path)
    data = json.load(f)
    new_path = str(settings.CORE_DIR) + "/facebook_splash_scraper/" + cfg.get_facebook_cookie_prefix() + str(cookieId) + "_job.json"
    cookies = data["cookies"]
    with open(new_path, 'w') as f:
        json.dump(cookies, f)
        return new_path

# Employment-counseling
@login_required(login_url="/login/")
def vieclamfb_employment_counseling(request):
    context = {}
    context["segment"] = "vieclamfb_employment_counseling"

    html_template = loader.get_template("employment-counseling.html")
    return HttpResponse(html_template.render(context, request))
                      