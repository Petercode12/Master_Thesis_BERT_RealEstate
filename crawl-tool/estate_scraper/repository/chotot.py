import logging
import re
import lxml.html as lh
from bs4 import BeautifulSoup
import json
import requests
import django
django.setup()
from ..models import Chotot
import datetime

def parsedatetime(str_val):

    parts = str_val.split(' ')

    if str_val == 'hôm qua':
        return datetime.timedelta(days=1)

    if len(parts) < 3 and parts[2] != 'trước':
        raise Exception("can't parse %s" % str_val)

    try:
        interval = int(parts[0])
    except ValueError as e:
        raise Exception("can't parse %s" % str_val)

    desc = parts[1]

    if 'giây' in desc:
        td = datetime.timedelta(seconds=interval)
    elif 'phút' in desc:
        td = datetime.timedelta(minutes=interval)
    elif 'giờ' in desc:
        td = datetime.timedelta(minutes=interval*60)
    elif 'ngày' in desc:
        td = datetime.timedelta(days=interval)
    elif 'tuần' in desc:
        td = datetime.timedelta(weeks=interval)
    elif 'tháng' in desc:
        td = datetime.timedelta(weeks=interval)
    else:
        raise Exception("cant parse %s" % str_val)
    return td

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

def chotot_scraper(start, end):
    try:
        for page in range(start, end):
            html = requests.get(
                'https://nha.chotot.com/mua-ban-bat-dong-san?page=' + str(page) + '&sp=0')
            soup = BeautifulSoup(html.text, "lxml")

            links = []
            for element in soup.select('a.AdItem_adItem__2O28x'):
                links.append('https://nha.chotot.com' + element['href'])
            chotot_list = []
            for i, link in enumerate(links):
                html = requests.get(link)
                doc = lh.fromstring(html.text)
                soup = BeautifulSoup(html.text, "lxml")
                json_data = soup.find('script', {'type': "application/json"})
                data = json.loads(json_data.text)
                json_data = data['props']['initialState']['adView']
                format_posted_at = datetime.datetime.now() - parsedatetime(json_data['adInfo']['ad']['date'])
                json_data = str(json_data)

                title = doc.xpath(
                    '/html/body/div[1]/div/div[3]/div[1]/div/div[4]/div[2]/h1')
                if(len(title) > 0):
                    title = str(title[0].text_content())
                else:
                    title = None

                price = doc.xpath(
                    '/html/body/div[1]/div/div[3]/div[1]/div/div[4]/div[2]/div[1]/div[1]/span/div/span/span/span[1]')
                if(len(price) > 0):
                    price = str(price[0].text_content())
                else:
                    price = None

                description = doc.xpath(
                    '/html/body/div[1]/div/div[3]/div[1]/div/div[4]/div[2]/p')
                if(len(description) > 0):
                    description = str(description[0].text_content())
                else:
                    description = None

                user_type = doc.xpath(
                    '/html/body/div[1]/div/div[3]/div[1]/div/div[6]/div/div[2]/div[1]/div/div/div[1]/div')
                if(len(user_type) > 0):
                    user_type = str(user_type[0].text)
                else:
                    user_type = None

                posted_at = doc.xpath(
                    '/html/body/div[1]/div/div[3]/div[1]/div/div[4]/div[1]/div[2]/span')
                if(len(posted_at) > 0):
                    posted_at = str(posted_at[0].text_content())
                else:
                    posted_at = None

                # formated_posted_at = datetime.datetime.now() - parsedatetime(posted_at)
                size = ''
                direction = ''
                property_legal = ''
                pricem2 = ''
                block = ''
                land_type = ''
                commercial_type = ''
                house_type = ''
                apartment_type = ''
                length = ''
                width = ''
                bedrooms = ''
                toilets = ''
                living_size = ''
                floors = ''
                furniture = ''
                tags = soup.select('div.media-body.media-middle')
                if(len(tags) > 0):
                    for i in tags:
                        if re.search('Diện tích đất: ', i.text):
                            size = size + '$' + \
                                re.sub('Diện tích đất: ', '', i.text)
                        elif re.search('Hướng cửa chính: ', i.text):
                            direction = direction + '$' + \
                                re.sub('Hướng cửa chính: ', '', i.text)
                        elif re.search('Giấy tờ pháp lý: ', i.text):
                            property_legal = property_legal + '$' + \
                                re.sub('Giấy tờ pháp lý: ', '', i.text)
                        elif re.search('Giá/m2: ', i.text):
                            pricem2 = pricem2 + '$' + re.sub('Giá/m2: ', '', i.text)
                        elif re.search('Tên phân khu/Lô/Block/Tháp: ', i.text):
                            block = block + '$' + \
                                re.sub('Tên phân khu/Lô/Block/Tháp: ', '', i.text)
                        elif re.search('Loại hình đất: ', i.text):
                            land_type = land_type + '$' + \
                                re.sub('Loại hình đất: ', '', i.text)
                        elif re.search('Loại hình văn phòng: ', i.text):
                            commercial_type = commercial_type + '$' + \
                                re.sub('Loại hình văn phòng: ', '', i.text)
                        elif re.search('Loại hình nhà ở: ', i.text):
                            house_type = house_type + '$' + \
                                re.sub('Loại hình nhà ở: ', '', i.text)
                        elif re.search('Loại hình căn hộ: ', i.text):
                            apartment_type = apartment_type + '$' + \
                                re.sub('Loại hình căn hộ: ', '', i.text)
                        elif re.search('Chiều dài: ', i.text):
                            length = length + '$' + re.sub('Chiều dài: ', '', i.text)
                        elif re.search('Chiều ngang: ', i.text):
                            width = width + '$' + re.sub('Chiều ngang: ', '', i.text)
                        elif re.search('Số phòng ngủ: ', i.text):
                            bedrooms = bedrooms + '$' + \
                                re.sub('Số phòng ngủ: ', '', i.text)
                        elif re.search('Số phòng vệ sinh: ', i.text):
                            toilets = toilets + '$' + \
                                re.sub('Số phòng vệ sinh: ', '', i.text)
                        elif re.search('Diện tích sử dụng: ', i.text):
                            living_size = living_size + '$' + \
                                re.sub('Diện tích sử dụng: ', '', i.text)
                        elif re.search('Tổng số tầng: ', i.text):
                            floors = floors + '$' + \
                                re.sub('Tổng số tầng: ', '', i.text)
                        elif re.search('Tình trạng nội thất: ', i.text):
                            furniture = furniture + '$' + \
                                re.sub('Tình trạng nội thất: ', '', i.text)
                sum_tag = ''.join([tag.text + '$' for tag in tags])
                chotot_list.append(Chotot(format_posted_at = format_posted_at.replace(tzinfo=datetime.timezone.utc), page=page, title=title, price=price, description=description,
                                        user_type=user_type, posted_at=posted_at, size=size,
                                        direction=direction, property_legal=property_legal,
                                        pricem2=pricem2, block=block, land_type=land_type,
                                        commercial_type=commercial_type, house_type=house_type,
                                        apartment_type=apartment_type, length=length, width=width,
                                        bedrooms=bedrooms, toilets=toilets, living_size=living_size,
                                        floors=floors, furniture=furniture, tags=sum_tag, link=link, json_data=json_data))
            Chotot.objects.bulk_create(chotot_list)
            print('Page ' + str(page) + ' done')
    except Exception as err:
        logger.error(err)
        print(err)
