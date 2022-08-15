from django.db import models


class Batdongsancom(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    page = models.IntegerField(null=False)
    posted_at = models.DateTimeField(null=True)
    expired_at = models.DateTimeField(null=True)
    post_rank = models.CharField(max_length=500, null=True)
    post_number = models.CharField(max_length=15, null=True)
    price = models.CharField(max_length=50, null=True)
    size = models.CharField(max_length=50, null=True)
    house_type = models.CharField(max_length=50, null=True)
    direction = models.CharField(max_length=15, null=True)
    floors = models.CharField(max_length=15, null=True)
    location = models.CharField(max_length=150, null=True)
    balcony_direction = models.CharField(max_length=15, null=True)
    bedrooms = models.CharField(max_length=15, null=True)
    toilets = models.CharField(max_length=15, null=True)
    furniture = models.CharField(max_length=150, null=True)
    property_legal = models.CharField(max_length=30, null=True)
    street_in = models.CharField(max_length=15, null=True)
    street = models.CharField(max_length=15, null=True)
    detail_header = models.CharField(max_length=1000, null=True)
    title = models.CharField(max_length=200, null=True)
    short_description = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=3500, null=True)
    tags = models.CharField(max_length=1000, null=True)
    link = models.CharField(max_length=500, null=True)
    class Meta:
        db_table = 'batdongsancom'


class Muabannet(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    page = models.IntegerField(null=False)
    posted_at = models.DateTimeField(null=True)
    title = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=150, null=True)
    exact_location = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=3000, null=False)
    price = models.CharField(max_length=100, null=True)
    user_type = models.CharField(max_length=100, null=True)
    property_name = models.CharField(max_length=500, null=True)
    tags = models.CharField(max_length=1000, null=True)
    direction = models.CharField(max_length=100, null=True)
    bedrooms = models.CharField(max_length=15, null=True)
    toilets = models.CharField(max_length=15, null=True)
    floors = models.CharField(max_length=15, null=True)
    living_size = models.CharField(max_length=15, null=True)
    size = models.CharField(max_length=15, null=True)
    property_legal = models.CharField(max_length=50, null=True)
    link = models.CharField(max_length=500, null=True)
    class Meta:
        db_table = 'muabannet'


class Chotot(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    page = models.IntegerField(null=False)
    posted_at = models.CharField(max_length=50, null=False)
    format_posted_at = models.DateTimeField(null=True)
    title = models.CharField(max_length=200, null=True)
    price = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=3000, null=False)
    user_type = models.CharField(max_length=30, null=True)
    size = models.CharField(max_length=50, null=True)
    direction = models.CharField(max_length=50, null=True)
    property_legal = models.CharField(max_length=50, null=True)
    pricem2 = models.CharField(max_length=30, null=True)
    block = models.CharField(max_length=200, null=True)
    land_type = models.CharField(max_length=50, null=True)
    commercial_type = models.CharField(max_length=50, null=True)
    house_type = models.CharField(max_length=50, null=True)
    apartment_type = models.CharField(max_length=50, null=True)
    length = models.CharField(max_length=10, null=True)
    width = models.CharField(max_length=10, null=True)
    bedrooms = models.CharField(max_length=30, null=True)
    toilets = models.CharField(max_length=30, null=True)
    living_size = models.CharField(max_length=30, null=True)
    floors = models.CharField(max_length=30, null=True)
    furniture = models.CharField(max_length=100, null=True)
    tags = models.CharField(max_length=1000, null=True)
    link = models.CharField(max_length=500, null=True)
    json_data = models.CharField(max_length=10000, null=False)
    class Meta:
        db_table = 'chotot'

class Estate_Tags(models.Model):
    id = models.AutoField(primary_key=True)
    _type = models.CharField(max_length=30, null=True)
    content = models.CharField(max_length=200, null=True)
    table_name = models.CharField(max_length=100, null=True)
    post_id = models.IntegerField(null=True)
    class Meta:
        db_table = 'estate_tags'