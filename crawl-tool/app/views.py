# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from asyncio.subprocess import PIPE
from traceback import print_stack
import django
import traceback
import os.path
from app.models import (
    Vieclamtot_Scraper,
    Google_Scraper,
    Facebook_Search_Scraper,
    Facebook_Post_Scraper,
    Facebook_User_Scraper,
    Facebook_Comment_Scraper,
    Facebook_User_Profile_Scraper,
    Vieclamtot_Statistic,
    AnCu_Scraper,
    NhaDat24h_Scraper,
    DangBanNhaDat_Scraper,
    MuaBanNet_Scraper,
    Facebook_User_From_Group_Scraper
)
from django_serverside_datatable.views import ServerSideDatatableView
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
from django.conf import settings
from django.db import connection, reset_queries
from facebook_scraper import get_profile, get_posts
import os
import subprocess
import sys
import time
import json
from django.contrib.postgres.aggregates import StringAgg
from django.db.models import Count
from django.shortcuts import render
from django_serverside_datatable import datatable
from django.db.models.functions import RowNumber
from django.db.models import F, Func, CharField, DateField, Max
from django.db.models.expressions import Window
# setting path
sys.path.append("..")

from configuration.config import Config

cfg = Config("configuration/config.json")

# Constant Variables

environment_command = "source " + str(settings.CORE_DIR) + str(settings.VIRTUAL_ENV_DIR)

# Documentation


@login_required(login_url="/login/")
def doc_start(request):

    context = {}
    # context['segment'] = 'index'
    context["segment"] = "doc-start"

    # html_template = loader.get_template( 'index.html' )
    # html_template = loader.get_template( 'dashboard.html' )

    html_template = loader.get_template("doc-start.html")
    return HttpResponse(html_template.render(context, request))


# Google Scraper


@login_required(login_url="/login/")
def index(request):

    context = {}
    # context['segment'] = 'index'
    context["segment"] = "google-scraper"

    # html_template = loader.get_template( 'index.html' )
    # html_template = loader.get_template( 'dashboard.html' )

    html_template = loader.get_template("google-scraper.html")
    return HttpResponse(html_template.render(context, request))


class GoogleItemListView(ServerSideDatatableView):
    queryset = Google_Scraper.objects.order_by("-timestamp").all()
    columns = ["id", "keyword", "title", "link", "datetime", "timestamp"]


@login_required(login_url="/login/")
def google_get_data(request):
    if request.method == "POST":
        command = (
            # environment_command
            # + " && "
            "cd "
            + str(settings.CORE_DIR)
            + "/google_scraper"
            + " && "
        )

        command += (
            'scrapy crawl google -a search_keyword="'
            + request.POST["search_keyword"]
            + '" -a end_page='
            + request.POST["end_page"]
        )
        subprocess.Popen(command, shell=True, executable="/bin/bash")
        # subprocess.Popen(command, shell=True)
        return JsonResponse({"success": True})


@login_required(login_url="/login/")
def google_auto_data(request):
    if request.method == "POST":
        queryset = Google_Scraper.objects.filter(
            timestamp__gte=request.POST["timestamp"]
        ).all()
        data = list(queryset.values())
        return JsonResponse({"data": data})


@login_required(login_url="/login/")
def google_delete_data(request):
    if request.method == "POST":
        id_array = request.POST["id_array"].split(",")
        Google_Scraper.objects.filter(id__in=id_array).delete()
        return JsonResponse({"success": True})




@login_required(login_url="/login/")
def bd_real_estate_index(request):

    context = {}
    # context['segment'] = 'index'
    context["segment"] = "binh-duong-real-estate-scraper"

    # html_template = loader.get_template( 'index.html' )
    # html_template = loader.get_template( 'dashboard.html' )

    html_template = loader.get_template("binh_duong_real_estate.html")
    return HttpResponse(html_template.render(context, request))

# An Cu Scraper

class AnCuItemListView(ServerSideDatatableView):
    queryset = AnCu_Scraper.objects.annotate(formatted_date=Func(
            F('post_time') + 25200, #timezone
            function='to_timestamp',
            output_field=CharField()
        )).order_by("post_time").all()
    columns = [
        "id",
        "updated_at",
        "formatted_date",
        "post_title",
        "type",
        "description",
        "area",
        "price_with_unit",
        "address",
        "coordinate",
        "url",
        "post_author",   
        "phone_number"
    ]


@login_required(login_url="/login/")
def ancu_get_data(request):
    if request.method == "POST":
        command = (
            # environment_command
            # + " && "
            "cd "
            + str(settings.CORE_DIR)
            + "/ancu_scraper"
            + " && "
        )

        command += (
            'scrapy crawl ancu -a end_page="'
            + request.POST["end_page"]
            + '" -a auto="False"'
        )
        process = subprocess.Popen(command, shell=True, executable="/bin/bash")
        #subprocess.Popen(command, shell=True)
        process.wait()
        return JsonResponse({"success": True})


@login_required(login_url="/login/")
def ancu_auto_data(request):
    if request.method == "POST":
        queryset = AnCu_Scraper.objects.filter(
            timestamp__gte=request.POST["timestamp"]
        ).all()
        data = list(queryset.values())
        return JsonResponse({"data": data})


@login_required(login_url="/login/")
def ancu_delete_data(request):
    if request.method == "POST":
        id_array = request.POST["id_array"].split(",")
        AnCu_Scraper.objects.filter(id__in=id_array).delete()
        return JsonResponse({"success": True})

# Mua Ban Scraper

class MuaBanItemListView(ServerSideDatatableView):
    queryset = MuaBanNet_Scraper.objects.annotate(formatted_date=Func(
            F('post_time') + 25200, #timezone
            function='to_timestamp',
            output_field=CharField()
        )).order_by("post_time").all()
    columns = [
        "id",
        "updated_at",
        "formatted_date",
        "post_title",
        "type",
        "description",
        "land_area",
        "bedroom",
        "bathroom",
        "floors",
        "legal",
        "price_with_unit",
        "address",
        "location",
        "url",
        "post_author",   
        "phone_number"
    ]


@login_required(login_url="/login/")
def muaban_get_data(request):
    if request.method == "POST":
        command = (
            # environment_command
            # + " && "
            "cd "
            + str(settings.CORE_DIR)
            + "/muaban_scraper"
            + " && "
        )

        command += (
            'scrapy crawl muaban -a end_page="'
            + request.POST["end_page"]
            + '" -a auto="False"'
        )
        process = subprocess.Popen(command, shell=True, executable="/bin/bash")
        #subprocess.Popen(command, shell=True)
        process.wait()
        return JsonResponse({"success": True})


@login_required(login_url="/login/")
def muaban_auto_data(request):
    if request.method == "POST":
        queryset = MuaBanNet_Scraper.objects.filter(
            timestamp__gte=request.POST["timestamp"]
        ).all()
        data = list(queryset.values())
        return JsonResponse({"data": data})


@login_required(login_url="/login/")
def muaban_delete_data(request):
    if request.method == "POST":
        id_array = request.POST["id_array"].split(",")
        MuaBanNet_Scraper.objects.filter(id__in=id_array).delete()
        return JsonResponse({"success": True}) 

# Dang Ban Nha Dat Scraper

class DangBanNhaDatItemListView(ServerSideDatatableView):
    queryset = DangBanNhaDat_Scraper.objects.annotate(formatted_date=Func(
            F('post_time') + 25200, #timezone
            function='to_timestamp',
            output_field=CharField()
        )).order_by("post_time").all()
    columns = [
        "id",
        "updated_at",
        "formatted_date",
        "post_title",
        "type",
        "description",
        "area",
        "price_with_unit",
        "address",
        "url",
        "post_author",   
        "phone_number"
    ]


@login_required(login_url="/login/")
def dangbannhadat_get_data(request):
    if request.method == "POST":
        command = (
            # environment_command
            # + " && "
            "cd "
            + str(settings.CORE_DIR)
            + "/dangbannhadat_scraper"
            + " && "
        )

        command += (
            'scrapy crawl dangbannhadat -a end_page="'
            + request.POST["end_page"]
            + '" -a auto="False"'
        )
        process = subprocess.Popen(command, shell=True, executable="/bin/bash")
        #subprocess.Popen(command, shell=True)
        process.wait()
        return JsonResponse({"success": True})


@login_required(login_url="/login/")
def dangbannhadat_auto_data(request):
    if request.method == "POST":
        queryset = DangBanNhaDat_Scraper.objects.filter(
            timestamp__gte=request.POST["timestamp"]
        ).all()
        data = list(queryset.values())
        return JsonResponse({"data": data})


@login_required(login_url="/login/")
def dangbannhadat_delete_data(request):
    if request.method == "POST":
        id_array = request.POST["id_array"].split(",")
        DangBanNhaDat_Scraper.objects.filter(id__in=id_array).delete()
        return JsonResponse({"success": True}) 


# Nha Dat 24h

class NhaDat24hItemListView(ServerSideDatatableView):
    queryset = NhaDat24h_Scraper.objects.order_by("updated_at").all()
    columns = [
        "id",
        "updated_at",
        "post_title",
        "type",
        "description",
        "area",
        "bedroom",
        "bathroom",
        "floors",
        "legal",
        "price_with_unit",
        "address",
        "url",
        "post_author",   
        "phone_number"
    ]


@login_required(login_url="/login/")
def nhadat24h_get_data(request):
    if request.method == "POST":
        command = (
            # environment_command
            # + " && "
            "cd "
            + str(settings.CORE_DIR)
            + "/nhadat24h_scraper"
            + " && "
        )

        command += (
            'scrapy crawl nhadat24h -a end_page="'
            + request.POST["end_page"]
            + '" -a auto="False"'
        )
        process = subprocess.Popen(command, shell=True, executable="/bin/bash")
        #subprocess.Popen(command, shell=True)
        process.wait()
        return JsonResponse({"success": True})


@login_required(login_url="/login/")
def nhadat24h_auto_data(request):
    if request.method == "POST":
        queryset = NhaDat24h_Scraper.objects.filter(
            timestamp__gte=request.POST["timestamp"]
        ).all()
        data = list(queryset.values())
        return JsonResponse({"data": data})


@login_required(login_url="/login/")
def nhadat24h_delete_data(request):
    if request.method == "POST":
        id_array = request.POST["id_array"].split(",")
        NhaDat24h_Scraper.objects.filter(id__in=id_array).delete()
        return JsonResponse({"success": True}) 


# Viec Lam Tot Scraper

@login_required(login_url="/login/")
def vieclamtot_index(request):

    context = {}
    # context['segment'] = 'index'
    context["segment"] = "vieclamtot-scraper"

    # html_template = loader.get_template( 'index.html' )
    # html_template = loader.get_template( 'dashboard.html' )

    html_template = loader.get_template("vieclamtot-scraper.html")
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def vieclamtot_phone_index(request):
    jt = request.GET.get('job', None)
    return render(request, 'vieclamtot-phone-user.html', {'job_type' : jt.replace('\'', '')})


class ViecLamTotItemListView(ServerSideDatatableView):
    queryset = Vieclamtot_Scraper.objects.annotate(formatted_date=Func(
            F('post_time') + 25200, #timezone
            function='to_timestamp',
            output_field=CharField()
        )).order_by("post_time").all()
    columns = [
        "id",
        "updated_at",
        "formatted_date",
        "search_keyword",
        # "page",
        "post_title",
        "job_type",
        "full_description",
        "company_name",
        "vacancies",
        "salary_with_unit",
        "min_salary",
        "max_salary",
        "salary_type",
        "contract_type",
        "min_age",
        "max_age",
        "preferred_gender",
        "preferred_education",
        "preferred_working_experience",
        "skills",
        "benefits",
        "street_number",
        "ward",
        "district",
        "city",
        "address",
        "coordinate",
        # "website",
        "url",
        # "is_crawled",
        "post_author",   
        "phone"
    ]


class ViecLamTotPhoneUserView(ServerSideDatatableView):
    def get(self, request, *args, **kwargs):
        jt = request.GET["job_type"]
        self.queryset = Vieclamtot_Scraper.objects.filter(job_type=jt).annotate(formatted_date=Func(
            F('post_time') + 25200,
            function='to_timestamp',
            output_field=DateField()
        )).order_by('post_time').all()
        result = datatable.DataTablesServer(
            request, self.columns, self.get_queryset()).output_result()
        return JsonResponse(result, safe=False)
    
    columns = ['formatted_date', 'post_author', 'phone', 'address']


class ViecLamTotPhoneView(ServerSideDatatableView):
    queryset = Vieclamtot_Scraper.objects.values('job_type').annotate(phone = StringAgg('phone', '; ', ordering=('post_time')), max_id=Max('id'))
    columns = ['max_id', 'job_type', 'phone']


@login_required(login_url="/login/")
def vieclamtot_update_chart(request):
    if request.method == "POST":
        command = (
            # environment_command
            # + " && "
            "cd "
            + str(settings.CORE_DIR)
            + "/vieclamtot_scraper"
            + " && "
        )

        command += (
            'scrapy crawl vieclamtot'
        )
        process = subprocess.Popen(command, shell=True, executable="/bin/bash", stdout=PIPE)
        #subprocess.Popen(command, shell=True)
        o, e = process.communicate()
        print(o)
        process.wait()
        return JsonResponse({"success": True})


@login_required(login_url="/login/")
def vieclamtot_get_data(request):
    if request.method == "POST":
        command = (
            # environment_command
            # + " && "
            "cd "
            + str(settings.CORE_DIR)
            + "/vieclamtot_scraper"
            + " && "
        )

        command += (
            'scrapy crawl vieclamtot -a search_keyword="'
            + request.POST["search_keyword"]
            + '" -a end_page="'
            + request.POST["end_page"]
            + '" -a auto="False"'
        )
        process = subprocess.Popen(command, shell=True, executable="/bin/bash")
        #subprocess.Popen(command, shell=True)
        process.wait()
        return JsonResponse({"success": True})


@login_required(login_url="/login/")
def vieclamtot_auto_data(request):
    if request.method == "POST":
        queryset = Vieclamtot_Scraper.objects.filter(
            timestamp__gte=request.POST["timestamp"]
        ).all()
        data = list(queryset.values())
        return JsonResponse({"data": data})


@login_required(login_url="/login/")
def vieclamtot_delete_data(request):
    if request.method == "POST":
        id_array = request.POST["id_array"].split(",")
        Vieclamtot_Scraper.objects.filter(post_time__in=id_array).delete()
        return JsonResponse({"success": True})

@login_required(login_url="/login/")
def vieclamtot_get_job_filter(request):
    if request.method == "POST":
        job_type = list(Vieclamtot_Scraper.objects.values('job_type').distinct())
        return JsonResponse({"job_type": job_type})        

# @login_required(login_url="/login/")
# def vieclamtot_get_phone_data(request):
#     if request.method == "POST":
#         phone_string = list(Vieclamtot_Scraper.objects.values('job_type').annotate(phone = StringAgg('phone', '; ', distinct=True)))
#         return JsonResponse({"phone_string": phone_string})   

@login_required(login_url="/login/")
def vieclamtot_statistic_chart(request):
    if request.method == "POST":
        stats = list(
            Vieclamtot_Statistic.objects.order_by("-crawled_at")[:5].values(
                'crawled_at', 
                'builder', 
                'seller', 
                'driver', 
                'maid', 
                'restaurant_hotel', 
                'customer_care', 
                'guard', 
                'electrician', 
                'weaver', 
                'beauty_care', 
                'food_processor', 
                'assistant', 
                'mechanic', 
                'unskilled_labor', 
                'salesman', 
                'real_estate', 
                'worker', 
                'multi_industry', 
                'receptionist', 
                'chef_bartender', 
                'audit', 
                'metalist', 
                'carpenter', 
                'shipper'
            )
        )


        return JsonResponse({"statistic": stats})


# Facebook Cookie Check


@login_required(login_url="/login/")
def facebook_cookie_check(request):
    context = {}
    # context['segment'] = 'index'
    context["segment"] = "facebook-cookie-check"

    # html_template = loader.get_template( 'index.html' )
    # html_template = loader.get_template( 'dashboard.html' )

    html_template = loader.get_template("facebook-cookie-check.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def facebook_check_login(request):
    if request.method == "POST":
        path = str(settings.CORE_DIR) + "/facebook_splash_scraper/" + cfg.get_facebook_cookie_prefix() + request.POST["user_id"] + ".json"
        if os.path.exists(path):
            command = (
                # environment_command
                # + " && "
                "cd "
                + str(settings.CORE_DIR)
                + "/facebook_splash_scraper"
                + " && "
            )

            command += (
                "scrapy crawl facebook_check_login -a user_id="
                + request.POST["user_id"]
            )
            p = subprocess.Popen(command, shell=True, executable="/bin/bash")
            # p = subprocess.Popen(command, shell=True)
            p.wait()
            
            if os.path.exists(
                str(settings.CORE_DIR)
                + "/facebook_splash_scraper/"
                + cfg.get_facebook_cookie_prefix()
                + request.POST["user_id"]
                + ".json"
            ) and os.path.exists(
                str(settings.CORE_DIR)
                + "/facebook_splash_scraper/"
                + cfg.get_facebook_cookie_prefix()
                + request.POST["user_id"]
                + ".txt"
            ):
                return JsonResponse({"success": True})
            return JsonResponse({"success": True})
        return JsonResponse({'status':'false'}, status=500)


def _handle_uploaded_file(dst, f):
    with open(dst, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required(login_url="/login/")
def facebook_upload_file(request):
    if request.method == "POST":
        context = {}
        context["segment"] = "facebook-cookie-check"

        if request.FILES.get("file", "") != "":
            _handle_uploaded_file(
                str(settings.CORE_DIR)
                + "/facebook_splash_scraper/"
                + cfg.get_facebook_cookie_prefix()
                + str(request.POST["user_id"])
                + ".json",
                request.FILES["file"],
            )

        html_template = loader.get_template("facebook-cookie-check.html")
        return HttpResponse(html_template.render(context, request))


# Facebook Search
@login_required(login_url="/login/")
def facebook_index(request):

    context = {}
    # context['segment'] = 'index'
    context["segment"] = "facebook-search-scraper"

    # html_template = loader.get_template( 'index.html' )
    # html_template = loader.get_template( 'dashboard.html' )

    html_template = loader.get_template("facebook-search-scraper.html")
    return HttpResponse(html_template.render(context, request))


class FacebookItemListView(ServerSideDatatableView):
    queryset = Facebook_Search_Scraper.objects.order_by("-timestamp").all()
    columns = [
        "id",
        "keyword",
        "name",
        "bio",
        "work",
        "friends",
        "link",
        "datetime",
        "timestamp",
    ]


@login_required(login_url="/login/")
def facebook_search_get_data(request):
    if request.method == "POST":
        command = (
            # environment_command
            # + " && "
            "cd "
            # + str(settings.CORE_DIR)
            + "/facebook_splash_scraper"
            + " && "
        )

        command += (
            'scrapy crawl facebook_auto_search -a search_keyword="'
            + request.POST["search_keyword"]
            + '" -a user_id="'
            + str(request.user.id)
            + '" -a scrolls='
            + request.POST["scrolls"]
        )
        # subprocess.Popen(command, shell=True, executable="/bin/bash")
        subprocess.Popen(command, shell=True)
        return JsonResponse({"success": True})


@login_required(login_url="/login/")
def facebook_search_auto_data(request):
    if request.method == "POST":
        queryset = Facebook_Search_Scraper.objects.filter(
            timestamp__gte=request.POST["timestamp"]
        ).all()
        data = list(queryset.values())
        return JsonResponse({"data": data})


@login_required(login_url="/login/")
def facebook_search_delete_data(request):
    if request.method == "POST":
        id_array = request.POST["id_array"].split(",")
        Facebook_Search_Scraper.objects.filter(id__in=id_array).delete()
        return JsonResponse({"success": True})


# Facebook Post


@login_required(login_url="/login/")
def facebook_post_index(request):
    context = {}
    # context['segment'] = 'index'
    context["segment"] = "facebook-post-scraper"

    if not os.path.exists(
        str(settings.CORE_DIR)
        + "/facebook_splash_scraper/"
        + cfg.get_facebook_group_file_prefix()
        + str(request.user.id)
        + ".txt"
    ):
        with open(
            str(settings.CORE_DIR)
            + "/facebook_splash_scraper/"
            + cfg.get_facebook_group_file_prefix()
            + str(request.user.id)
            + ".txt",
            "w+",
        ) as f:
            f.write("")

    with open(
        str(settings.CORE_DIR)
        + "/facebook_splash_scraper/"
        + cfg.get_facebook_group_file_prefix()
        + str(request.user.id)
        + ".txt",
        "r",
    ) as f:
        context["group_list"] = f.read()

    # html_template = loader.get_template( 'index.html' )
    # html_template = loader.get_template( 'dashboard.html' )

    html_template = loader.get_template("facebook-post-scraper.html")
    return HttpResponse(html_template.render(context, request))


class FacebookPostItemListView(ServerSideDatatableView):
    queryset = Facebook_Post_Scraper.objects.order_by("-updated_at").all()
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
def facebook_post_get_data(request):
    if request.method == "POST":
        # with open(
        #     str(settings.CORE_DIR)
        #     + "/facebook_splash_scraper/"
        #     + cfg.get_facebook_group_file_prefix()
        #     + str(request.user.id)
        #     + ".txt",
        #     "w+",
        # ) as f:
        #     f.write(request.POST["group_list"])

        # command = (
        #     # environment_command
        #     # + " && "
        #     "cd "
        #     # + str(settings.CORE_DIR)
        #     + "/facebook_splash_scraper"
        #     + " && "
        # )

        # the_uuid = uuid.uuid4()
        # command += (
        #     'scrapy crawl facebook_links -a user_id="'
        #     + str(request.user.id)
        #     + '" -a the_uuid="'
        #     + str(the_uuid)
        #     + '" -a scrolls='
        #     + request.POST["scrolls"]
        # )
        # command += " && "
        # command += (
        #     'scrapy crawl facebook_posts -a user_id="'
        #     + str(request.user.id)
        #     + '" -a the_uuid="'
        #     + str(the_uuid)
        #     + '" -a scrolls='
        #     + request.POST["scrolls"]
        # )

        # # print(command)
        # # subprocess.Popen(command, shell=True, executable="/bin/bash")
        # subprocess.Popen(command, shell=True)
        pages = int(request.POST["scrolls"])
        group_lists = request.POST["group_list"]
        # first_group = group_lists.split(',')[0]
        # print(str(settings.CORE_DIR)
        #         + "/facebook_splash_scraper/"
        #         + cfg.get_facebook_cookie_prefix()
        #         + str(request.user.id)
        #         + "_backup.json",)
        # print(first_group)
        # print(first_group.split('/')[-1])
        # group_id  =first_group.split('/')[-1]
        for test_group in group_lists.split(','): 
            test_group_id = test_group.split('/')[-1]
            if test_group_id is not None:
                for post in get_posts(
                    group=test_group_id, 
                    cookies = str(settings.CORE_DIR)
                        + "/facebook_splash_scraper/"
                        + cfg.get_facebook_cookie_prefix()
                        + str(request.user.id)
                        + "_backup.json",
                    pages = pages,
                    options={"allow_extra_requests": False}):
                        
                        Facebook_Post_Scraper.objects.create(
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

                        try:
                            profile = get_profile(
                            str(post['user_id']),
                            cookies=str(settings.CORE_DIR)
                            + "/facebook_splash_scraper/"
                            + cfg.get_facebook_cookie_prefix()
                            + str(request.user.id)
                            + "_backup.json",
                            )

                            Facebook_User_From_Group_Scraper.objects.create(
                                user_id=profile["id"],
                                group_id = test_group_id,
                                name=profile["Name"],
                                work=profile.get("Work", ""),
                                education=profile.get("Education",""),
                                friend_count=int(profile["Friend_count"] or 0),
                                follower_count=int(profile["Follower_count"] or 0),
                                following_count=int(profile["Following_count"] or 0),
                            )
                        except Exception as e:
                            print(str(traceback.format_exc()))
                time.sleep(20)
            
        # for post in get_posts(
        #     group=group_id, 
        #     cookies = str(settings.CORE_DIR)
        #         + "/facebook_splash_scraper/"
        #         + cfg.get_facebook_cookie_prefix()
        #         + str(request.user.id)
        #         + "_backup.json",
        #     pages = pages,
        #     options={"allow_extra_requests": False}):
        #         Facebook_Post_Scraper.objects.create(
        #             post_message = post['text'],
        #             post_image_link = post['image'],
        #             post_total_reactions = post['likes'],
        #             post_total_comments = post['comments'],
        #             post_total_shares = post['shares'],
        #             group_id = group_id,
        #             post_id =  post['post_id'],
        #             post_user_id = post['user_id'],
        #             timestamp  = post['time'].timestamp()
        #             )
                    # post_message = post['text'],
                    # post_image_link = '1',
                    # post_total_reactions = 2,
                    # post_total_comments = 3,
                    # post_total_shares = 4,
                # break
                # print(post_id)
                # id = models.AutoField(primary_key=True)
                # group_id = models.CharField(max_length=191)
                # post_id = models.CharField(max_length=191)
                # post_user_id = models.CharField(max_length=191)
                # post_message = models.TextField(null=True)
                # post_image_link = models.TextField(null=True)
                # post_image_alt = models.TextField(null=True)
                # post_total_reactions = models.BigIntegerField(default=0)
                # post_total_comments = models.BigIntegerField(default=0)
                # post_total_shares = models.BigIntegerField(default=0)
                # timestamp = models.FloatField(default=get_default_my_date())
                # created_at = models.FloatField(default=get_default_my_date())
                # updated_at = models.FloatField(default=get_default_my_date())
        return JsonResponse({"success": True})


@login_required(login_url="/login/")
def facebook_post_auto_data(request):
    if request.method == "POST":
        queryset = Facebook_Post_Scraper.objects.filter(
            timestamp__gte=request.POST["timestamp"]
        ).all()
        data = list(queryset.values())
        return JsonResponse({"data": data})


@login_required(login_url="/login/")
def facebook_post_delete_data(request):
    if request.method == "POST":
        id_array = request.POST["id_array"].split(",")
        Facebook_Post_Scraper.objects.filter(id__in=id_array).delete()
        return JsonResponse({"success": True})



@login_required(login_url="/login/")
def facebook_post_chart(request):
    if request.method == "POST":
        likes = list(
            Facebook_Post_Scraper.objects.order_by("-post_total_reactions")[:7].values(
                "group_id", "post_id", "post_total_reactions"
            )
        )
        comments = list(
            Facebook_Post_Scraper.objects.order_by("-post_total_comments")[:7].values(
                "group_id", "post_id", "post_total_comments"
            )
        )
        return JsonResponse({"likes": likes, "comments": comments})


@login_required(login_url="/login/")
def facebook_post_get_comments(request):
    if request.method == "POST":
        post_id = request.POST["post_id"]
        print(post_id)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT user_name, user_id, post_message, post_comment_parent_id FROM app_facebook_comment_scraper, app_facebook_user_scraper WHERE app_facebook_comment_scraper.post_id = '"
                + post_id
                + "' AND app_facebook_comment_scraper.post_comment_user_id = app_facebook_user_scraper.user_id"
            )
            comments = cursor.fetchall()

        return JsonResponse({"comments": comments})


# Facebook User


@login_required(login_url="/login/")
def facebook_user_index(request):

    context = {}
    # context['segment'] = 'index'
    context["segment"] = "facebook-user-scraper"

    html_template = loader.get_template("facebook-user-scraper.html")
    return HttpResponse(html_template.render(context, request))


class FacebookUserItemListView(ServerSideDatatableView):
    queryset = Facebook_User_Scraper.objects.order_by("-updated_at").all()
    columns = [
        "id",
        "user_name",
        "user_id",
        "post_id",
        "post_comment_id",
        "post_reaction_id",
        "total_posts",
        "total_comments",
        "total_reactions",
        "created_at",
        "updated_at",
    ]


@login_required(login_url="/login/")
def facebook_user_auto_data(request):
    if request.method == "POST":
        queryset = Facebook_User_Scraper.objects.filter(
            timestamp__gte=request.POST["-updated_at"]
        ).all()
        data = list(queryset.values())
        return JsonResponse({"data": data})


@login_required(login_url="/login/")
def facebook_user_delete_data(request):
    if request.method == "POST":
        id_array = request.POST["id_array"].split(",")
        Facebook_User_Scraper.objects.filter(id__in=id_array).delete()
        return JsonResponse({"success": True})


@login_required(login_url="/login/")
def facebook_user_chart(request):
    if request.method == "POST":
        posts = list(
            Facebook_User_Scraper.objects.order_by("-total_posts")[:7].values(
                "user_name", "user_id", "total_posts"
            )
        )
        comments = list(
            Facebook_User_Scraper.objects.order_by("-total_comments")[:7].values(
                "user_name", "user_id", "total_comments"
            )
        )
        return JsonResponse({"posts": posts, "comments": comments})


# Facebook Comment


@login_required(login_url="/login/")
def facebook_comment_index(request):

    context = {}
    # context['segment'] = 'index'
    context["segment"] = "facebook-comment-scraper"

    html_template = loader.get_template("facebook-comment-scraper.html")
    return HttpResponse(html_template.render(context, request))


class FacebookCommentItemListView(ServerSideDatatableView):
    queryset = Facebook_Comment_Scraper.objects.order_by("-updated_at").all()
    columns = [
        "id",
        "post_id",
        "post_comment_user_id",
        "post_comment_parent_id",
        "post_message",
        "post_total_reactions",
        "post_image_link",
        "post_image_alt",
        "post_tags",
        "post_links",
        "post_attach_link",
        "timestamp",
        "created_at",
        "updated_at",
    ]


@login_required(login_url="/login/")
def facebook_comment_auto_data(request):
    if request.method == "POST":
        queryset = Facebook_Comment_Scraper.objects.filter(
            timestamp__gte=request.POST["-updated_at"]
        ).all()
        data = list(queryset.values())
        return JsonResponse({"data": data})


@login_required(login_url="/login/")
def facebook_comment_delete_data(request):
    if request.method == "POST":
        id_array = request.POST["id_array"].split(",")
        Facebook_Comment_Scraper.objects.filter(id__in=id_array).delete()
        return JsonResponse({"success": True})


@login_required(login_url="/login/")
def facebook_user_profile_index(request):
    context = {}
    context["segment"] = "facebook-user-profile-scraper"

    html_template = loader.get_template("facebook-user-profile-scraper.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def facebook_user_profile_get_data(request):
    if request.method == "POST":
        profile_url = request.POST["profile_url"]

        user_name = profile_url.split("/")[-1]
        profile = get_profile(
            user_name,
            cookies=str(settings.CORE_DIR)
            + "/facebook_splash_scraper/"
            + cfg.get_facebook_cookie_prefix()
            + str(request.user.id)
            + "_backup.json",
        )

        # for key in profile.keys():
        #     print(key, profile[key])
        Facebook_User_Profile_Scraper.objects.create(
            user_id=profile["id"],
            user_name=user_name,
            name=profile["Name"],
            work=profile.get("Work", ""),
            education=profile.get("Education",""),
            # places_lived = models.CharField(max_length=500)
            # contact_info = models.CharField(max_length=500)
            # basic_info = models.CharField(max_length=500)
            friend_count=int(profile["Friend_count"] or 0),
            follower_count=int(profile["Follower_count"] or 0),
            following_count=int(profile["Following_count"] or 0),
            cover_photo=profile.get("cover_photo",''),
            profile_picture=profile.get("profile_picture",''),
        )

        return JsonResponse({"success": True})


@login_required(login_url="/login/")
def facebook_user_profile_auto_data(request):
    if request.method == "POST":
        queryset = Facebook_User_Profile_Scraper.objects.order_by("-updated_at").all()
        data = list(queryset.values())
        return JsonResponse({"data": data})


@login_required(login_url="/login/")
def facebook_user_profile_delete_data(request):
    if request.method == "POST":

        return JsonResponse({"success": True})


class FacebookUserProfileListView(ServerSideDatatableView):
    queryset = Facebook_User_Profile_Scraper.objects.order_by("-updated_at").all()
    columns = [
        "id",
        "user_id",
        "user_name",
        "name",
        "work",
        "education",
        "friend_count",
        "follower_count",
        "following_count",
        "cover_photo",
        "profile_picture",
    ]

class FacebookUserFromGroupListView(ServerSideDatatableView):
    queryset = Facebook_User_From_Group_Scraper.objects.order_by("-updated_at").all()
    columns = [
        "id",
        "user_id",
        "group_id",
        "name",
        "work",
        "education",
        "friend_count",
        "follower_count",
        "following_count",
        "created_at",
        "updated_at"
    ]


@login_required(login_url="/login/")
def facebook_user_from_group_get_data(request):
    if request.method == "POST":
        pages = 100
        group_lists = request.POST["group_list"]

        for test_group in group_lists.split(','): 
            test_group_id = test_group.split('/')[-1]
            if test_group_id is not None:
                
                    posts = get_posts(
                        group=test_group_id, 
                        cookies = str(settings.CORE_DIR)
                            + "/facebook_splash_scraper/"
                            + cfg.get_facebook_cookie_prefix()
                            + str(request.user.id)
                            + "_backup.json",
                        pages = pages,
                        options={"allow_extra_requests": False})

                    # print(len(posts))        
                    for post in posts:
                        try:
                            profile = get_profile(
                            str(post['user_id']),
                            cookies=str(settings.CORE_DIR)
                            + "/facebook_splash_scraper/"
                            + cfg.get_facebook_cookie_prefix()
                            + str(request.user.id)
                            + "_backup.json",
                            )

                            Facebook_User_From_Group_Scraper.objects.create(
                                user_id=profile["id"],
                                group_id = test_group_id,
                                name=profile["Name"],
                                work=profile.get("Work", ""),
                                education=profile.get("Education",""),
                                friend_count=int(profile["Friend_count"] or 0),
                                follower_count=int(profile["Follower_count"] or 0),
                                following_count=int(profile["Following_count"] or 0),
                            )
                        except Exception as e:
                            print(str(traceback.format_exc()))
                            
                    time.sleep(20)
            
        return JsonResponse({"success": True})    


@login_required(login_url="/login/")
def facebook_user_from_group_delete_data(request):
    if request.method == "POST":
        id_array = request.POST["id_array"].split(",")
        Facebook_User_From_Group_Scraper.objects.filter(id__in=id_array).delete()
        return JsonResponse({"success": True})

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split("/")[-1]
        context["segment"] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template("page-500.html")
        return HttpResponse(html_template.render(context, request))
