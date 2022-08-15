from ..ultis import *
import re
import csv


class AnCuSpider(scrapy.Spider):
    # Tên bot quét
    name = 'ancu'

    # Lấy kết nối tổng để đảm bảo chỉ có 1 connection đến PostgreSQL, tránh được việc quá tải nhiều yêu cầu truy xuất khi quét đa luồng
    global one_connection
    connection = one_connection
    cursor = connection.cursor()
    
    website = 'ancu.net'
    website_type = 'real_estate'
    url_type = 'mua-ban-nha-dat-tinh-binh-duong' 
    # get time of the most recent post of each type of job
    # times_table = queryTimes(connection)
    # #time of statistic chart
    # time_now = str(datetime.datetime.now().timestamp())
    ## Statistic
    

    def __init__(self, end_page='200',auto=True, **kwargs):
        self.auto = auto
        self.url = "https://ancu.me/mua-ban-nha-dat-tinh-binh-duong" 
        self.end_page = int(end_page)
        super().__init__(**kwargs)

    def start_requests(self):
        for i in range(1, 1 + self.end_page):
                # self.crawled_num_post += 1
                yield scrapy.Request(self.url + "/t" + str(i) , callback=self.parse_links, meta={
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
        links = response.xpath('/html/body/div[5]/div/div[1]/div[4]/div/ul/li/a/@href').getall()
        # if not auto:
        #     self.crawled_num_post[response.meta["search_keyword"]] += len(links)

        def preprocess(links):
            return urljoin(self.url, link)
        
        for link in links:
            yield scrapy.Request(link, callback=self.parse_content, meta=response.meta)
        
    # def save(self, response):
    #     json_data = getLinkData(self, response.meta, response.url, response.meta["crawling_type"])
    #     insertOne(json_data, self.connection)
    

    def parse_content(self, response):
        """
        Trang này có thể dùng mã javascript của nó để truy xuất thông tin thay vì XPath.
        """
        try :
            json_data = getLinkData(self, response.meta, response.url)
            extra_info = response.xpath('//div[@class="extra-info"]//li/text()').getall()
            pattern = re.compile('(\<.*?\>)|\t|\r|\n')
            json_data['id'] = int(extra_info[1])
            json_data['post_time'] = int(datetime.datetime.strptime(extra_info[3].strip(), "%d/%m/%Y").timestamp())


            json_data["post_title"] = response.xpath('/html/body/div[5]/div/div[1]/article/h1/text()').get()

            user_info = response.xpath('//table//td/text()').getall()
            json_data['type'] = user_info[1]
            json_data["post_author"] = user_info[3]
            json_data["phone_number"] = user_info[5]

            json_data["description"] = re.sub(pattern,'', response.xpath('/html/body/div[5]/div/div[1]/article/div[1]').get()).strip()
            json_data["price_with_unit"] = response.xpath('/html/body/div[5]/div/div[1]/article/ul[2]/li[1]/span[1]/text()').get().strip()
            
            a = response.xpath('/html/body/div[5]/div/div[1]/article/ul[2]/li[1]/span[2]/text()').get()
            json_data['area'] = re.findall('[0-9\.]+', a)[0]
            
            
            json_data['address'] = response.xpath('/html/body/div[5]/div/div[1]/article/ul[2]/li[2]/strong/text()').get().replace("Địa chỉ: ", "").strip()
            
            json_data['coordinate'] = '0, 0'

            for i in response.xpath('//script').getall():
                if '<script>\n    var estate_lat' in str(i):
                    lat = re.findall('lat = (.*);', i)[0]
                    lon = re.findall('lon = (.*);', i)[0]
                    json_data['coordinate'] = lat + ', ' + lon
            
            
            content = AnCuContent(self.website, response)
            content.update(json_data)
            insertOne(content.json(), self.connection, 'app_ancu_scraper')

            with open(os.path.dirname(__file__) + '/../data/data_ancu.csv', 'a', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(json_data.values())

        except Exception as e:
            print(e)

