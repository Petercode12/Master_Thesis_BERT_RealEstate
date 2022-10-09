# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from app import views

urlpatterns = [
    # The home page
    path("", views.bd_real_estate_index, name="home"),

    # Binh Duong real estate
    re_path(r"binh-duong-real-estate/", views.bd_real_estate_index,name="binh-duong-real-estate-scraper"),
    
    # AnCu
    re_path(r"ancu-get-data/", views.ancu_get_data, name="ancu-get-data"),
    re_path(r"ancu-auto-data/", views.ancu_auto_data, name="ancu-auto-data"),
    re_path(r"ancu-delete-data/", views.ancu_delete_data, name="ancu-delete-data"),
    re_path(
        r"ancu-show-data/",
        views.AnCuItemListView.as_view(),
        name="ancu-show-data",
    ),

    # Mua Ban
    re_path(r"muaban-get-data/", views.muaban_get_data, name="muaban-get-data"),
    re_path(r"muaban-auto-data/", views.muaban_auto_data, name="muaban-auto-data"),
    re_path(r"muaban-delete-data/", views.muaban_delete_data, name="muaban-delete-data"),
    re_path(
        r"muaban-show-data/",
        views.MuaBanItemListView.as_view(),
        name="muaban-show-data",
    ),

    # Dang Ban Nha Dat
    re_path(r"dangbannhadat-get-data/", views.dangbannhadat_get_data, name="dangbannhadat-get-data"),
    re_path(r"dangbannhadat-auto-data/", views.dangbannhadat_auto_data, name="dangbannhadat-auto-data"),
    re_path(r"dangbannhadat-delete-data/", views.dangbannhadat_delete_data, name="dangbannhadat-delete-data"),
    re_path(
        r"dangbannhadat-show-data/",
        views.DangBanNhaDatItemListView.as_view(),
        name="dangbannhadat-show-data",
    ),

    # Nha dat 24h
    re_path(r"nhadat24h-get-data/", views.nhadat24h_get_data, name="nhadat24h-get-data"),
    re_path(r"nhadat24h-auto-data/", views.nhadat24h_auto_data, name="nhadat24h-auto-data"),
    re_path(r"nhadat24h-delete-data/", views.nhadat24h_delete_data, name="nhadat24h-delete-data"),
    re_path(
        r"nhadat24h-show-data/",
        views.NhaDat24hItemListView.as_view(),
        name="nhadat24h-show-data",
    ),

    
    
    
    #old code block



    # # Matches any html file
    # # re_path(r'^.*\.*', views.pages, name='pages'),
    # # Google Scraper
    # re_path(r"google-scraper/", views.index, name="google-scraper"),
    # re_path(r"google-get-data/", views.google_get_data, name="google-get-data"),
    # re_path(r"google-auto-data/", views.google_auto_data, name="google-auto-data"),
    # re_path(
    #     r"google-delete-data/", views.google_delete_data, name="google-delete-data"
    # ),
    # re_path(
    #     r"google-show-data/",
    #     views.GoogleItemListView.as_view(),
    #     name="google-show-data",
    # ),
    # # Facebook Cookie Check
    # re_path(
    #     r"facebook-cookie-check/",
    #     views.facebook_cookie_check,
    #     name="facebook-cookie-check",
    # ),
    # re_path(
    #     r"facebook-check-login/",
    #     views.facebook_check_login,
    #     name="facebook-check-login",
    # ),
    # re_path(
    #     r"facebook-upload-file/",
    #     views.facebook_upload_file,
    #     name="facebook-upload-file",
    # ),
    # # Facebook Search Scraper
    # re_path(
    #     r"facebook-search-scraper/",
    #     views.facebook_index,
    #     name="facebook-search-scraper",
    # ),
    # re_path(
    #     r"facebook-search-get-data/",
    #     views.facebook_search_get_data,
    #     name="facebook-search-get-data",
    # ),
    # re_path(
    #     r"facebook-search-auto-data/",
    #     views.facebook_search_auto_data,
    #     name="facebook-search-auto-data",
    # ),
    # re_path(
    #     r"facebook-search-delete-data/",
    #     views.facebook_search_delete_data,
    #     name="facebook-search-delete-data",
    # ),
    # re_path(
    #     r"facebook-search-show-data/",
    #     views.FacebookItemListView.as_view(),
    #     name="facebook-search-show-data",
    # ),
    # # Facebook Post Scraper
    # re_path(
    #     r"facebook-post-scraper/",
    #     views.facebook_post_index,
    #     name="facebook-post-scraper",
    # ),
    # re_path(
    #     r"facebook-post-get-data/",
    #     views.facebook_post_get_data,
    #     name="facebook-post-get-data",
    # ),
    # re_path(
    #     r"facebook-post-auto-data/",
    #     views.facebook_post_auto_data,
    #     name="facebook-post-auto-data",
    # ),
    # re_path(
    #     r"facebook-post-delete-data/",
    #     views.facebook_post_delete_data,
    #     name="facebook-post-delete-data",
    # ),
    # re_path(
    #     r"facebook-post-show-data/",
    #     views.FacebookPostItemListView.as_view(),
    #     name="facebook-post-show-data",
    # ),
    # re_path(
    #     r"facebook-post-chart/", views.facebook_post_chart, name="facebook-post-chart"
    # ),

    # re_path(
    #     r"vieclamtot-time-chart/", views.vieclamtot_statistic_chart, name="vieclamtot-time-chart"
    # ),

    # re_path(
    #     r"facebook-post-get-comments/",
    #     views.facebook_post_get_comments,
    #     name="facebook-post-get-comments",
    # ),
    # # Facebook User Scraper
    # re_path(
    #     r"facebook-user-scraper/",
    #     views.facebook_user_index,
    #     name="facebook-user-scraper",
    # ),
    # # re_path(r'facebook-user-get-data/', views.facebook_user_get_data, name='facebook-user-get-data'),
    # re_path(
    #     r"facebook-user-auto-data/",
    #     views.facebook_user_auto_data,
    #     name="facebook-user-auto-data",
    # ),
    # re_path(
    #     r"facebook-user-delete-data/",
    #     views.facebook_user_delete_data,
    #     name="facebook-user-delete-data",
    # ),
    # re_path(
    #     r"facebook-user-show-data/",
    #     views.FacebookUserItemListView.as_view(),
    #     name="facebook-user-show-data",
    # ),
    # re_path(
    #     r"facebook-user-chart/", views.facebook_user_chart, name="facebook-user-chart"
    # ),
    # # Facebook Comment Scraper
    # re_path(
    #     r"facebook-comment-scraper/",
    #     views.facebook_comment_index,
    #     name="facebook-comment-scraper",
    # ),
    # # re_path(r'facebook-user-get-data/', views.facebook_user_get_data, name='facebook-user-get-data'),
    # re_path(
    #     r"facebook-comment-auto-data/",
    #     views.facebook_comment_auto_data,
    #     name="facebook-comment-auto-data",
    # ),
    # re_path(
    #     r"facebook-comment-delete-data/",
    #     views.facebook_comment_delete_data,
    #     name="facebook-comment-delete-data",
    # ),
    # re_path(
    #     r"facebook-comment-show-data/",
    #     views.FacebookCommentItemListView.as_view(),
    #     name="facebook-comment-show-data",
    # ),
    # # Facebook user profile
    # re_path(
    #     r"facebook-user-profile-scraper/",
    #     views.facebook_user_profile_index,
    #     name="facebook-user-profile-scraper",
    # ),
    # re_path(
    #     r"facebook-user-profile-get-data/",
    #     views.facebook_user_profile_get_data,
    #     name="facebook-user-profile-get-data",
    # ),
    # re_path(
    #     r"facebook-user-profile-auto-data/",
    #     views.facebook_user_profile_auto_data,
    #     name="facebook-user-profile-auto-data",
    # ),
    # re_path(
    #     r"facebook-user-profile-delete-data/",
    #     views.facebook_user_profile_delete_data,
    #     name="facebook-user-profile-delete-data",
    # ),
    # re_path(
    #     r"facebook-user-profile-show-data/",
    #     views.FacebookUserProfileListView.as_view(),
    #     name="facebook-user-profile-show-data",
    # ),

    # # Vieclamtot
    # path(r"vieclamtot-phone-user/", views.vieclamtot_phone_index, name="vieclamtot_phone_user_index"),
    # re_path(r"vieclamtot-scraper/", views.vieclamtot_index,name="vieclamtot-scraper"),
    # re_path(r"vieclamtot-update-chart/", views.vieclamtot_update_chart, name="vieclamtot-update-chart"),
    # re_path(r"vieclamtot-get-data/", views.vieclamtot_get_data, name="vieclamtot-get-data"),
    # re_path(r"vieclamtot-auto-data/", views.vieclamtot_auto_data, name="vieclamtot-auto-data"),
    # re_path(r"vieclamtot-delete-data/", views.vieclamtot_delete_data, name="vieclamtot-delete-data"),
    # re_path(r"vieclamtot-get-job-filter/", views.vieclamtot_get_job_filter, name="vieclamtot-get-job-filter"),
    # re_path(r"vieclamtot-phone-data/", views.ViecLamTotPhoneView.as_view(), name="vieclamtot-get-phone-data"),
    # re_path(r"vieclamtot-phone-user-data/", views.ViecLamTotPhoneUserView.as_view(), name="vieclamtot-phone-user-data"),
    # re_path(
    #     r"vieclamtot-show-data/",
    #     views.ViecLamTotItemListView.as_view(),
    #     name="vieclamtot-show-data",
    # ),

    # # Real estate scraper
    # re_path(r'estate-scraper', include('estate_scraper.urls')),

    

    # # Dang Ban Nha Dat
    # re_path(r"facebook_user_from_group_get_data/", views.facebook_user_from_group_get_data, name="facebook_user_from_group_get_data"),
    # re_path(r"facebook_user_from_group_delete_data/", views.facebook_user_from_group_delete_data, name="facebook_user_from_group-delete-data"),
    # re_path(
    #     r"facebook_user_from_group-show-data/",
    #     views.FacebookUserFromGroupListView.as_view(),
    #     name="facebook_user_from_group-show-data",
    # ),
    
    # # Documentation
    # re_path(r"doc-start/", views.doc_start, name="doc-start"),


    #end old code block
]
