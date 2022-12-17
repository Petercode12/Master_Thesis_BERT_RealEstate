# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import csv
import sqlite3
from statistics import mode
from django.db import models

# Create your models here.

# Person for login


class Houses(models.Model):
    house_id = models.AutoField(primary_key=True, blank=True)
    LoaiHinh = models.CharField(max_length=200, blank=True)
    TacGia = models.CharField(max_length=200, blank=True)
    SoDienThoai = models.CharField(max_length=30, blank=True)
    Gia = models.CharField(max_length=200, blank=True)
    DienTich = models.CharField(max_length=200, null=True, blank=True)
    DiaChi = models.CharField(max_length=200, blank=True)
    ChungNhanSoHuu = models.CharField(max_length=200, null=True, blank=True)
    Description = models.TextField(null=True)

class Extractsentence(models.Model):
    id = models.AutoField(primary_key=True)
    org_id = models.IntegerField(default=0)
    result_sentence = models.TextField(null=True)