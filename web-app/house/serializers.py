from rest_framework import serializers
from house.models import *


class HouseSerializer (serializers.ModelSerializer):
    class Meta:
        model = Houses
        fields = ('house_id',
                  'LoaiHinh',
                  'TacGia',
                  'SoDienThoai',
                  'Gia',
                  'DienTich',
                  'DiaChi',
                  'ChungNhanSoHuu',
                  'Description')
        
class SentenceSerializer (serializers.ModelSerializer):
    class Meta:
        model = Extractsentence
        fields = ('id',
                  'org_id',
                  'result_sentence')        
