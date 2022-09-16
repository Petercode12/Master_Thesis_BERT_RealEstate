import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.core import serializers as core_serializers
# Create your views here.

from house.models import *
from house.serializers import *

from django.http import HttpResponse
import os
import psycopg2

# from .bertapi.utils import DatasetProcessor, PhoBERT

# processor = DatasetProcessor()
# processor.load_tags()
# 

# __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
# bert = PhoBERT(labels=processor.get_tags(), 
# config_file_path=os.path.join(__location__,'bertapi','PhoBERT_base_transformers','config.json'),
# pretrained_model_path=os.path.join(__location__,'bertapi','PhoBERT_base_transformers','model.bin'))
# bert.load_model(filename=os.path.join(__location__,'bertapi','model-training','phobert'))


@csrf_exempt
def get_sentence(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        if id is not None and id != "": 
            print(id)
            sentence = Extractsentence.objects.filter(org_id=id)
            house = Houses.objects.filter(house_id=id)[0]
            response = {}
            # if len(sentence) == 0:
            #     print(house.Description)
            #     #result = extractSentenceApi(house.Description)
            #     contents, labels = bert.predict_sentence(house.Description)
            #     jsonResult = ''
            #     start = 0
            #     for content, label in zip(contents, labels):
            #         if start > 0 :
            #             jsonResult += ','
            #         jsonResult += f'{{"{label}": "{content}"}}'
            #         start += 1
            #     result = f'[{jsonResult}]'
            #     Extractsentence.objects.create(org_id=id,result_sentence=result)
            #     response['house'] =json.loads(core_serializers.serialize("json", [house]))
            #     response['result_sentence'] = json.loads(result)
            #     return JsonResponse(response)
            response['house'] = json.loads(core_serializers.serialize("json", [house]))
            response['result_sentence'] = json.loads(sentence[0].result_sentence)
            return JsonResponse(response)

# @csrf_exempt
# def extract_sentence(request):
#     if request.method == "POST":
#         sentence = request.POST['sentence']
#         print(sentence)
#         if sentence is not None and sentence != "": 
#             result = extractSentenceApi(sentence)
#             return JsonResponse( json.loads(result), safe=False)

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
