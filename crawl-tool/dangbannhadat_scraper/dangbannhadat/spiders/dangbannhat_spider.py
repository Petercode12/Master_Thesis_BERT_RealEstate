import scrapy
import os
from urllib.parse import urljoin
import json
import calendar
from dateutil import parser
from ..ultis import *
import re
import csv

class DangBanNhaDatSpider(scrapy.Spider):
    
    name = 'dangbannhadat'
    global one_connection
    connection = one_connection
    cursor = connection.cursor()
    
    # times_table = queryTimes(connection)
    # time of statistic chart
    # time_now = str(datetime.datetime.now().timestamp())
    
    website = 'dangbannhadat.vn/nha-dat-ban-binh-duong'
    website_type = 'dang_ban_nha_dat'
    
    i = 0

    def __init__(self, end_page='200', auto=True, **kwargs):
        self.auto = auto
        self.url = "https://dangbannhadat.vn/nha-dat-ban-binh-duong" 
        self.end_page = int(end_page)
        # self.crawled_num_post = {i:0 for i in range(1, 25)}
        
        
        super().__init__(**kwargs)

    def start_requests(self):
        for i in range(1, 1 + self.end_page):
                # self.crawled_num_post += 1
                yield scrapy.Request(self.url + "/" + str(i) + "/?order=NgayDang-desc" , callback=self.parse_links, meta={
              "download_timeout": 10,
              "max_retry_time": 1,
            #   "page" : i,
              "auto": self.auto
            })

        
    def parse_links(self, response):
        links = response.xpath('//li/a[@rel="canonical"]/@href').getall()
        # if not auto:
        #     self.crawled_num_post[response.meta["search_keyword"]] += len(links)

        def preprocess(links):
            return urljoin(self.url, link)
        
        for link in links:
            link = preprocess(link)
            yield scrapy.Request(link, callback=self.parse_content1, meta=response.meta)
            
            # with open(os.path.dirname(__file__) + '/../../data/url.txt', 'a') as f:
            #     f.write(link)
            #     f.write('\n')
            #     f.close()
        
    def parse_content1(self, response):

        try :
            json_data = getLinkData(self, response.meta, response.url)

            pattern = re.compile('(\<.*?\>)|\t|\r|\n')
            json_data['id'] = response.xpath('//*[@id="ContentPlaceHolder1_ProductDetail1_divprice"]/div/span[1]/text()').getall()[0]
            json_data["post_title"] = re.sub(pattern,'', response.xpath('//div[@class = "product-detail"]/h1').get()).strip()
            json_data['type'] = ''.join(response.xpath('//*[@id="ContentPlaceHolder1_ProductDetail1_divlocation"]/a/text()').getall())
            json_data["description"] = re.sub(pattern,'', response.xpath('//div[@class = "pd-desc-content"]').get()).strip()
            json_data["price_with_unit"] = re.sub(pattern,'', response.xpath('//span[@class="spanprice"]').get()).strip()
            
            a = re.sub(pattern,'', response.xpath('//*[@id="ContentPlaceHolder1_ProductDetail1_divprice"]/span[2]').get()).strip()
            try :
                json_data['area'] = re.findall('[0-9\.]+', a)[0]
            except Exception:
                pass
            
            n = response.xpath('//*[@id="tbl2"]//td').getall()[1].replace('\t', '').replace('\n', '').replace('\r', '')
            json_data["post_author"] = re.findall('b\>(.*?)\</b\>', n)[0]

            json_data["phone_number"] = re.findall('[0-9]+', response.xpath('//*[@id="tbl2"]//td').getall()[3])[0]

            address = re.sub(pattern, '',response.xpath('//div[@id="ContentPlaceHolder1_ProductDetail1_divlocation"]').get())
            json_data['address'] = re.split("tại", address)[1].strip()

            json_data['post_time'] = re.sub(pattern,'', response.xpath('//*[@id="ContentPlaceHolder1_ProductDetail1_divprice"]/div/span[2]').get()).strip()[11:]

            print(json_data['post_time'])
            if json_data['post_time'] == 'Hôm nay':
                d = datetime.utcnow().replace(tzinfo=pytz.utc)
                json_data['post_time'] = int(datetime(d.year, d.month, d.day).timestamp())

            elif json_data['post_time'] == 'Hôm qua':
                d = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(days=1)
                json_data['post_time'] = int(datetime(d.year, d.month, d.day).timestamp())

            elif json_data['post_time'] == 'Hôm kia':
                d = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(days=2)
                json_data['post_time'] = int(datetime(d.year, d.month, d.day).timestamp())

            else :
                d = parser.parse(json_data['post_time'])
                json_data['post_time'] = int(datetime(d.year, d.month, d.day).timestamp())
            
            print(json_data['post_time'])
            content = DangBanNhaDatContent(self.website, response)
            content.update(json_data)
            insertOne(content.json(), self.connection, 'app_dangbannhadat_scraper')

            with open(os.path.dirname(__file__) + '/../../data/data_dangbannhadat.csv', 'a', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(json_data.values())
        except Exception as e:
            print(traceback.format_exc())


    
