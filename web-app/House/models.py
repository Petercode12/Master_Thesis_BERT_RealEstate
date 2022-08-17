# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import csv
import sqlite3
from django.db import models

# Create your models here.

# Person for login


class Houses(models.Model):
    house_id = models.AutoField(primary_key=True, blank=True)
    LoaiHinh = models.CharField(max_length=100)
    TacGia = models.CharField(max_length=100)
    SoDienThoai = models.CharField(max_length=20)
    Gia = models.CharField(max_length=100)
    DienTich = models.CharField(max_length=100, blank=True)
    DiaChi = models.CharField(max_length=100)
    ChungNhanSoHuu = models.CharField(max_length=100, blank=True)
