import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.core import serializers as core_serializers
# Create your views here.
import pyodbc
from house.models import *
from house.serializers import *

from django.http import HttpResponse
import os
import psycopg2
	
import time

@csrf_exempt
def get_sentence(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        if id is not None and id != "": 
            print(id)
            sentence = Extractsentence.objects.filter(org_id=id)
            house = Houses.objects.filter(house_id=id)[0]
            response = {}
            response['house'] = json.loads(core_serializers.serialize("json", [house]))
            response['result_sentence'] = json.loads(sentence[0].result_sentence)
            return JsonResponse(response)

@csrf_exempt
def houseApi(request):
    if request.method == 'GET':
        os.system("python import-data.py")
        houses = Houses.objects.all()
        houses_serializer = HouseSerializer(houses, many=True)
        return JsonResponse(houses_serializer.data, safe=False)

# server = 'TANPHUOC' 
# database = 'DJANGO_MSSQL' 
# username = 'sa' 
# password = 'ABCD' 

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
            # delete_record_ancu = 'DELETE FROM app_ancu_scraper a WHERE a.id = '+ str(id)
            # delete_record_dangbannhadat = 'DELETE FROM app_dangbannhadat_scraper a WHERE a.id ='+ str(id)
            delete_record_nhadat24h = 'DELETE FROM app_nhadat24h_scraper WHERE id ='+ str(id)
            # delete_record_muaban = 'DELETE FROM app_muabannet_scraper WHERE id =' + str(id)
            # cursor.execute(delete_record_ancu)
            # cursor.execute(delete_record_dangbannhadat)
            cursor.execute(delete_record_nhadat24h)
            # cursor.execute(delete_record_muaban)
            connection.commit()
            connection.close()
            return HttpResponse(status = 200)
    return HttpResponse(status = 400)


@csrf_exempt
def nha_dat_query_all(request):
    if request.method == 'GET':
        connection = psycopg2.connect(
            host="129.146.248.20",
            port="5432", #default
            database="ttndung",
            user="tdung",
            password="8M44Ck48wn3J")
        # connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password+';Trusted_Connection=yes')
        cursor = connection.cursor()
        select_record_nhadat = "SELECT * FROM app_nhadat24h_scraper"
        cursor.execute(select_record_nhadat)
        data = cursor.fetchall()
        connection.commit()
        connection.close()
        return JsonResponse(data, safe=False)

@csrf_exempt
def nha_dat_conditional_query(request):
    if request.method == 'POST':
        area = request.GET.get('area')
        compareArea = request.GET.get('compareArea')
        floors = request.GET.get('floors')
        compareFloors = request.GET.get('compareFloors')
        address = request.GET.get('address')
        owner = request.GET.get('owner')
        logicalOperator = request.GET.get('logicalOperator')
        connection = psycopg2.connect(
            host="129.146.248.20",
            port="5432", #default
            database="ttndung",
            user="tdung",
            password="8M44Ck48wn3J")
        cursor = connection.cursor()
        like1 = "\'%" + str(address) + "%\'"
        like2 = "\'%" + str(owner) + "%\'"
        select_record_nhadat = "SELECT * FROM app_nhadat24h_scraper WHERE area {} {} {} floors {} {} {} address LIKE {} {} post_author LIKE {}".format(compareArea, area, logicalOperator, compareFloors, floors, logicalOperator, like1, logicalOperator, like2)
        print(select_record_nhadat)
        start = time.time()
        cursor.execute(select_record_nhadat)
        end = time.time()
        data = cursor.fetchall()
        delayTime = end-start
        print("Time: ", end-start)
        connection.commit()
        connection.close()
        data.append(delayTime)
        res = JsonResponse(data, safe=False)
        return res
        
