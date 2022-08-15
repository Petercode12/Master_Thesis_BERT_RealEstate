
from django.urls import re_path

from . import views

urlpatterns = [
    # Real estate
    re_path(r'get-data', views.real_estate_get_data,
            name='get-data'),
    re_path(r'show-data/chotot', views.show_chotot_data, name='show-data'),
    re_path(r'show-data/muabannet', views.show_muabannet_data, name='show-data'),
    re_path(r'show-data/batdongsancom', views.show_batdongsancom_data, name='show-data'),
    re_path(r'parsing', views.parsing_data, name='show-data'),
    re_path(r'chart-data', views.get_chart_data, name='index'),
    re_path(r'/', views.real_estate_index)
]
