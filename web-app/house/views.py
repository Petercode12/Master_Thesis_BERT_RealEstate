from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
# Create your views here.

from house.models import Houses
from house.serializers import HouseSerializer

from django.http import HttpResponse
import os
import psycopg2
@csrf_exempt
def houseApi(request):
    if request.method == 'GET':
        os.system("python import-data.py")
        houses = Houses.objects.all()
        houses_serializer = HouseSerializer(houses, many=True)
        return JsonResponse(houses_serializer.data, safe=False)
@csrf_exempt
def delete_house(request):
    if request.method == "POST":
        id = request.GET.get('id')
        if id is not None and id != "": 
            print(id)
            connection = psycopg2.connect(
                host="129.146.248.20",
                port="5432", #default
                database="ttndung",
                user="tdung",
                password="8M44Ck48wn3J")

            cursor = connection.cursor()
            delete_record_ancu = 'DELETE FROM app_ancu_scraper a WHERE a.id = '+ str(id)
            delete_record_dangbannhadat = 'DELETE FROM app_dangbannhadat_scraper a WHERE a.id ='+ str(id)
            delete_record_nhadat24h = 'DELETE FROM app_nhadat24h_scraper WHERE id ='+ str(id)
            delete_record_muaban = 'DELETE FROM app_muabannet_scraper WHERE id =' + str(id)
            cursor.execute(delete_record_ancu)
            cursor.execute(delete_record_dangbannhadat)
            cursor.execute(delete_record_nhadat24h)
            cursor.execute(delete_record_muaban)
            connection.commit()
            connection.close()
            return HttpResponse(status = 200)
    return HttpResponse(status = 400)
