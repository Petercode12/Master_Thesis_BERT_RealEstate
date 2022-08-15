# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.headerregistry import Address
from django.db import models
import datetime

# Create your models here.
class Vieclamtot_Statistic(models.Model):
    """
    Statistics about one time crawl in vieclamtot
    Time crawled
    Id: AutoIncrement
    Time: 
    Crawled Post: including Created + Updated 
    keywords
    """
    id = models.AutoField(primary_key=True)
    crawled_at = models.CharField(max_length=191)
    builder = models.IntegerField(default=0)
    seller = models.IntegerField(default=0)
    driver = models.IntegerField(default=0)
    maid = models.IntegerField(default=0)
    restaurant_hotel = models.IntegerField(default=0)
    customer_care = models.IntegerField(default=0)
    guard = models.IntegerField(default=0)
    electrician = models.IntegerField(default=0)
    weaver = models.IntegerField(default=0)
    beauty_care = models.IntegerField(default=0)
    food_processor = models.IntegerField(default=0)
    assistant = models.IntegerField(default=0)
    mechanic = models.IntegerField(default=0)
    unskilled_labor = models.IntegerField(default=0)
    salesman = models.IntegerField(default=0)
    real_estate = models.IntegerField(default=0)
    worker = models.IntegerField(default=0)
    multi_industry = models.IntegerField(default=0)
    receptionist = models.IntegerField(default=0)
    chef_bartender = models.IntegerField(default=0)
    audit = models.IntegerField(default=0)
    metalist = models.IntegerField(default=0)
    carpenter = models.IntegerField(default=0)
    shipper = models.IntegerField(default=0)


class Vieclamtot_Scraper(models.Model):
    id = models.AutoField(primary_key=True)
    search_keyword = models.CharField(max_length=191)
    # page = models.IntegerField()
    post_title = models.TextField(null=True)
    post_author = models.CharField(max_length=191, null=True)
    job_type = models.CharField(max_length=191, null=True)
    full_description = models.TextField(null=True)
    vacancies = models.CharField(max_length=191, null = True)
    company_name = models.TextField(max_length=191, null = True)
    phone = models.CharField(max_length=20, null=True)
    salary_with_unit = models.CharField(max_length=191, null = True)
    min_salary = models.IntegerField(null=True)
    max_salary = models.IntegerField(null=True)
    salary_type = models.CharField(max_length=191, null=True)
    contract_type = models.CharField(max_length=191, null=True)
    min_age = models.IntegerField(null=True)
    max_age = models.IntegerField(null=True)
    preferred_education = models.TextField(null=True)
    preferred_gender = models.TextField(null=True)
    preferred_working_experience = models.TextField(null=True)
    skills = models.TextField(null=True)
    benefits = models.TextField(null=True)
    street_number = models.CharField(max_length=191, null=True)
    ward = models.TextField(null=True)
    district = models.TextField(null=True)
    city = models.TextField(null=True)
    address = models.TextField(null=True)
    coordinate = models.CharField(max_length=191, null=True)
    website = models.CharField(max_length=191)
    url = models.CharField(max_length=191, unique=True)
    post_time = models.BigIntegerField(null=True)
    updated_at = models.CharField(max_length=191)
    job_id = models.IntegerField(null=True)
    auto = models.CharField(max_length=191)

    class Meta:
        indexes = [
            models.Index(fields=["search_keyword"]),
            # models.Index(fields=["page"]),
    
        ]

class Google_Scraper(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=191)
    crawled_page = models.IntegerField()
    title = models.CharField(max_length=191, unique=True)
    link = models.CharField(max_length=191, unique=True)
    datetime = models.CharField(max_length=191)
    timestamp = models.BigIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["keyword"]),
            models.Index(fields=["crawled_page"]),
        ]


class Facebook_Search_Scraper(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=191)
    scrolls = models.IntegerField()
    name = models.CharField(max_length=191)
    bio = models.CharField(max_length=191, null=True)
    work = models.CharField(max_length=191, null=True)
    friends = models.CharField(max_length=191, null=True)
    link = models.CharField(max_length=191, unique=True)
    datetime = models.CharField(max_length=191)
    timestamp = models.BigIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["keyword"]),
            models.Index(fields=["scrolls"]),
        ]


def get_default_my_date():
    return datetime.datetime.utcnow().timestamp()


class Facebook_Post_Scraper(models.Model):
    id = models.AutoField(primary_key=True)
    group_id = models.CharField(max_length=191)
    post_id = models.CharField(max_length=191)
    post_user_id = models.CharField(max_length=191)
    post_message = models.TextField(null=True)
    post_image_link = models.TextField(null=True)
    post_image_alt = models.TextField(null=True)
    post_total_reactions = models.BigIntegerField(default=0)
    post_total_comments = models.BigIntegerField(default=0)
    post_total_shares = models.BigIntegerField(default=0)
    timestamp = models.FloatField(default=get_default_my_date())
    created_at = models.FloatField(default=get_default_my_date())
    updated_at = models.FloatField(default=get_default_my_date())

    # class Meta:
    #     indexes = [
    #         models.Index(fields=["group_id"]),
    #     ]
    #     unique_together = (("group_id", "post_id"),)


class Facebook_User_Scraper(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=191)
    user_id = models.CharField(max_length=191, default="-1")
    post_id = models.TextField(null=True)
    post_comment_id = models.TextField(null=True)
    post_reaction_id = models.TextField(null=True)
    total_posts = models.BigIntegerField(default=0)
    total_comments = models.BigIntegerField(default=0)
    total_reactions = models.BigIntegerField(default=0)
    created_at = models.FloatField(default=get_default_my_date())
    updated_at = models.FloatField(default=get_default_my_date())

    class Meta:
        indexes = [
            models.Index(fields=["user_name"]),
            models.Index(fields=["user_id"]),
            models.Index(fields=["post_id"]),
            models.Index(fields=["post_comment_id"]),
        ]
        unique_together = (("user_name", "user_id"),)


class Facebook_Comment_Scraper(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.CharField(max_length=191)
    post_comment_user_id = models.CharField(max_length=191)
    post_comment_parent_id = models.CharField(max_length=191, null=True)
    post_message = models.TextField()
    post_total_reactions = models.BigIntegerField(default=0)
    post_image_link = models.TextField(null=True)
    post_image_alt = models.TextField(null=True)
    post_tags = models.TextField(null=True)
    post_links = models.TextField(null=True)
    post_attach_link = models.TextField(null=True)
    timestamp = models.FloatField(default=get_default_my_date())
    created_at = models.FloatField(default=get_default_my_date())
    updated_at = models.FloatField(default=get_default_my_date())

    class Meta:
        indexes = [
            models.Index(fields=["post_comment_user_id"]),
            models.Index(fields=["post_id"]),
        ]


class Facebook_Reaction_Scraper(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.CharField(max_length=191)
    post_user_id = models.CharField(max_length=191)
    like_reaction = models.BigIntegerField(null=True)
    created_at = models.FloatField(default=get_default_my_date())
    updated_at = models.FloatField(default=get_default_my_date())

    class Meta:
        indexes = [
            models.Index(fields=["post_user_id"]),
            models.Index(fields=["post_id"]),
        ]
        unique_together = (("post_user_id", "post_id"),)


class Facebook_User_Profile_Scraper(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(default=None)
    user_name = models.CharField(max_length=250, default="-1")
    name = models.CharField(max_length=250)
    work = models.CharField(max_length=500, default=None)
    education = models.CharField(max_length=500, default=None)
    # places_lived = models.CharField(max_length=500)
    # contact_info = models.CharField(max_length=500)
    # basic_info = models.CharField(max_length=500)
    friend_count = models.IntegerField(default=None)
    follower_count = models.IntegerField(default=None)
    following_count = models.IntegerField(default=None)
    cover_photo = models.CharField(max_length=500, default=None)
    profile_picture = models.CharField(max_length=500, default=None)
    created_at = models.FloatField(default=get_default_my_date())
    updated_at = models.FloatField(default=get_default_my_date())

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user_id"], name="facebook user id"),
            models.UniqueConstraint(fields=["user_name"], name="facebook username"),
        ]

class Facebook_User_From_Group_Scraper(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(default=None)
    group_id = models.CharField(max_length=191)
    name = models.CharField(max_length=250)
    work = models.TextField(default=None)
    education = models.TextField(default=None)
    friend_count = models.IntegerField(default=None)
    follower_count = models.IntegerField(default=None)
    following_count = models.IntegerField(default=None)
    created_at = models.FloatField(default=get_default_my_date())
    updated_at = models.FloatField(default=get_default_my_date())


class MuaBanNet_Scraper(models.Model):
    id = models.IntegerField(primary_key=True)
    post_title = models.CharField(max_length=100, null=True)
    post_time = models.BigIntegerField(null=True)
    post_author = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    price = models.BigIntegerField(null=True)
    price_with_unit = models.CharField(max_length=100, null=True)
    phone_number = models.BigIntegerField(null=True)
    address = models.TextField(null=True)
    location = models.CharField(max_length=100, null=True)
    land_area = models.FloatField(null=True)
    bedroom = models.IntegerField(null=True)
    bathroom = models.IntegerField(null=True)
    floors = models.IntegerField(null=True)
    legal = models.CharField(max_length=100, null=True)
    search_keywords = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=True)
    website = models.CharField(max_length=191, null=True)
    url = models.CharField(max_length=191, unique=True)
    updated_at = models.CharField(max_length=191, null=True)

class DangBanNhaDat_Scraper(models.Model):
    id = models.IntegerField(primary_key=True)
    post_title = models.CharField(max_length=200, null=True)
    post_author = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    price_with_unit = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True)
    area = models.FloatField(null=True)
    phone_number = models.BigIntegerField(null=True)
    website = models.CharField(max_length=191, null=True)
    url = models.CharField(max_length=191, unique=True)
    type = models.CharField(max_length=100, null=True)
    post_time = models.BigIntegerField(null=True)
    updated_at = models.CharField(max_length=191, null=True)

class AnCu_Scraper(models.Model):
    id = models.IntegerField(primary_key=True)
    post_title = models.CharField(max_length=200, null=True)
    post_author = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    price_with_unit = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True)
    area = models.FloatField(null=True)
    phone_number = models.BigIntegerField(null=True)
    website = models.CharField(max_length=191, null=True)
    url = models.CharField(max_length=191, unique=True)
    type = models.CharField(max_length=100, null=True)
    updated_at = models.CharField(max_length=191, null=True)
    post_time = models.BigIntegerField(null=True)
    coordinate = models.CharField(max_length=191, null=True)

class NhaDat24h_Scraper(models.Model):
    id = models.IntegerField(primary_key=True)
    post_title = models.CharField(max_length=200, null=True)
    post_author = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    price_with_unit = models.CharField(max_length=100, null=True)
    bedroom = models.IntegerField(null=True)
    bathroom = models.IntegerField(null=True)
    floors = models.IntegerField(null=True)
    legal = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True)
    area = models.FloatField(null=True)
    phone_number = models.BigIntegerField(null=True)
    website = models.CharField(max_length=191, null=True)
    url = models.CharField(max_length=191, unique=True)
    type = models.CharField(max_length=100, null=True)
    updated_at = models.CharField(max_length=191, null=True)
    post_time = models.BigIntegerField(null=True)
    
