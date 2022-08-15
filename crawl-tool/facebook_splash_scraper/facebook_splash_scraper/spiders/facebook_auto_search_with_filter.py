# ===========================================================
#  Title:  Get posts links and group html for later crawling
#  Author: Huỳnh Ngọc Thiện
#  Date:   Jan 9 2021
# ===========================================================

import sys

# setting path
sys.path.append("..")
print(sys.path)

import scrapy
from scrapy.utils.project import get_project_settings
from scrapy_splash import SplashRequest
import json
import psycopg2
from datetime import datetime

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


class FacebookSpider(scrapy.Spider):
    # This name will be use to call the crawling spider, for example: scrapy crawl facebook_links

    name = "facebook_auto_search"

    # Arguments

    def __init__(self, search_keyword="", scrolls="", user_id="", **kwargs):
        self.search_keyword = search_keyword
        self.user_id = user_id
        self.scrolls = int(scrolls)
        super().__init__(**kwargs)

    # This will setup settings variable to get constant from settings.py such as SCROLLS (scrolling number)

    settings = get_project_settings()

    # Xpath variables to use to get elements when crawling

    xpath_search_container = "j83agx80 l9j0dhe7 k4urcfbm"

    xpath_info_user = "nc684nl6"

    xpath_work_info = "d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa fgxwclzu e9vueds3 j5wam9gi knj5qynh m9osqain"

    xpath_detail_info = "jktsbyx5"

    # Lua script to interact with js in the website while crawling

    def start_requests(self):

        # Scripts

        script = (
            """

            function main(splash, args)

                splash:init_cookies(splash.args.cookies)

                assert(splash:go{
                    splash.args.url,
                    headers=splash.args.headers
                })

                assert(splash:wait(5))

                splash:set_viewport_full()

                local scroll_to = splash:jsfunc("window.scrollTo")
                local get_body_height = splash:jsfunc(
                    "function() {return document.body.scrollHeight;}"
                )

                for _ = 1, """
            + str(self.scrolls)
            + """ do
                    scroll_to(0, get_body_height())
                    assert(splash:wait(1))
                end 

                assert(splash:wait(5))

                local entries = splash:history()
                local last_response = entries[#entries].response

                return {
                    cookies = splash:get_cookies(),
                    headers = last_response.headers,
                    html = splash:html()
                }
            end

        """
        )

        # Get Facebook Account Cookie that was stored in the first spider

        with open("./cookies/cookie_" + str(self.user_id) + ".json", "r") as jsonfile:
            cookies = json.load(jsonfile)["cookies"]

        yield SplashRequest(
            url="https://facebook.com/search/people?q=" + str(self.search_keyword),
            callback=self.parse_links,
            session_id="test",
            meta={
                "splash": {
                    "endpoint": "execute",
                    "args": {
                        "lua_source": script,
                        "cookies": cookies,
                        "headers": {
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
                        },
                    },
                },
                # "key": query['key']
            },
        )

        # query_list = self.settings.get("SEARCH_QUERY")
        # search_link = self.settings.get("SEARCH_LINK")

        # for query in query_list:

        #     url = search_link + query['key']

        #     if query['filter'] != '':
        #         url = url + '&filters=' + query['filter']

        #     print(url)

        #     with open("./search/html/auto_with_filter/search_result_of_" + query['key']+ '.html', 'w+') as out:
        #         out.write('')

        #     # Send splash request with cookies to get full html of each groups

        #     yield SplashRequest(
        #         url=url,
        #         callback=self.parse_links,
        #         session_id="test",
        #         meta={
        #             "splash": {
        #                 "endpoint": "execute",
        #                 "args": {
        #                     "lua_source": self.script,
        #                     "cookies": cookies,
        #                     "headers": {
        #                         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        #                     }
        #                 }
        #             },
        #             "key": query['key']
        #         }
        #     )

    def parse_links(self, response):

        # with open("./search/json/auto_with_filter/search_result_info_of_" + response.meta["key"] + '.html', 'w+') as out:
        #     out.write(response.text)

        print('Hello')
        info = response.xpath(f"//div[@class='{self.xpath_search_container}']")
        print('-'*20)
        print(response.text[:200])
        print('-'*20)
        print('Hello1')
        print(info)
        output_info = []

        for info_xpath in info:
            link = info_xpath.xpath(
                ".//div[@class='" + self.xpath_info_user + "']/a/@href"
            ).get()
            name = info_xpath.xpath(
                ".//div[@class='" + self.xpath_info_user + "']/a//text()"
            ).get()
            worksAt = info_xpath.xpath(
                ".//span[@class='" + self.xpath_work_info + "']//text()"
            ).get()
            bio = info_xpath.xpath(
                ".//div[@class='" + self.xpath_detail_info + "']/span[1]/span/text()"
            ).get()
            friends = info_xpath.xpath(
                ".//div[@class='" + self.xpath_detail_info + "']/span[2]/span/text()"
            ).get()

            result = {
                "name": name,
                "link": link,
                "worksAt": worksAt,
                "bio": bio,
                "friends": friends,
            }

            try:

                now = datetime.now()

                timestamp = int(datetime.timestamp(now))
                print('-'*30)
                print(f'{result}')
                print('-'*30)
                postgres_insert_query = """ INSERT INTO app_facebook_search_scraper (keyword, scrolls, name, bio, work, friends, link, datetime, timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                record_to_insert = (
                    self.search_keyword,
                    self.scrolls,
                    name,
                    bio,
                    worksAt,
                    friends,
                    link,
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

            output_info.append(result)

        now = datetime.now()

        timestamp = int(datetime.timestamp(now))

        final = {
            "search_keyword": str(self.search_keyword),
            "scrolls": self.scrolls,
            "results": output_info,
            "datetime": now.strftime("%m/%d/%Y, %H:%M:%S"),
            "timestamp": timestamp,
        }

        mongo_db.facebook_search_scraper.insert_one(final)

        # with open("./search/json/auto_with_filter/search_result_info_of_" + str(response.meta["key"]) + '.json', 'w+') as jsonfile:
        #     json.dump(output_info, jsonfile, ensure_ascii=False)
