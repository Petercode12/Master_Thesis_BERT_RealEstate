# ===================================================
#  Title:  Get posts html for later xpath extraction
#  Author: Huỳnh Ngọc Thiện
#  Date:   Jan 9 2021
# ===================================================

import lxml.html
import scrapy
from scrapy.utils.project import get_project_settings
from scrapy_splash import SplashRequest
import json
import time
from datetime import datetime, timedelta
import traceback
import logging
import os

# import psycopg2
# import uuid
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


class FacebookReactionSpider(scrapy.Spider):

    # This name will be use to call the crawling spider, for example: scrapy crawl facebook_posts

    name = "facebook_reactions"

    # Arguments

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # This will setup settings variable to get constant from settings.py such as SCROLLS (scrolling number)

    settings = get_project_settings()

    # Xpath variables to use to get elements when crawling

    xpath_view_reaction = "gpro0wi8 pcp91wgn"

    # xpath_hover_reaction =

    def start_requests(self):

        # Lua script to interact with js in the website while crawling

        script_links = (
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

                scroll_to(0, get_body_height())

                local _a = splash:select("span[class='"""
            + self.xpath_view_reaction
            + """']")

                assert(_a:mouse_click())
                assert(splash:wait(5))

                for _ = 1, tonumber(_a:text()) do
                    scroll_to(0, get_body_height())
                    assert(splash:wait(5))
                end 

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

            # Use group ID to access groups json files that contain posts list in the same group for later storing and accessing to extract xpath

            with open("./groups/json/group_posts_" + group + ".json", "r") as jsonfile:
                posts = json.load(jsonfile)

            # group_json = db.facebook_group_scraper.find_one({'group' : group, 'the_uuid' : self.the_uuid })

            # for post in group_json["results"]:
            for post in posts:

                # Use post ID from posts list inside each groups json files to access posts html files

                # with open( "./posts/html/post_html_" + post["post"] + '.html', 'w+') as out:
                #     out.write('')

                # Send splash request with cookies to get full html of each posts

                if not os.path.isfile(
                    "./groups/reaction/reaction_html_"
                    + group
                    + "_"
                    + post["post"]
                    + ".html"
                ):

                    yield SplashRequest(
                        url=post["link"],
                        callback=self.parse,
                        session_id="test",
                        meta={
                            "splash": {
                                "endpoint": "execute",
                                "args": {
                                    "lua_source": script_links,
                                    "cookies": cookies,
                                    "timeout": 3600,
                                },
                            },
                            "post": post["post"],
                            "group": group,
                        },
                    )

                break

                # time.sleep(30)

    def parse(self, response):

        # Store each return posts html to their corresponding html file named with their own post ID

        # with open( "./posts/html/post_html_" + response.meta["post"] + '.html', 'w+') as out:
        #     out.write(response.text)

        with open(
            "./groups/reaction/reaction_html_"
            + response.meta["group"]
            + "_"
            + response.meta["post"]
            + ".html",
            "w+",
        ) as out:
            out.write(response.text)
