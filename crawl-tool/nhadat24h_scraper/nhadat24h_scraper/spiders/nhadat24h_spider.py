from ..ultis import *
import re
import csv


class NhaDat24hSpider(scrapy.Spider):
    # Tên bot quét
    name = 'nhadat24h'

    # Lấy kết nối tổng để đảm bảo chỉ có 1 connection đến PostgreSQL, tránh được việc quá tải nhiều yêu cầu truy xuất khi quét đa luồng
    global one_connection
    connection = one_connection
    cursor = connection.cursor()
    
    website = 'nhadat24h.net'
    website_type = 'nhadat24h'
    url_type = 'nha-dat-binh-duong' 
    # get time of the most recent post of each type of job
    # times_table = queryTimes(connection)
    #time of statistic chart
    time_now = str(datetime.datetime.now().timestamp())
    ## Statistic
    

    def __init__(self, end_page='200',auto=True, **kwargs):
        self.auto = auto
        self.url = "https://nhadat24h.net/nha-dat-binh-duong/" 
        self.end_page = int(end_page)
        
        super().__init__(**kwargs)

    def start_requests(self):
        for i in range(1, 1 + self.end_page):
                # self.crawled_num_post += 1
                yield scrapy.Request(self.url + "page" + str(i), callback=self.parse_links, meta={
              "download_timeout": 10,
              "max_retry_time": 1,
            #   "page" : i,
              "auto": self.auto
            })

            
        # print(self.crawled_num_post)
        # self.save_num_post()

    # def parse(self, response):
    #     for i in range(1,5):
    #         yield scrapy.Request(self.url + '/' + response.meta['url_type'] + "?page=" + str(i), callback=self.parse_links, meta=response.meta)
    
    def parse_links(self, response):
        links = response.xpath('//a[@class="a-title"]/@href').getall()
        # if not auto:
        #     self.crawled_num_post[response.meta["search_keyword"]] += len(links)

        def preprocess(links):
            return urljoin(self.url, link)
        
        for link in links:
            link = preprocess(link)
            yield scrapy.Request(link, callback=self.parse_content, meta=response.meta)
            # print(link)
        
    # def save(self, response):
    #     json_data = getLinkData(self, response.meta, response.url, response.meta["crawling_type"])
    #     insertOne(json_data, self.connection)
    
    def _get_javascript_data(self, response):
        all_data = {}
        for script in response.xpath("//script").getall():
            if '<script type="application/ld json">' in str(script):
                all_data.update(dict(json.loads(script.split('<script type="application/ld json">')[1].split('</script>')[0])))

            if '<script type="application/ld+json">' in str(script):
                all_data.update(dict(json.loads(script.split('<script type="application/ld+json">')[1].split('</script>')[0])))
                
        data = all_data["itemListElement"]
        return all_data, data

    def parse_content(self, response):
        try :
            all_data, data = self._get_javascript_data(response)

            json_data = getLinkData(self, response.meta, response.url)
            
            pattern = re.compile('(\<.*?\>)|\t|\r|\n')
            table = []
            for c in response.xpath('//div[@class="dv-tb-tsbds"]//tr//td[2]').getall(): 
                table.append(re.sub(pattern, '', c).strip())

            json_data['id'] = int(table[-1])

            json_data["post_title"] = all_data["name"]

            json_data['type'] = data[1]['item']['name'] + " - " + data[2]['item']['name']
            json_data["post_author"] = response.xpath('//label[@class="fullname"]/a/text()').get().replace('\n', '')
            json_data["phone_number"] = response.xpath('//*[@id="viewmobinumber"]/text()').get().strip().replace('.', '')

            json_data["description"] = re.sub(pattern,'', response.xpath('//*[@id="ContentPlaceHolder1_Panel1"]').get()).strip()
            json_data["price_with_unit"] = response.xpath('//label[@class="lb-pri-dt"]//label/text()').get() + " " + response.xpath('//label[@class="lb-pri-dt"]/text()').getall()[1].replace("-", "").strip()
            json_data['legal'] = response.xpath('//div[@class="dv-time-dt"]//strong/text()').get()
            json_data['area'] = response.xpath('//label[@class="lb-pri-dt"]//label/text()').getall()[1]
            
            json_data['address'] = response.xpath('//label[@class="lb-pri-dt"]/text()').getall()[-1]

            json_data['bedroom'] = table[0] if table[0]!='' else '0'
            json_data['bathroom'] = table[1] if table[1]!='' else '0'
            json_data['floors'] = re.findall('[0-9\.]+', table[2])[0] if table[2]!='' else '0'
            json_data["phone_number"] = response.xpath('//*[@id="viewmobinumber"]/text()').get().strip().replace('.', '')
            content = NhaDat24hContent(self.website, response)
            content.update(json_data)
            insertOne(content.json(), self.connection, 'app_nhadat24h_scraper')

            with open(os.path.dirname(__file__) + '/../../data/data_nhadat24h.csv', 'a', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(json_data.values())
        except Exception as e:
            print(str(traceback.format_exc()))

    # def save_num_post(self):
        
    #     save_statistic(self.time_now, self.crawled_num_post, self.connection)
