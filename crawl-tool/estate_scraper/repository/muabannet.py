from datetime import datetime, timezone
import re
import logging
import requests
import lxml.html as lh
from bs4 import BeautifulSoup
import argparse
import django
django.setup()
from ..models import Muabannet
import regex as re

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

def muabannet_scraper(start, end):
    try:
        for page in range(start, end):
            html = requests.get(
                'https://muaban.net/mua-ban-nha-dat-cho-thue-toan-quoc-l0-c3?cp=' + str(page))

            soup = BeautifulSoup(html.text, "lxml")

            links = []
            posted_at = []
            for element in soup.select('a.list-item__link'):
                links.append(str(element['href']))

            for element in soup.select('span.list-item__date'):
                posted_at.append(element.text)

            muabannet_list = []
            for i, link in enumerate(links):
                html = requests.get(link)
                doc = lh.fromstring(html.text)
                soup = BeautifulSoup(html.text, "lxml")

                title = doc.xpath('/html/body/main/div[2]/div[1]/h1')
                if(len(title) > 0):
                    title = str(title[0].text_content())
                else:
                    title = None

                location = doc.xpath('/html/body/main/div[2]/div[1]/div[3]/span[1]')
                if(len(location) > 0):
                    location = str(location[0].text_content())
                else:
                    location = None

                exact_location = doc.xpath(
                    '/html/body/main/div[2]/div[1]/div[7]/div[1]/div[2]')
                if(len(exact_location) > 0):
                    exact_location = str(exact_location[0].text_content())
                else:
                    exact_location = None

                price = doc.xpath('/html/body/main/div[2]/div[1]/div[2]')
                if(len(price) > 0):
                    price = str(price[0].text_content())
                else:
                    price = None

                description = doc.xpath('/html/body/main/div[2]/div[1]/div[5]')
                if(len(description) > 0):
                    description = str(description[0].text_content())
                else:
                    description = None

                user_type = doc.xpath(
                    '/html/body/main/div[2]/div[1]/div[4]/div/div[1]')
                if(len(user_type) > 0):
                    user_type = str(user_type[0].text_content())
                else:
                    user_type = None

                property_name = soup.select('span[property="name"]')
                if(len(property_name) > 0):
                    property_name = ''.join([str(x.text) + '>' for x in property_name])
                else:
                    property_name = None

                tags = soup.select('div.tech-item')
                tags = ''.join([str(x.text) + "$" for x in tags])

                tag_name = soup.select('div.tech-item__name')

                tag_value = soup.select('div.tech-item__value')

                direction = ''
                bedrooms = ''
                toilets = ''
                living_size = ''
                size = ''
                floors = ''
                property_legal = ''
                if(len(tag_name) > 0 and len(tag_name) == len(tag_value)):
                    for i in range(len(tag_name)):
                        if(tag_name[i].text == 'Hướng:'):
                            direction = tag_value[i].text
                        elif(tag_name[i].text == 'Phòng ngủ:'):
                            bedrooms = tag_value[i].text
                        elif(tag_name[i].text == 'Phòng tắm:'):
                            toilets = tag_value[i].text
                        elif(tag_name[i].text == 'Diện tích sử dụng:'):
                            living_size = tag_value[i].text
                        elif(re.search('Diện tích đất:', tag_name[i].text)):
                            size = tag_value[i].text
                        elif(re.search('Tầng/Lầu:', tag_name[i].text)):
                            floors = tag_value[i].text
                        elif(re.search('Pháp lý:', tag_name[i].text)):
                            property_legal = tag_value[i].text
                muabannet_list.append(Muabannet(page=page, title=title, location=location,
                                                exact_location=exact_location, description=description,
                                                price=price, posted_at=datetime.strptime(re.sub('[^z0-9-/]+', '', posted_at[i]), '%d/%m/%Y').replace(tzinfo=timezone.utc), 
                                                user_type=user_type, property_name=property_name, tags=tags,
                                                direction=direction, bedrooms=bedrooms, toilets=toilets,
                                                floors=floors, living_size=living_size, property_legal=property_legal,
                                                size=size, link=link))
            Muabannet.objects.bulk_create(muabannet_list)
            print('Page: ' + str(page) + ' is done')

    except ZeroDivisionError as err:
        # logger.error(err)
        print(err)
