from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
import regex as re
import django
django.setup()
from ..models import Batdongsancom
import time
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--headless")

# For ChromeDriver version 79.0.3945.16 or over
options.add_argument('--disable-blink-features=AutomationControlled')

def batdongsancom_scraper(start, end):
    for page in range(start, end):
        driver = webdriver.Remote("http://host.docker.internal:4444/wd/hub")
        driver.get('https://batdongsan.com.vn/nha-dat-ban/p' + str(page))
        links = []
        for element in driver.find_elements(By.CSS_SELECTOR,
                                            'a.js__product-link-for-product-id'):
            links.append(str(element.get_attribute('href')))

        driver.close()

        try:
            for i, link in enumerate(links):
                driver = webdriver.Remote("http://host.docker.internal:4444/wd/hub")
                driver.get(link)

                short_description = driver.find_elements(By.XPATH,
                                                            '/html/body/div[4]/div/div[1]/div[1]/div[3]/span')
                if(len(short_description) > 0):
                    short_description = str(short_description[0].text)
                else:
                    short_description = None

                description = driver.find_elements(By.XPATH,
                                                    '//*[@id="product-detail-web"]/div[2]/div[1]')
                if(len(description) > 0):
                    description = str(description[0].text)
                else:
                    description = None

                price_ext = driver.find_elements(
                    By.XPATH, '/html/body/div[4]/div/div[1]/div[1]/div[3]/div[1]/div[1]/span[3]')
                if len(price_ext) > 0:
                    price_ext = price_ext[0].text
                else:
                    price_ext = ''

                size_ext = driver.find_elements(
                    By.XPATH, '/html/body/div[4]/div/div[1]/div[1]/div[3]/div[1]/div[2]/span[3]')
                if len(size_ext) > 0:
                    size_ext = size_ext[0].text
                else:
                    size_ext = ''

                tags_title = driver.find_elements(By.CSS_SELECTOR, 'span.title')
                tags_value = driver.find_elements(By.CSS_SELECTOR, 'span.value')
                posted_at = ''
                expired_at = ''
                post_rank = ''
                post_number = ''
                price = ''
                size = ''
                house_type = ''
                direction = ''
                floors = ''
                location = ''
                balcony_direction = ''
                bedrooms=bedrooms = ''
                toilets = ''
                furniture = ''
                property_legal = ''
                street_in = ''
                street = ''
                detail_header = ''
                tags = ''
                for index, title in enumerate(tags_title):
                    if re.search('Ngày đăng', title.text):
                        posted_at = tags_value[index].text
                    elif re.search('Ngày hết hạn', title.text):
                        expired_at = expired_at + tags_value[index].text
                    elif re.search('Loại tin', title.text):
                        post_rank = post_rank + '$' + tags_value[index].text
                    elif re.search('Mã tin', title.text):
                        post_number = post_number + '$' + tags_value[index].text
                    elif re.search('Mức giá', title.text):
                        price = price + '$' + \
                            tags_value[index].text + '$' + price_ext
                    elif re.search('Diện tích', title.text):
                        size = size + '$' + tags_value[index].text + '$' + size_ext
                    elif re.search('Loại tin đăng', title.text):
                        house_type = house_type + '$' + tags_value[index].text
                    elif re.search('Hướng nhà', title.text):
                        direction = direction + '$' + tags_value[index].text
                    elif re.search('Số tầng', title.text):
                        floors = floors + '$' + tags_value[index].text
                    elif re.search('Địa chỉ', title.text):
                        location = location + '$' + tags_value[index].text
                    elif re.search('Hướng ban công', title.text):
                        balcony_direction = balcony_direction + \
                            '$' + tags_value[index].text
                    elif re.search('Số phòng ngủ', title.text):
                        bedrooms=bedrooms = bedrooms=bedrooms + '$' + tags_value[index].text
                    elif re.search('Số toilet', title.text):
                        toilets = toilets + '$' + tags_value[index].text
                    elif re.search('Nội thất', title.text):
                        furniture = furniture + '$' + tags_value[index].text
                    elif re.search('Pháp lý', title.text):
                        property_legal = property_legal + \
                            '$' + tags_value[index].text
                    elif re.search('Đường vào', title.text):
                        street_in = street_in + '$' + tags_value[index].text
                    elif re.search('Mặt tiền', title.text):
                        street = street + '$' + tags_value[index].text

                for index, title in enumerate(tags_title):
                    tags = tags + '$' + title.text + ': ' + tags_value[index].text
                headers = driver.find_elements(By.CSS_SELECTOR, 'a.re__link-se')
                detail_header = ''
                if len(headers) > 0:
                    for header in headers:
                        detail_header = detail_header + header.text + '>'
                title = driver.find_elements(
                    By.XPATH, '/html/body/div[4]/div/div[1]/div[1]/div[3]/h1')
                if(len(title) > 0):
                    title = str(title[0].text)
                else:
                    title = None

                driver.close()
                Batdongsancom(page=page, posted_at=datetime.strptime(posted_at, '%d/%m/%Y'), 
                                expired_at=datetime.strptime(expired_at, '%d/%m/%Y'), post_rank=post_rank,
                                post_number=post_number, price=price, size=size, house_type=house_type,
                                direction=direction, floors=floors, location=location, 
                                balcony_direction=balcony_direction, bedrooms=bedrooms, toilets=toilets, 
                                furniture=furniture, property_legal=property_legal, street_in=street_in,
                                street=street, detail_header=detail_header, title=title,
                                short_description=short_description, description=description,tags=tags, link=link).save()
                print(page, ': ', link)

            driver.close()
        except ZeroDivisionError as err:
            logger.error(err)
            print(err)


