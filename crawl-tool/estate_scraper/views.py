import random
import regex as re
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
import subprocess
from django.db.models import Count
import json
from estate_scraper.models import Batdongsancom, Chotot, Estate_Tags, Muabannet
from estate_scraper.repository.chotot import chotot_scraper
from estate_scraper.repository.muabannet import muabannet_scraper
from estate_scraper.repository.batdongsandotcom import batdongsancom_scraper
# Real estate scrapper


@login_required(login_url='login')
def real_estate_index(request):
    context = {}
    context['segment'] = 'index'
    html_template = loader.get_template('real-estate-scrapper.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url='login')
def real_estate_get_data(request):
    if request.method == "POST":
        if request.POST['option'] == 'chotot':
            chotot_scraper(int(request.POST['start_page']), int(request.POST['end_page']))
            return JsonResponse({'success': True})
        elif request.POST['option'] == 'muabannet':
            muabannet_scraper(int(request.POST['start_page']), int(request.POST['end_page']))
            return JsonResponse({'success': True})
        elif request.POST['option'] == 'batdongsandotcom':
            batdongsancom_scraper(int(request.POST['start_page']), int(request.POST['end_page']))
            return JsonResponse({'success': True})


def show_chotot_data(request):
    if request.method == "GET":
        data = Chotot.objects.values_list('id', 'format_posted_at', 'title', 'price', 'size', 'property_legal', 'description', 'link')
        data = list(data)
        return JsonResponse(data[0:100], safe=False)


def show_muabannet_data(request):
    if request.method == "GET":
        data = Muabannet.objects.values_list('id', 'posted_at', 'title', 'location', 'price', 'size', 'property_legal','description', 'link')
        data = list(data)
        return JsonResponse(data[0:100], safe=False)



def show_batdongsancom_data(request):
    if request.method == "GET":
        data = Batdongsancom.objects.values_list('id', 'posted_at', 'post_rank', 'price', 'size', 'title', 'description', 'link')
        data = list(data)
        return JsonResponse(data[0:100], safe=False)


def parsing_data(request):
    if request.method == "POST":
        Estate_Tags.objects.all().delete()
        # Parsing chotot
        chotot_data = Chotot.objects.values_list('id', 'json_data')
        chotot_tags_list = []
        for data in chotot_data:
            try:
                json_data = data[1].strip("'<>() ").replace('\'', '\"').replace('True', '"True"').replace(
                    'False', '"False"').replace('None', '"None"').replace('\\', '')
                json_data = json.loads(json_data)
                for param in json_data['adInfo']['parameters']:
                    if param['id'] == 'area':
                        area = param['value']
                        chotot_tags_list.append(Estate_Tags(
                            _type='area', content=area, table_name='chotot', post_id=data[0]))
            except Exception as e:
                print(e)
        Estate_Tags.objects.bulk_create(chotot_tags_list)

        # Parsing muabannet
        muabannet_data = Muabannet.objects.values_list('id', 'location')
        muabannet_tags_list = []
        for data in muabannet_data:
            try:
                if data[1] is not None:
                    location = re.findall("(.*?) -", data[1])
                    muabannet_tags_list.append(Estate_Tags(
                        _type='area', content=location[0], table_name='muabannet', post_id=data[0]))
            except Exception as e:
                print(e)
        Estate_Tags.objects.bulk_create(muabannet_tags_list)

        # Parsing batdongsancom
        batdongsancom_data = Batdongsancom.objects.values_list(
            'id', 'detail_header')
        batdongsancom_tags_list = []
        for data in batdongsancom_data:
            try:
                detail_header = data[1].split('>')
                batdongsancom_tags_list.append(Estate_Tags(
                    _type='area', content=detail_header[2], table_name='batdongsancom', post_id=data[0]))
            except Exception as e:
                print(e)
        Estate_Tags.objects.bulk_create(batdongsancom_tags_list)
        return JsonResponse({'success': True})


def get_chart_data(request):
    if request.method == "GET":
        raw_data = Estate_Tags.objects.values('content').annotate(
            count=Count('content')).order_by('-count')

        raw_data = [field for field in raw_data]
        data = []
        labels = []
        background_color = []
        for i in range(0, len(raw_data)):
            data.append(raw_data[i]['count'])
            labels.append(raw_data[i]['content'])
            background_color.append('rgba({r}, {g}, {b}, 0.5)'.format(r=random.randint(0, 255),g=random.randint(0, 255),b=random.randint(0, 255)))
        return JsonResponse({"labels": labels, "datasets": [{"data": data, "backgroundColor": background_color}]}, safe=False)
