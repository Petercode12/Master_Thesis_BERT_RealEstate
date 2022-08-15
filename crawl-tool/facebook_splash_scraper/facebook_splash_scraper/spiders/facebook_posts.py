# ===================================================
#  Title:  Get posts html for later xpath extraction
#  Author: Huỳnh Ngọc Thiện
#  Date:   Jan 9 2021
# ===================================================
import sys

# setting path
sys.path.append("..")
print(sys.path)

import lxml.html
import scrapy
from scrapy.utils.project import get_project_settings
from scrapy_splash import SplashRequest
import json
import time
from datetime import datetime, timedelta
import traceback
import logging
import psycopg2
import uuid

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

    # Convert datetime get from facebook html to timestamp

    def _convert_to_timestamp(self, the_input):

        ts = -1

        for each in ["Hôm qua"]:
            if each in the_input:
                today = datetime.now()

                the_time = the_input.split(" ")[-1].split(":")

                d = (
                    datetime(
                        year=today.year,
                        month=today.month,
                        day=today.day,
                        hour=int(the_time[0]),
                        minute=int(the_time[1]),
                    )
                    - timedelta(days=1)
                )

                ts = int(time.mktime(d.utctimetuple()))

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

                    ts = int(time.mktime(d.utctimetuple()))

                    return ts

                else:

                    today = datetime.now()

                    the_time = the_input.split(" ")

                    the_hrs_mins = the_time[-1].split(":")

                    d = datetime(
                        year=today.year,
                        month=int(the_time[2].replace(",", "")),
                        day=int(the_time[0]),
                        hour=int(the_hrs_mins[0]),
                        minute=int(the_hrs_mins[1]),
                    )

                    ts = int(time.mktime(d.utctimetuple()))

                    return ts

        for each in ["giờ"]:
            if each in the_input:

                today = datetime.now()

                the_time = the_input.split(" ")

                d = (
                    datetime(
                        year=today.year,
                        month=today.month,
                        day=today.day,
                        hour=today.hour,
                        minute=today.minute,
                        second=today.second,
                    )
                    - timedelta(hours=int(the_time[0]))
                )

                ts = int(time.mktime(d.utctimetuple()))

                return ts

        for each in ["phút"]:
            if each in the_input:

                today = datetime.now()

                the_time = the_input.split(" ")

                d = (
                    datetime(
                        year=today.year,
                        month=today.month,
                        day=today.day,
                        hour=today.hour,
                        minute=today.minute,
                        second=today.second,
                    )
                    - timedelta(minutes=int(the_time[0]))
                )

                ts = int(time.mktime(d.utctimetuple()))

                return ts

        for each in ["giây"]:
            if each in the_input:

                today = datetime.now()

                the_time = the_input.split(" ")

                d = (
                    datetime(
                        year=today.year,
                        month=today.month,
                        day=today.day,
                        hour=today.hour,
                        minute=today.minute,
                        second=today.second,
                    )
                    - timedelta(seconds=int(the_time[0]))
                )

                ts = int(time.mktime(d.utctimetuple()))

                return ts

    # This name will be use to call the crawling spider, for example: scrapy crawl facebook_posts

    name = "facebook_posts"

    # Arguments

    def __init__(self, scrolls="", the_uuid="", user_id="", **kwargs):
        self.scrolls = scrolls
        self.user_id = user_id
        self.the_uuid = the_uuid
        super().__init__(**kwargs)

    # Xpath variables to use to get elements when crawling

    xpath_view_more_cmt = "j83agx80 fv0vnmcu hpfvmrgz"

    xpath_view_more_info = "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p"

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
                assert(splash:wait(1))

                while(more)
                do
                    more = false
                    local spans = splash:select_all("span[class='"""
            + self.xpath_view_more_cmt
            + """']")

                    for _, _span in ipairs(spans) do
                        assert(_span:mouse_click())
                        more = true
                    end

                    assert(splash:wait(5))

                    splash:set_viewport_full()

                    local scroll_to = splash:jsfunc("window.scrollTo")
                    local get_body_height = splash:jsfunc(
                        "function() {return document.body.scrollHeight;}"
                    )

                    scroll_to(0, get_body_height())
                    assert(splash:wait(1))

                    local divs = splash:select_all("div[class='"""
            + self.xpath_view_more_info
            + """']")

                    for _, _ in ipairs(divs) do
                        local _div = splash:select("div[class='"""
            + self.xpath_view_more_info
            + """']")
                        if _div ~= nil then
                            assert(_div:mouse_click())
                        end
                    end

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
        with open(
            cfg.get_facebook_cookie_prefix() + str(self.user_id) + ".json", "r"
        ) as jsonfile:
            cookies = json.load(jsonfile)["cookies"]

        # Get groups list
        with open(
            cfg.get_facebook_group_file_prefix() + str(self.user_id) + ".txt",
            "r",
        ) as f:
            groups = str(f.read()).split(",")

        for url in groups:
            # Split string to get group ID
            group = str(url.split("/")[-1])

            # Use group ID to access groups json files that contain posts list in the same group for later storing and accessing to extract xpath

            # with open("./groups/json/group_posts_" + group + '.json', 'r') as jsonfile:
            #     posts = json.load(jsonfile)

            group_json = mongo_db.facebook_group_scraper.find_one(
                {"group": group, "the_uuid": self.the_uuid}
            )

            for post in group_json["results"]:
                # Use post ID from posts list inside each groups json files to access posts html files
                # with open( "./posts/html/post_html_" + post["post"] + '.html', 'w+') as out:
                #     out.write('')

                # Send splash request with cookies to get full html of each posts
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

        now = datetime.now()
        timestamp = int(datetime.timestamp(now))
        the_uuid = uuid.uuid4()

        post = {
            "group": str(response.meta["group"]),
            "post": str(response.meta["post"]),
            "html": response.text,
            "link": response.url.split("&")[0],
            "datetime": now.strftime("%m/%d/%Y, %H:%M:%S"),
            "timestamp": timestamp,
            "the_uuid": str(the_uuid),
        }

        try:

            htmls = lxml.html.fromstring(str(response.text))

            # Start extracting informaiton
            post_user_id = htmls.xpath(
                "//h2[@class='gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl aahdfvyu hzawbc8m']//a/@href"
            )

            post["post_user_id"] = str(post_user_id).split("?")[0].split("/")[-1]
            post_message = htmls.xpath("//div[@class='kr9hpln1']")
            if post_message == []:
                post_message = htmls.xpath(
                    "//div[@class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q']//text()"
                )
                post["post_message"] = post_message

            else:
                post["post_message"] = post_message[0].xpath(".//text()")

            post_image_link = htmls.xpath(
                "//img[@class='i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm bixrwtb6']/@src"
            )

            if len(post_image_link) > 0:
                post["post_image_link"] = post_image_link[0]

            else:
                post["post_image_link"] = " "

            post_image_alt = htmls.xpath(
                "//img[@class='i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm bixrwtb6']/@alt"
            )

            if len(post_image_alt) > 0:
                post["post_image_alt"] = post_image_alt[0]

            else:
                post["post_image_alt"] = " "

            post_total_reactions = htmls.xpath(
                "//span[@class='gpro0wi8 cwj9ozl2 bzsjyuwj ja2t1vim']//text()"
            )

            if len(post_total_reactions) > 0:
                post["post_total_reactions"] = post_total_reactions[0]
            else:
                post["post_total_reactions"] = "0"

            comments_and_shares = htmls.xpath(
                "//div[@class='bp9cbjyn j83agx80 pfnyh3mw p1ueia1e']//text()"
            )

            if len(comments_and_shares) > 0:
                post["post_total_comments"] = comments_and_shares[0].split(" ")[0]
            else:
                post["post_total_comments"] = "0"

            if len(comments_and_shares) > 1:
                post["post_total_shares"] = comments_and_shares[1].split(" ")[0]
            else:
                post["post_total_shares"] = "0"

            post_comments = {}
            comments = htmls.xpath("//div[@class='cwj9ozl2 tvmbv18p']/ul/li")

            user_id_list = {}

            for comment in comments:
                post_comment_user_id = comment.xpath(
                    ".//div[@class='l9j0dhe7 ecm0bbzt rz4wbd8a qt6c0cv9 dati1w0a j83agx80 btwxx1t3 lzcic4wl']//div[@class='nc684nl6']//a/@href"
                )

                post_comment_user_id = (
                    str(post_comment_user_id).split("?")[0].split("/")[-1]
                )

                each = {}

                each["post_comment_message"] = comment.xpath(
                    ".//div[@class='l9j0dhe7 ecm0bbzt rz4wbd8a qt6c0cv9 dati1w0a j83agx80 btwxx1t3 lzcic4wl']//div[@class='ecm0bbzt e5nlhep0 a8c37x1j']//text()"
                )

                links = comment.xpath(
                    ".//div[@class='l9j0dhe7 ecm0bbzt rz4wbd8a qt6c0cv9 dati1w0a j83agx80 btwxx1t3 lzcic4wl']//div[@class='ecm0bbzt e5nlhep0 a8c37x1j']//a"
                )

                for link in links:
                    link = link.xpath("./@href")[0]

                    each["post_comment_tags"] = []
                    each["post_comment_links"] = []

                    if "user" in link:

                        link = str(link).split("/?")[0].split("/")[-1]

                        each["post_comment_tags"].append(link)

                    else:

                        each["post_comment_links"].append(link)

                post_comment_attach_link = comment.xpath(
                    ".//div[@class='j83agx80 bvz0fpym c1et5uql']//a/@href"
                )

                if len(post_comment_attach_link) > 0:

                    each["post_comment_attach_link"] = post_comment_attach_link[0]

                post_comment_image_link = comment.xpath(
                    ".//div[@class='j83agx80 bvz0fpym c1et5uql']//img/@src"
                )

                if len(post_comment_image_link) > 0:

                    each["post_comment_image_link"] = post_comment_image_link[0]

                post_comment_image_alt = comment.xpath(
                    ".//div[@class='j83agx80 bvz0fpym c1et5uql']//img/@alt"
                )

                if len(post_comment_image_alt) > 0:

                    post["post_comment_image_alt"] = post_comment_image_alt[0]

                post_comment_reactions = comment.xpath(
                    ".//div[@class='l9j0dhe7 ecm0bbzt rz4wbd8a qt6c0cv9 dati1w0a j83agx80 btwxx1t3 lzcic4wl']//div[@class='_680y']//span[@class='m9osqain e9vueds3 knj5qynh j5wam9gi jb3vyjys n8tt0mok qt6c0cv9 hyh9befq g0qnabr5']/text()"
                )

                if len(post_comment_reactions) > 0:
                    each["post_comment_reactions"] = post_comment_reactions[0]

                post_comment_timestamp = comment.xpath(
                    ".//div[@class='l9j0dhe7 ecm0bbzt rz4wbd8a qt6c0cv9 dati1w0a j83agx80 btwxx1t3 lzcic4wl']//ul[@class='_6coi oygrvhab ozuftl9m l66bhrea linoseic']//span[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']/text()"
                )

                if len(post_comment_timestamp) > 0:
                    each["post_comment_timestamp"] = self._convert_to_timestamp(
                        post_comment_timestamp[0]
                    )

                user_id = str(post_comment_user_id).split("/?")[0].split("/")[-1]

                post_comments[user_id] = []

                # Replies

                replies = comment.xpath(
                    ".//div[@class='kvgmc6g5 jb3vyjys rz4wbd8a qt6c0cv9 d0szoon8']"
                )

                post_rep = {}

                for index in range(0, len(replies)):
                    reps = replies[index].xpath("./ul/li")

                    if len(reps) > 0:
                        for rep in reps:

                            post_reply_user_id = rep.xpath(
                                ".//div[@class='nc684nl6']//a/@href"
                            )

                            post_reply_user_id = (
                                str(post_reply_user_id).split("?")[0].split("/")[-1]
                            )

                            each_rep = {}

                            each_rep["post_reply_message"] = rep.xpath(
                                ".//div[@class='ecm0bbzt e5nlhep0 a8c37x1j']//text()"
                            )

                            links = rep.xpath(
                                ".//div[@class='ecm0bbzt e5nlhep0 a8c37x1j']//a"
                            )

                            for link in links:
                                link = link.xpath("./@href")[0]

                                each_rep["post_reply_tags"] = []
                                each_rep["post_reply_links"] = []

                                if "user" in link:

                                    link = str(link).split("/?")[0].split("/")[-1]

                                    each_rep["post_reply_tags"].append(link)

                                else:

                                    each_rep["post_reply_links"].append(link)

                            post_reply_attach_link = rep.xpath(
                                ".//div[@class='j83agx80 bvz0fpym c1et5uql']//a/@href"
                            )

                            if len(post_reply_attach_link) > 0:

                                each["post_reply_attach_link"] = post_reply_attach_link[
                                    0
                                ]

                            post_reply_image_link = rep.xpath(
                                ".//div[@class='j83agx80 bvz0fpym c1et5uql']//img/@src"
                            )

                            if len(post_reply_image_link) > 0:

                                each["post_reply_image_link"] = post_reply_image_link[0]

                            post_reply_image_alt = rep.xpath(
                                ".//div[@class='j83agx80 bvz0fpym c1et5uql']//img/@alt"
                            )

                            if len(post_reply_image_alt) > 0:

                                post["post_reply_image_alt"] = post_reply_image_alt[0]

                            post_reply_reactions = rep.xpath(
                                ".//div[@class='_680y']//span[@class='m9osqain e9vueds3 knj5qynh j5wam9gi jb3vyjys n8tt0mok qt6c0cv9 hyh9befq g0qnabr5']/text()"
                            )

                            if len(post_reply_reactions) > 0:
                                each["post_reply_reactions"] = post_reply_reactions[0]

                            post_reply_timestamp = rep.xpath(
                                ".//ul[@class='_6coi oygrvhab ozuftl9m l66bhrea linoseic']//span[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']/text()"
                            )

                            if len(post_reply_timestamp) > 0:
                                each[
                                    "post_reply_timestamp"
                                ] = self._convert_to_timestamp(post_reply_timestamp[0])

                            rep_user_id = (
                                str(post_reply_user_id).split("/?")[0].split("/")[-1]
                            )

                            if post_rep.get(rep_user_id, -1) == -1:
                                post_rep[rep_user_id] = [each_rep]
                            else:
                                post_rep[rep_user_id].append(each_rep)

                each["post_comment_replies"] = post_rep

                post_comments[user_id].append(each)

                # break

            post["post_comments"] = post_comments

            # Stored extracted information to posts json files named by their own post ID

            # with open( "./posts/json/post_" + post["post"] + '.json', 'w+') as jsonfile:
            #     json.dump(post, jsonfile, ensure_ascii=False)

            mongo_db.facebook_post_scraper.insert_one(post)

            try:

                now = datetime.now()
                timestamp = int(datetime.timestamp(now))

                postgres_insert_query = """ INSERT INTO app_facebook_post_scraper (group_id, scrolls, post, the_uuid, post_user_id, post_message, post_image_link, post_total_reactions, post_total_comments, post_total_shares, post_comments, link, datetime, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                record_to_insert = (
                    post["group"],
                    self.scrolls,
                    str(post["post"]),
                    post["the_uuid"],
                    post["post_user_id"],
                    " ".join(post["post_message"]),
                    post["post_image_link"],
                    post["post_total_reactions"],
                    post["post_total_comments"],
                    post["post_total_shares"],
                    str(post["post_comments"]),
                    post["link"],
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

        except Exception as e:

            logging.error(traceback.format_exc())
