from django.urls import path
from house import views
# http://127.0.0.1:8000/house/
urlpatterns = [
    path('house/', views.houseApi, name="houseData"),
]
