# ===========================================================
#  Title:  Get posts links and group html for later crawling
#  Author: Huỳnh Ngọc Thiện
#  Date:   Jan 9 2021
# ===========================================================

import scrapy
from scrapy.utils.project import get_project_settings
from scrapy_splash import SplashRequest
import json
import time

from datetime import datetime, timedelta

# import psycopg2
# from pymongo import MongoClient

# try:
#     connection = psycopg2.connect(user="WhiteWolf21",
#                                     password="Ohyeahbaby123",
#                                     host="localhost",
#                                     port="5432",
#                                     database="huynhngocthien_django_tools")
#     cursor = connection.cursor()

# except (Exception, psycopg2.Error) as error :
#     if(connection):
#         print("Failed to insert record into mobile table", error)

# client = MongoClient('mongodb://localhost:27017')

# db = client.huynhngocthien_django_tools


class FacebookSpider(scrapy.Spider):

    # This name will be use to call the crawling spider, for example: scrapy crawl facebook_links

    name = "new_facebook_links"

    # Arguments

    def __init__(self, scrolls="", **kwargs):
        self.scrolls = int(scrolls)
        super().__init__(**kwargs)

    # This will setup settings variable to get constant from settings.py such as SCROLLS (scrolling number)

    settings = get_project_settings()

    # Xpath variables to use to get elements when crawling

    xpath_post_link = "_52jc _5qc4 _78cz _24u0 _36xo"

    xpath_user_profile_1 = "_52jd _52jb _52jh _5qc3 _4vc- _3rc4 _4vc-"

    xpath_user_profile_2 = "_52jd _52jb _52jg _5qc3 _4vc- _3rc4 _4vc-"

    # Convert datetime get from facebook html to timestamp

    def _convert_to_timestamp(the_input):

        ts = -1

        for each in ["ngày"]:
            if each in the_input:

                today = datetime.utcnow()

                the_time = the_input.split(" ")

                d = datetime(
                    year=today.year,
                    month=today.month,
                    day=today.day,
                    hour=today.hour,
                    minute=today.minute,
                    second=today.second,
                ) - timedelta(days=int(the_time[0]))

                ts = time.mktime(d.utctimetuple())

                return ts

        for each in ["tuần"]:
            if each in the_input:

                today = datetime.utcnow()

                the_time = the_input.split(" ")

                d = datetime(
                    year=today.year,
                    month=today.month,
                    day=today.day,
                    hour=today.hour,
                    minute=today.minute,
                    second=today.second,
                ) - timedelta(weeks=int(the_time[0]))

                ts = time.mktime(d.utctimetuple())

                return ts

        for each in ["tháng"]:
            if each in the_input:
                if "," in the_input:

                    the_time = the_input.split(" ")

                    the_hrs_mins = the_time[-1].split(":")

                    d = datetime(
                        year=int(the_time[3]),
                        month=int(the_time[2].replace(",", "")),
                        day=int(the_time[0]),
                        hour=int(the_hrs_mins[0]),
                        minute=int(the_hrs_mins[1]),
                    )

                    ts = time.mktime(d.utctimetuple())

                    return ts

                else:

                    today = datetime.utcnow()

                    the_time = the_input.split(" ")

                    the_hrs_mins = the_time[-1].split(":")

                    d = datetime(
                        year=today.year,
                        month=int(the_time[2].replace(",", "")),
                        day=int(the_time[0]),
                        hour=int(the_hrs_mins[0]),
                        minute=int(the_hrs_mins[1]),
                    )

                    ts = time.mktime(d.utctimetuple())

                    return ts

        for each in ["năm"]:
            if each in the_input:

                today = datetime.utcnow()

                the_time = the_input.split(" ")

                d = datetime(
                    year=today.year,
                    month=today.month,
                    day=today.day,
                    hour=today.hour,
                    minute=today.minute,
                    second=today.second,
                ) - timedelta(years=int(the_time[0]))

                ts = time.mktime(d.utctimetuple())

                return ts

        for each in ["giờ"]:
            if each in the_input:

                today = datetime.utcnow()

                the_time = the_input.split(" ")

                d = datetime(
                    year=today.year,
                    month=today.month,
                    day=today.day,
                    hour=today.hour,
                    minute=today.minute,
                    second=today.second,
                ) - timedelta(hours=int(the_time[0]))

                ts = time.mktime(d.utctimetuple())

                return ts

        for each in ["phút"]:
            if each in the_input:

                today = datetime.utcnow()

                the_time = the_input.split(" ")

                d = datetime(
                    year=today.year,
                    month=today.month,
                    day=today.day,
                    hour=today.hour,
                    minute=today.minute,
                    second=today.second,
                ) - timedelta(minutes=int(the_time[0]))

                ts = time.mktime(d.utctimetuple())

                return ts

        for each in ["giây"]:
            if each in the_input:

                today = datetime.utcnow()

                the_time = the_input.split(" ")

                d = datetime(
                    year=today.year,
                    month=today.month,
                    day=today.day,
                    hour=today.hour,
                    minute=today.minute,
                    second=today.second,
                ) - timedelta(seconds=int(the_time[0]))

                ts = time.mktime(d.utctimetuple())

                return ts

        for each in ["Hôm qua"]:
            if each in the_input:
                today = datetime.utcnow()

                the_time = the_input.split(" ")[-1].split(":")

                d = datetime(
                    year=today.year,
                    month=today.month,
                    day=today.day,
                    hour=int(the_time[0]),
                    minute=int(the_time[1]),
                ) - timedelta(days=1)

                ts = time.mktime(d.utctimetuple())

                return ts

        return ts

    def start_requests(self):

        # Lua script to interact with js in the website while crawling

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
                    assert(splash:wait(5))
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

        with open("./cookies/cookie_1.json", "r") as jsonfile:
            cookies = json.load(jsonfile)["cookies"]

        # Get groups list

        with open("./groups/groups_facebook_1.txt", "r") as f:
            groups = str(f.read()).split(",")

        for url in groups:

            # Split string to get group ID

            group = str(url.split("/")[-1])

            # # Use group ID to name groups html files for later storing and accessing to extract xpath

            # with open( "./groups/html/group_html_" + group + '.html', 'w+') as out:
            #     out.write('')

            # Send splash request with cookies to get full html of each groups

            yield SplashRequest(
                url=url,
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
                            "timeout": 9999,
                        },
                    },
                    "group": group,
                },
            )

    def parse_links(self, response):

        # Store each return groups html to their corresponding html file named with their own group ID

        # print("=====================", "./groups/html/group_html_" + response.meta["group"] + '.html')

        with open(
            "./groups/html/group_html_" + response.meta["group"] + ".html", "w+"
        ) as out:
            out.write(response.text)

        # Extract xpath to get more information of each posts scraped from groups pages

        links = response.xpath("//div[@class='" + self.xpath_post_link + "']")

        # print("=====================", links)

        output_links = []

        for link_xpath in links:

            link = link_xpath.xpath("./a/@href").get()

            if link == "#":
                break

            if "permalink" not in str(link):
                link = "https://facebook.com" + link.split("&refid")[0]

            times = link_xpath.xpath("./a//text()").get()

            times = self._convert_to_timestamp(times)

            link = link.split("/?")[0]

            post = str(link.split("/")[-1])

            result = {"post": post, "link": link.replace("m.", ""), "timestamp": times}

            output_links.append(result)

        now = datetime.utcnow()

        timestamp = int(datetime.timestamp(now))

        final = {
            "group": str(response.meta["group"]),
            "scrolls": self.scrolls,
            "html": response.text,
            "results": output_links,
            "datetime": now.strftime("%m/%d/%Y, %H:%M:%S"),
            "timestamp": timestamp,
        }

        # db.facebook_group_scraper.insert_one(final)

        # # Dump posts list with their additional information such as timestamp to groups json filles (named with group ID) for the third spider to access and get

        with open(
            "./groups/json/group_posts_" + str(response.meta["group"]) + ".json", "w+"
        ) as jsonfile:
            json.dump(output_links, jsonfile, ensure_ascii=False)
