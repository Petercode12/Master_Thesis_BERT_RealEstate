from ..ultis import *


class VieclamtotlinksSpider(scrapy.Spider):
    # Tên bot quét
    name = 'vieclamtot'

    # Lấy kết nối tổng để đảm bảo chỉ có 1 connection đến PostgreSQL, tránh được việc quá tải nhiều yêu cầu truy xuất khi quét đa luồng
    global one_connection
    connection = one_connection
    cursor = connection.cursor()
    
    website = 'vieclamtot.com'
    website_type = 'viec_lam'
    url_type = 'viec-lam' 
    # get time of the most recent post of each type of job
    times_table = queryTimes(connection)
    #time of statistic chart
    time_now = str(datetime.datetime.now().timestamp())
    ## Statistic
    

    def __init__(self, search_keyword='', end_page='200',auto=True, **kwargs):
        self.auto = auto
        self.url = "https://www.vieclamtot.com/viec-lam" 
        self.search_keywords = search_keyword
        search_keyword = self.search_keywords.split(',')
        end_page = end_page.split(',')

        self.search_keyword_and_page = {i.strip():None for i in search_keyword}
        self.crawled_num_post = {i:0 for i in range(1, 25)}
        
        self.n = len(search_keyword)
        for idx in range(self.n):
            try:
                self.search_keyword_and_page[search_keyword[idx].strip()] = int(end_page[idx])
            except IndexError:
                self.search_keyword_and_page[search_keyword[idx].strip()] = int(end_page[-1])
        super().__init__(**kwargs)

    def start_requests(self):
        for k,p in self.search_keyword_and_page.items():
            for i in range(1, 1 + p):
                # self.crawled_num_post += 1
                yield scrapy.Request(self.url + "?q=" + k + "&page=" + str(i) + "&sp=0", callback=self.parse_links, meta={
              "download_timeout": 10,
              "max_retry_time": 1,
            #   "page" : i,
              "search_keyword": k,
              "auto": self.auto
            })

            
        # print(self.crawled_num_post)
        # self.save_num_post()

    # def parse(self, response):
    #     for i in range(1,5):
    #         yield scrapy.Request(self.url + '/' + response.meta['url_type'] + "?page=" + str(i), callback=self.parse_links, meta=response.meta)
    
    def parse_links(self, response):
        links = response.xpath("//a[@class='AdItem_adItem__2O28x AdItem_adItemJob__1bDVu']/@href").getall()
        # if not auto:
        #     self.crawled_num_post[response.meta["search_keyword"]] += len(links)

        def preprocess(links):
            return urljoin(self.url, link)
        
        for link in links:
            # filter for priorities which might be posted long time ago
            if '[PL-top]' not in link:
                link = preprocess(link)
                yield scrapy.Request(link, callback=self.parse_content, meta=response.meta)
        
    # def save(self, response):
    #     json_data = getLinkData(self, response.meta, response.url, response.meta["crawling_type"])
    #     insertOne(json_data, self.connection)
    

    def _get_javascript_data(self, response):
        all_data = {}
        for script in response.xpath("//script").getall():
            if '<script id="__NEXT_DATA__" type="application/json">' in str(script):
                all_data = json.loads(script.split('<script id="__NEXT_DATA__" type="application/json">')[1].split('</script>')[0])
                break
        data = all_data["props"]["initialState"]["adView"]["adInfo"]["ad"]
        parameters = all_data["props"]["initialState"]["adView"]["adInfo"]["ad_params"]
        project = all_data["props"]["initialState"]["adView"]["adInfo"]
        return data, parameters, project

    def parse_content(self, response):
        """
        Trang này có thể dùng mã javascript của nó để truy xuất thông tin thay vì XPath.
        """
        
        try:
            data, parameters, project = self._get_javascript_data(response)
            json_data = getLinkData(self, response.meta, response.url)
            json_data["job_id"] = data["job_type"]
            json_data["post_time"] = int(int(data["list_time"])/1000)
            idx, val = int(json_data["job_id"]), json_data["post_time"]
            
            if self.times_table[idx] is None or (self.times_table[idx] is not None and int(self.times_table[idx]) < val):
                # json_data = {}
                self.crawled_num_post[idx] += 1
                json_data["post_title"] = data.get("subject", ' ').replace("'"," ").replace('"',' ')
                json_data["post_author"] = data["reviewer_nickname"]
                json_data["full_description"] = data.get("body", ' ').strip().replace("'"," ").replace('"',' ').replace(",",";")
                json_data["vacancies"] = data.get("vacancies")
                json_data["salary_with_unit"] = data.get("price_string")
                json_data["min_salary"] = data.get("min_salary")
                json_data["max_salary"] = data.get("max_salary")
                json_data["benefits"] = data.get("benefits")
                json_data["skills"] = data.get("skills")
                # json_data["phone_number"] = data.get("phone", ' ')
                json_data["street_number"] = data.get("street_number")
                
                json_data["coordinate"] = str(data.get("latitude","")) + ', ' + str(data.get("longitude",""))
                json_data["address"] = parameters.get("address", {}).get("value","")
                json_data["min_age"] = data.get("min_age")
                json_data["max_age"] = data.get("max_age")
                json_data["city"] = data.get("region_name","")
                json_data["district"] = data.get("area_name","")
                json_data["ward"] = data.get("ward_name","")

                json_data["salary_type"] = parameters["salary_type"]["value"]
                json_data["contract_type"] = parameters["contract_type"]["value"]
                json_data["job_type"] = parameters["job_type"]["value"]
                json_data["preferred_education"] = parameters.get("preferred_education", {}).get("value", "")
                json_data["preferred_gender"] = parameters.get("preferred_gender",{}).get("value", "")
                json_data["preferred_working_experience"] = parameters.get("preferred_working_experience",{}).get("value")
                json_data["company_name"] = parameters.get("company_name", {}).get("value","")
                
                
                try:
                    opt = Options()
                    opt.add_argument('--no-sandbox')
                    opt.add_argument('--headless')
                    opt.add_argument('--disable-dev-shm-usage')
                    
                    driver = webdriver.Chrome('chromedriver', chrome_options=opt)
                    driver.get(response.url)
                    rq = driver.wait_for_request('/v1/public/ad-listing/phone')
                    rl = json.loads(rq.response.body)
                    
                    driver.close()
                    driver.quit()
                    json_data["phone"] = rl["phone"]
                except Exception as e:
                    json_data["phone"] = ''
                    print(e)


                if json_data["search_keyword"] == '':
                    json_data["search_keyword"] = json_data["job_type"]

                content = VieclamtotContent(self.website, response)
                content.update(json_data)
                insertOne(content.json(), self.connection, 'app_vieclamtot_scraper')


        except Exception as e:
            print(str(traceback.format_exc()))

    def save_num_post(self):
        
        save_statistic(self.time_now, self.crawled_num_post, self.connection)
