import scrapy
import os
from urllib.parse import urljoin
import json
import calendar
from dateutil import parser
from ..ultis import *
import re
import csv

class MuabanSpider(scrapy.Spider):
    
    name = 'muaban'
    global one_connection
    connection = one_connection
    cursor = connection.cursor()
    
    # times_table = queryTimes(connection)
    #time of statistic chart
    time_now = str(datetime.datetime.now().timestamp())
    
    website = 'muaban.net/bat-dong-san/'
    website_type = 'mua_ban'
    types = ['cho-thue-nha-dat-binh-duong', 'ban-nha-dat-chung-cu-binh-duong']
    
    i = 0

    def __init__(self, search_keyword='', end_page='1000', estate_type = [], auto=True, **kwargs):
        self.auto = auto
        self.url = "https://www.muaban.net/bat-dong-san/" 
        self.search_keywords = search_keyword.split(',')
        self.end_page = int(end_page)
        self.types = ['cho-thue-nha-dat-binh-duong', 'ban-nha-dat-chung-cu-binh-duong']
        self.estate_type = self.types if len(estate_type) == 0 else estate_type
        
        super().__init__(**kwargs)

    def start_requests(self):
        for p in range(1, self.end_page + 1, 5):
            for t in self.types: 
                x = self.url + "/" + t + "?q=" + "&sort=1" + "#page=" + str(p)
                yield scrapy.Request(url = x, callback=self.parse_links, meta={
              "download_timeout": 10,
              "max_retry_time": 1,
            #   "page" : i,
            #   "search_keyword": k,
              "auto": self.auto
            })


    # def parse(self, response):
    #     for i in range(1,5):
    #         yield scrapy.Request(self.url + '/' + response.meta['estate_type'] + "?page=" + str(i), callback=self.parse_links, meta=response.meta)
    
    def parse_links(self, response):
        links = response.xpath('//div[@class="sc-q9qagu-10 cpTfDV"]/a/@href').getall()
        # if not auto:
        #     self.crawled_num_post[response.meta["search_keyword"]] += len(links)

        def preprocess(link):
            return urljoin(self.url, link)
        
        for link in links:
            link = preprocess(link)

            # with open(os.path.dirname(__file__) + '/../../url.txt', 'a') as f:
            #     f.write(link)
            #     f.write('\n')
            #     f.close()
            print("ssssssssssssssssssssssssssssssssssssssssssssss")
            yield scrapy.Request(link, callback=self.parse_content, meta=response.meta)
            
            
        


    # def save(self, response):
    #     json_data = getLinkData(self, response.meta, response.url, response.meta["crawling_type"])
    #     insertOne(json_data, self.connection)
    
    def parse_content1(self, response):
        data = self._get_javascript_data(response)


    def _get_javascript_data(self, response):
        all_data = {}
        for script in response.xpath("//script").getall():
            if '<script id="__NEXT_DATA__" type="application/json">' in str(script):
                all_data = json.loads(script.split('<script id="__NEXT_DATA__" type="application/json">')[1].split('</script>')[0])
                break
        data = all_data["props"]["pageProps"]["initialProps"]["detail"]

        self.i +=1 
        return data

    def parse_content(self, response):
        """
        Trang này có thể dùng mã javascript của nó để truy xuất thông tin thay vì XPath.
        """
        
        try:
            data = self._get_javascript_data(response)
            json_data = getLinkData(self, response.meta, response.url)

            parse_time = parser.isoparse(data["publish_at"].replace("T", " "))
            json_data["post_time"] = calendar.timegm(parse_time.utctimetuple())
            json_data["type"] = data["parameters"][0]["value"]
            json_data["id"] = data["id"]
            json_data["post_title"] = data.get("title", ' ')
            json_data["post_author"] = data["contact_name"]
            json_data["description"] = data.get("body", ' ').strip().replace("'"," ").replace('"',' ').replace(",",";").replace("<br />", "")
            json_data["price"] = data.get("price", "")
            json_data["price_with_unit"] = data.get("price_display")
            json_data["phone_number"] = data.get("phone", ' ')
            
            json_data["address"] = data.get("address", "")
            json_data["location"] = data.get("location")

            json_data["land_area"] = "0"
            json_data["bedroom"] = "0"
            json_data["bathroom"] = "0"
            json_data["floors"] = "0"
            json_data["land_area"] = "0"
            json_data["legal"] = "0"

            for x in data["parameters"][1:]:
                k = re.findall( r"[a-z-]+" ,x["icon"])[1].replace("-", "_")
                val = re.findall( r"[0-9]+" ,x["value"])

                if k in json_data.keys():
                    if len(val) > 0:
                        json_data[k] = val[0]

                    else:
                        json_data[k] = x["value"]

            json_data["search_keywords"] = response.meta.get("search_keyword", "")
            if json_data["search_keywords"] == '':
                json_data["search_keywords"] = json_data["type"]

            content = MuaBanContent(self.website, response)
            content.update(json_data)
            insertOne(content.json(), self.connection, 'app_muabannet_scraper')

            with open(os.path.dirname(__file__) + '/../data/data_muaban.csv', 'a', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(json_data.values())


        except Exception as e:
            print(str(traceback.format_exc()))

    # # def save_num_post(self):
        
    # #     save_statistic(self.time_now, self.crawled_num_post, self.connection)

