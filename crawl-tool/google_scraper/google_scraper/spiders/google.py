import sys

# setting path
sys.path.append("..")
print(sys.path)

import scrapy
import psycopg2
from datetime import datetime
from pymongo import MongoClient
from configuration.config import Config
from helpers.postgres import connect_to_postgres
from helpers.mongo import connect_to_mongodb


cfg = Config("../configuration/config.json")
pg_conn = connect_to_postgres(
    cfg.get_postgres_user(),
    cfg.get_postgres_password(),
    cfg.get_postgres_host(),
    cfg.get_postgres_port(),
    cfg.get_mongo_database(),
)
pg_cursor = pg_conn.cursor()

mongo_db = connect_to_mongodb(
    cfg.get_mongo_user(),
    cfg.get_mongo_password(),
    cfg.get_mongo_host(),
    cfg.get_mongo_port(),
    cfg.get_mongo_database(),
)


class GoogleSpider(scrapy.Spider):
    name = "google"

    results = []

    def __init__(self, search_keyword="", end_page="", **kwargs):
        self.urls = ["https://www.google.com/search?q=" + str(search_keyword)]
        self.search_keyword = search_keyword
        self.end_page = int(end_page)
        self.count = 0
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.urls:
            for page in range(10, (self.end_page + 1) * 10, 10):
                page -= 10
                yield scrapy.Request(url + "&start=" + str(page), callback=self.parse)

    def parse(self, response):

        # with open("./result/html/result.html", "w+") as out:
        #     out.write("")

        # with open("./result/html/result.html", "w+") as out:
        #     out.write(response.text)

        ad_links = response.xpath("//div[@class='v5yQqb']")
        normal_links = response.xpath("//div[@class='yuRUbf']")

        res = {}

        for ad in ad_links:
            link = ad.xpath(".//a[@class='sVXRqc']/@href").get()
            title = ad.xpath(".//a[@class='sVXRqc']//text()").get()
            res[str(title).replace(".", "u002E")] = link

        for normal in normal_links:
            link = normal.xpath(".//a/@href").get()
            title = normal.xpath(".//a//text()").get()
            res[str(title).replace(".", "u002E")] = link

        self.results.append(res)

        self.count += 1

        if self.count == self.end_page:
            # with open("./result/json/Keyword_" + str(self.search_keyword) + "_EndPage_" + str(self.end_page) + '.json', 'w+') as jsonfile:
            #     json.dump(self.results, jsonfile, ensure_ascii=False)

            now = datetime.now()
            timestamp = int(datetime.timestamp(now))
            final = {
                "search_keyword": str(self.search_keyword),
                "end_page": self.end_page,
                "results": self.results,
                "datetime": now.strftime("%m/%d/%Y, %H:%M:%S"),
                "timestamp": timestamp,
            }
            mongo_db[cfg.get_mongo_google_collection()].insert_one(final)

            for each in self.results:
                for key in each:

                    try:

                        postgres_insert_query = """ INSERT INTO app_google_scraper (keyword, crawled_page, title, link, datetime, timestamp) VALUES (%s,%s,%s,%s,%s,%s)"""
                        record_to_insert = (
                            self.search_keyword,
                            self.end_page,
                            key.replace("u002E", "."),
                            each[key],
                            now.strftime("%m/%d/%Y, %H:%M:%S"),
                            timestamp,
                        )
                        pg_cursor.execute(postgres_insert_query, record_to_insert)

                        pg_conn.commit()
                        count = pg_cursor.rowcount
                        print(count, "Record inserted successfully into table")

                    except (Exception, psycopg2.Error) as error:
                        pg_conn.rollback()
                        print("Failed to insert record into table - ", error)
