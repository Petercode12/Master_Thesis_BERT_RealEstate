
from django.urls import path, re_path
from jobsfb import views

urlpatterns = [
    # VieclamFromFBGroups
    re_path(
        r"facebook-user-job-show-data/",
        views.FacebookUserProfileListJobListView.as_view(),
        name="facebook-user-job-show-data",
    ),
    re_path(
        r"facebook-post-job-show-data/",
        views.FacebookPostItemJobListView.as_view(),
        name="facebook-post-job-show-data/",
    ),
    re_path(
        r"facebook-user-profile-job-show-data/",
        views.FacebookUserProfileListJobListView.as_view(),
        name="facebook-user-profile-job-show-data",
    ),
    re_path(
        r"facebook-post-job-get-data/",
        views.facebook_post_job_get_data,
        name="facebook-post-job-get-data/",
    ),
    re_path(
        r"facebook-post-job-delete-data/",
        views.facebook_post_job_delete_data,
        name="facebook-post-job-delete-data/",
    ),
    re_path(
        r"facebook-user-profile-job-delete-data/",
        views.facebook_user_profile_job_delete_data,
        name="facebook-user-profile-job-delete-data/",
    ),
    re_path(
        r"facebook-user-profile-job-auto-data/",
        views.facebook_user_profile_job_auto_data,
        name="facebook-user-profile-job-auto-data",
    ),
    re_path(
        r"facebook-post-job-auto-data/",
        views.facebook_post_job_auto_data,
        name="facebook-post-job-auto-data",
    ),
    re_path(
        r"facebook-user-profile-job-get-data/",
        views.facebook_user_profile_job_get_data,
        name="facebook-user-profile-job-get-data",
    ),
    path(r"vieclamfb-scraper/", views.vieclamfb_scraper, name="vieclamfb_scraper"),
    path(r"vieclamfb-user-profile-scraper/", views.vieclamfb_user_profile_scraper, name="vieclamfb-user-profile-scraper"),
    path(r"vieclamfb-employment-counseling/", views.vieclamfb_employment_counseling, name="vieclamfb-employment-counseling/"),
]