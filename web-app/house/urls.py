from django.urls import path
from house import views
# http://127.0.0.1:8000/
urlpatterns = [
    path('house/', views.houseApi, name="houseData"),
    path('delete/house', views.delete_house, name="delete-record-house"),
    # path('api/extract-sentence', views.extract_sentence, name="extract-sentence"),
    path('api/get-sentence', views.get_sentence, name="get-sentence")
]
