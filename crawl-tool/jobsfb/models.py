from django.db import models

# Create your models here.

from django.db import models
import datetime

def get_default_my_date():
    return datetime.datetime.utcnow().timestamp()


class Facebook_Post_Job_Scraper(models.Model):
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
    class Meta:
       ordering = ['-id']

class Facebook_User_Profile_Job_Scraper(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.CharField(max_length=191)
    group_id = models.CharField(max_length=191)
    user_id_job = models.BigIntegerField(default=None)
    user_name_job = models.CharField(max_length=250, default="-1")
    name = models.CharField(max_length=250)
    work = models.CharField(max_length=500, default=None)
    education = models.CharField(max_length=500, default=None)
    friend_count = models.IntegerField(default=None, null=True)
    follower_count = models.IntegerField(default=None,null=True)
    following_count = models.IntegerField(default=None, null=True)
    cover_photo = models.CharField(max_length=500, default=None, null=True)
    profile_picture = models.CharField(max_length=500, default=None, null=True)
    created_at = models.FloatField(default=get_default_my_date())
    updated_at = models.FloatField(default=get_default_my_date())

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=["user_id_job"], name="facebook user id job"),
            models.UniqueConstraint(fields=["user_name_job"], name="facebook username job"),
        ]