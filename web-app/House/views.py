from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
# Create your views here.

from house.models import Houses
from house.serializers import HouseSerializer

import os

@csrf_exempt
def houseApi(request):
    if request.method == 'GET':
        os.system("python import-data.py")
        houses = Houses.objects.all()
        houses_serializer = HouseSerializer(houses, many=True)
        return JsonResponse(houses_serializer.data, safe=False)
    elif request.method == 'POST':
        houses_data = JSONParser().parse(request)
        houses_serializer = HouseSerializer(data=houses_data)
        if houses_serializer.is_valid():
            houses_serializer.save()
            return JsonResponse("Added successfully", safe=False)
        return JsonResponse("Failed to add", safe=False)
