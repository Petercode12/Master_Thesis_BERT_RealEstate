# =========================================================================
#  Title:  Extract neede features through xpath from posts html files that
#  Author: Huỳnh Ngọc Thiện
#  Date:   Jan 9 2021
# =========================================================================

import lxml.html
import json
import os
import time
import traceback
import logging
import psycopg2
import psycopg2.extras
import traceback
import copy
import re

from lxml.etree import tostring as htmlstring
from scrapy.utils.project import get_project_settings
from datetime import datetime, timedelta

import sys

sys.path.append("..")
print(sys.path)

from configuration.config import Config
from helpers.postgres import connect_to_postgres

cfg = Config("../configuration/config.json")
pg_conn = connect_to_postgres(
    cfg.get_postgres_user(),
    cfg.get_postgres_password(),
    cfg.get_postgres_host(),
    cfg.get_postgres_port(),
    cfg.get_mongo_database(),
)
pg_cursor = pg_conn.cursor()

# This will setup settings variable to get constant from settings.py such as SCROLLS (scrolling number)

settings = get_project_settings()

# Get groups list

with open("./groups/groups_facebook_1.txt", "r") as f:
    groups = str(f.read()).split(",")

# Convert datetime get from facebook html to timestamp


def _convert_to_timestamp(the_input):

    ts = -1

    for each in ["ngày"]:
        if each in the_input:

            today = datetime.utcnow()

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
                - timedelta(days=int(the_time[0]))
            )

            ts = time.mktime(d.utctimetuple())

            return ts

    for each in ["tuần"]:
        if each in the_input:

            today = datetime.utcnow()

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
                - timedelta(weeks=int(the_time[0]))
            )

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

            d = (
                datetime(
                    year=today.year,
                    month=today.month,
                    day=today.day,
                    hour=today.hour,
                    minute=today.minute,
                    second=today.second,
                )
                - timedelta(years=int(the_time[0]))
            )

            ts = time.mktime(d.utctimetuple())

            return ts

    for each in ["giờ"]:
        if each in the_input:

            today = datetime.utcnow()

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

            ts = time.mktime(d.utctimetuple())

            return ts

    for each in ["phút"]:
        if each in the_input:

            today = datetime.utcnow()

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

            ts = time.mktime(d.utctimetuple())

            return ts

    for each in ["giây"]:
        if each in the_input:

            today = datetime.utcnow()

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

            ts = time.mktime(d.utctimetuple())

            return ts

    for each in ["Hôm qua"]:
        if each in the_input:
            today = datetime.utcnow()

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

            ts = time.mktime(d.utctimetuple())

            return ts

    return ts


# Now we will go through group lists to get group IDs, then loop through them to access to posts list json and from there, we will get each post ID to access their own html file to extract xpath like the following codes

for url in groups:

    group = str(url.split("/")[-1])

    with open("./groups/json/group_posts_" + group + ".json", "r") as jsonfile:
        posts = json.load(jsonfile)

    for post in posts:

        # Check if post was crawled and stored into html file or not

        the_file = "./groups/post/post_html_" + group + "_" + post["post"] + ".html"

        # the_file = './groups/post/post_html_nghephantichdulieu_479308896748775.html'

        if os.path.isfile(the_file):
            htmls = ""
            with open(the_file, "r") as f:
                htmls = f.read()

            # Parse string html in file into xpath objects

            print(post)

            try:

                htmls = lxml.html.fromstring(str(htmls))

            except Exception as e:

                logging.error(traceback.format_exc())

                continue

            # Start extracting informaiton

            post_id = post["post"]

            timestamps = post["timestamp"]

            post = {}

            post["group_id"] = group

            post["post_id"] = post_id

            post["timestamp"] = timestamps

            post["created_at"] = datetime.utcnow().timestamp()

            post["updated_at"] = datetime.utcnow().timestamp()

            post_user_id = htmls.xpath(
                "//h2[@class='gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl aahdfvyu hzawbc8m']//a/@href"
            )

            post_user_id_array = re.findall("user\/.+\/\?", post_user_id[0])

            if post_user_id_array != []:
                post["post_user_id"] = post_user_id_array[0].split("/")[1]
            else:

                post_user_id_array = re.findall("\?id=.+&", post_user_id[0])

                if post_user_id_array != []:
                    post["post_user_id"] = (
                        post_user_id_array[0].split("=")[-1].replace("&", "")
                    )
                else:
                    post["post_user_id"] = post_user_id[0]

            post_user_id = post["post_user_id"]

            # print(post["post_user_id"])

            # post["post_user_name"] = htmls.xpath("//h2[@class='gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl aahdfvyu hzawbc8m']//a//text()")[0]

            post_user_name = htmls.xpath(
                "//h2[@class='gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl aahdfvyu hzawbc8m']//a//text()"
            )[0]

            post_message = htmls.xpath("//div[@class='kr9hpln1']")

            if post_message == []:

                post_message = htmls.xpath(
                    "//div[@class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q']//text()"
                )

                post["post_message"] = post_message

            else:

                post["post_message"] = post_message[0].xpath(".//text()")

            post_image_link = htmls.xpath(
                ".//img[@class='i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm']/@src"
            )

            if len(post_image_link) > 0:

                post["post_image_link"] = post_image_link

            post_image_alt = htmls.xpath(
                "//img[@class='i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm bixrwtb6']/@alt"
            )

            if len(post_image_alt) > 0:

                post["post_image_alt"] = post_image_alt[0]

            post_total_reactions = htmls.xpath(
                "//span[@class='gpro0wi8 cwj9ozl2 bzsjyuwj ja2t1vim']//text()"
            )

            if len(post_total_reactions) > 0:

                post["post_total_reactions"] = post_total_reactions[0]

            else:

                post["post_total_reactions"] = 0

            comments_and_shares = htmls.xpath(
                "//div[@class='bp9cbjyn j83agx80 pfnyh3mw p1ueia1e']//text()"
            )

            if len(comments_and_shares) > 0:

                post["post_total_comments"] = comments_and_shares[0].split(" ")[0]

            else:

                post["post_total_comments"] = 0

            if len(comments_and_shares) > 1:

                post["post_total_shares"] = comments_and_shares[1].split(" ")[0]

            else:

                post["post_total_shares"] = 0

            comments = htmls.xpath("//div[@class='cwj9ozl2 tvmbv18p']/ul/li")

            user_id_list = {}

            i = 0

            post_comments = []

            while i < len(comments):

                if len(comments[i].xpath("./div")) > 0:

                    comment = comments[i].xpath("./div")[0]

                    each = {}

                    post_comment_user_id = comment.xpath(
                        ".//div[@class='tw6a2znq sj5x9vvc d1544ag0 cxgpxx05']//div[@class='nc684nl6']//a/@href"
                    )

                    post_comment_user_id_array = re.findall(
                        "user\/.+\/\?", post_comment_user_id[0]
                    )

                    if post_comment_user_id_array != []:
                        each["post_comment_user_id"] = post_comment_user_id_array[
                            0
                        ].split("/")[1]
                    else:

                        post_comment_user_id_array = re.findall(
                            "\?id=.+&", post_comment_user_id[0]
                        )

                        if post_comment_user_id_array != []:
                            each["post_comment_user_id"] = (
                                post_comment_user_id_array[0]
                                .split("=")[-1]
                                .replace("&", "")
                            )
                        else:
                            each["post_comment_user_id"] = post_comment_user_id[0]

                    post_comment_user_id = each["post_comment_user_id"]

                    each["post_user_name"] = comment.xpath(
                        ".//div[@class='tw6a2znq sj5x9vvc d1544ag0 cxgpxx05']//div[@class='nc684nl6']//a//text()"
                    )[0]

                    # print(each["post_user_name"])

                    each["post_message"] = comment.xpath(
                        ".//div[@class='l9j0dhe7 ecm0bbzt rz4wbd8a qt6c0cv9 dati1w0a j83agx80 btwxx1t3 lzcic4wl']//div[@class='ecm0bbzt e5nlhep0 a8c37x1j']//text()"
                    )

                    links = comment.xpath(
                        ".//div[@class='l9j0dhe7 ecm0bbzt rz4wbd8a qt6c0cv9 dati1w0a j83agx80 btwxx1t3 lzcic4wl']//div[@class='ecm0bbzt e5nlhep0 a8c37x1j']//a"
                    )

                    for link in links:
                        link = link.xpath("./@href")[0]

                        each["post_tags"] = []
                        each["post_links"] = []

                        if "user" in link:

                            link = str(link).split("/?")[0].split("/")[-1]

                            each["post_tags"].append(link)

                        else:

                            each["post_links"].append(link)

                    post_attach_link = comment.xpath(
                        ".//div[@class='j83agx80 bvz0fpym c1et5uql']//a/@href"
                    )

                    if len(post_attach_link) > 0:

                        each["post_attach_link"] = post_attach_link[0]

                    post_image_link = comment.xpath(
                        ".//div[@class='i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm']//img/@src"
                    )

                    if len(post_image_link) > 0:

                        each["post_image_link"] = post_image_link[0]

                    post_image_alt = comment.xpath(
                        ".//div[@class='j83agx80 bvz0fpym c1et5uql']//img/@alt"
                    )

                    if len(post_image_alt) > 0:

                        post["post_image_alt"] = post_image_alt[0]

                    post_total_reactions = comment.xpath(
                        ".//div[@class='l9j0dhe7 ecm0bbzt rz4wbd8a qt6c0cv9 dati1w0a j83agx80 btwxx1t3 lzcic4wl']//div[@class='_680y']//span[@class='m9osqain e9vueds3 knj5qynh j5wam9gi jb3vyjys n8tt0mok qt6c0cv9 hyh9befq g0qnabr5']/text()"
                    )

                    if len(post_total_reactions) > 0:
                        each["post_total_reactions"] = post_total_reactions[0]
                    else:
                        each["post_total_reactions"] = 0

                    timestamps = comment.xpath(
                        ".//div[@class='l9j0dhe7 ecm0bbzt rz4wbd8a qt6c0cv9 dati1w0a j83agx80 btwxx1t3 lzcic4wl']//ul[@class='_6coi oygrvhab ozuftl9m l66bhrea linoseic']//span[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']/text()"
                    )

                    if len(timestamps) > 0:
                        each["timestamp"] = _convert_to_timestamp(timestamps[0])

                    post_comments.append(each)

                    if len(comments[i].xpath("./div")) > 1:
                        check_child = comments[i].xpath("./div")[1].xpath(".//text()")

                        if len(check_child) > 0:

                            child_comments = (
                                comments[i]
                                .xpath("./div")[1]
                                .xpath(
                                    "./div[@class='kvgmc6g5 jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso']/ul/li"
                                )
                            )

                            j = 0

                            while j < len(child_comments):

                                if len(child_comments[j].xpath("./div")) > 0:

                                    comment = child_comments[j].xpath("./div")[0]

                                    # with open( './posts/json/post_test.html', 'w+') as out:
                                    #     out.write(lxml.etree.tostring(comment, encoding='unicode', pretty_print=True))

                                    # exit()

                                    each = {}

                                    post_second_comment_user_id = comment.xpath(
                                        ".//div[@class='tw6a2znq sj5x9vvc d1544ag0 cxgpxx05']//div[@class='nc684nl6']//a/@href"
                                    )

                                    if post_comment_user_id == []:
                                        j += 1
                                        continue

                                    each[
                                        "post_comment_parent_id"
                                    ] = post_comment_user_id

                                    post_second_comment_user_id_array = re.findall(
                                        "user\/.+\/\?", post_second_comment_user_id[0]
                                    )

                                    if post_second_comment_user_id_array != []:
                                        each[
                                            "post_comment_user_id"
                                        ] = post_second_comment_user_id_array[0].split(
                                            "/"
                                        )[
                                            1
                                        ]
                                    else:

                                        post_second_comment_user_id_array = re.findall(
                                            "\?id=.+&", post_second_comment_user_id[0]
                                        )

                                        if post_second_comment_user_id_array != []:
                                            each["post_comment_user_id"] = (
                                                post_second_comment_user_id_array[0]
                                                .split("=")[-1]
                                                .replace("&", "")
                                            )
                                        else:
                                            each[
                                                "post_comment_user_id"
                                            ] = post_second_comment_user_id[0]

                                    post_second_comment_user_id = each[
                                        "post_comment_user_id"
                                    ]

                                    # print(each["post_comment_user_id"])

                                    each["post_user_name"] = comment.xpath(
                                        ".//div[@class='tw6a2znq sj5x9vvc d1544ag0 cxgpxx05']//div[@class='nc684nl6']//a//text()"
                                    )[0]

                                    # print(each["post_user_name"])

                                    each["post_message"] = comment.xpath(
                                        ".//div[@class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql']//text()"
                                    )

                                    links = comment.xpath(
                                        ".//div[@class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql']//a"
                                    )

                                    for link in links:
                                        link = link.xpath("./@href")[0]

                                        each["post_tags"] = []
                                        each["post_links"] = []

                                        if "user" in link:

                                            link = (
                                                str(link).split("/?")[0].split("/")[-1]
                                            )

                                            each["post_tags"].append(link)

                                        else:

                                            each["post_links"].append(link)

                                    post_attach_link = comment.xpath(
                                        ".//div[@class='j83agx80 bvz0fpym c1et5uql']//a/@href"
                                    )

                                    if len(post_attach_link) > 0:

                                        each["post_attach_link"] = post_attach_link[0]

                                    post_image_link = comment.xpath(
                                        ".//div[@class='i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm']//img/@src"
                                    )

                                    if len(post_image_link) > 0:

                                        each["post_image_link"] = post_image_link[0]

                                    post_image_alt = comment.xpath(
                                        ".//div[@class='j83agx80 bvz0fpym c1et5uql']//img/@alt"
                                    )

                                    if len(post_image_alt) > 0:

                                        post["post_image_alt"] = post_image_alt[0]

                                    post_total_reactions = comment.xpath(
                                        ".//span[@class='m9osqain e9vueds3 knj5qynh j5wam9gi jb3vyjys n8tt0mok qt6c0cv9 hyh9befq g0qnabr5']/text()"
                                    )

                                    if len(post_total_reactions) > 0:
                                        each[
                                            "post_total_reactions"
                                        ] = post_total_reactions[0]

                                    else:

                                        each["post_total_reactions"] = 0

                                    timestamps = comment.xpath(
                                        ".//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl m9osqain gpro0wi8 knj5qynh']/span[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']/text()"
                                    )

                                    if len(timestamps) > 0:
                                        each["timestamp"] = _convert_to_timestamp(
                                            timestamps[0]
                                        )

                                    post_comments.append(each)

                                    if len(child_comments[j].xpath("./div")) > 1:
                                        check_child = (
                                            child_comments[j]
                                            .xpath("./div")[1]
                                            .xpath(".//text()")
                                        )

                                        if len(check_child) > 0:

                                            third_child_comments = (
                                                child_comments[j]
                                                .xpath("./div")[1]
                                                .xpath("./ul/li")
                                            )

                                            k = 0

                                            while k < len(third_child_comments):

                                                if (
                                                    len(
                                                        third_child_comments[k].xpath(
                                                            "./div"
                                                        )
                                                    )
                                                    > 0
                                                ):

                                                    comment = third_child_comments[
                                                        k
                                                    ].xpath("./div")[0]

                                                    # with open( './posts/json/post_test.html', 'w+') as out:
                                                    #     out.write(lxml.etree.tostring(comment, encoding='unicode', pretty_print=True))

                                                    # exit()

                                                    each = {}

                                                    post_comment_user_id = comment.xpath(
                                                        ".//div[@class='tw6a2znq sj5x9vvc d1544ag0 cxgpxx05']//div[@class='nc684nl6']//a/@href"
                                                    )

                                                    if post_comment_user_id == []:
                                                        k += 1
                                                        continue

                                                    each[
                                                        "post_comment_parent_id"
                                                    ] = post_second_comment_user_id

                                                    post_comment_user_id_array = (
                                                        re.findall(
                                                            "user\/.+\/\?",
                                                            post_comment_user_id[0],
                                                        )
                                                    )

                                                    if post_comment_user_id_array != []:
                                                        each[
                                                            "post_comment_user_id"
                                                        ] = post_comment_user_id_array[
                                                            0
                                                        ].split(
                                                            "/"
                                                        )[
                                                            1
                                                        ]
                                                    else:

                                                        post_comment_user_id_array = (
                                                            re.findall(
                                                                "\?id=.+&",
                                                                post_comment_user_id[0],
                                                            )
                                                        )

                                                        if (
                                                            post_comment_user_id_array
                                                            != []
                                                        ):
                                                            each[
                                                                "post_comment_user_id"
                                                            ] = (
                                                                post_comment_user_id_array[
                                                                    0
                                                                ]
                                                                .split("=")[-1]
                                                                .replace("&", "")
                                                            )
                                                        else:
                                                            each[
                                                                "post_comment_user_id"
                                                            ] = post_comment_user_id[0]

                                                    post_comment_user_id = each[
                                                        "post_comment_user_id"
                                                    ]

                                                    # print(each["post_comment_user_id"])

                                                    each[
                                                        "post_comment_user_id"
                                                    ] = post_comment_user_id

                                                    each[
                                                        "post_user_name"
                                                    ] = comment.xpath(
                                                        ".//div[@class='tw6a2znq sj5x9vvc d1544ag0 cxgpxx05']//div[@class='nc684nl6']//a//text()"
                                                    )[
                                                        0
                                                    ]

                                                    # print(each["post_user_name"])

                                                    each[
                                                        "post_message"
                                                    ] = comment.xpath(
                                                        ".//div[@class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql']//text()"
                                                    )

                                                    links = comment.xpath(
                                                        ".//div[@class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql']//a"
                                                    )

                                                    for link in links:
                                                        link = link.xpath("./@href")[0]

                                                        each["post_tags"] = []
                                                        each["post_links"] = []

                                                        if "user" in link:

                                                            link = (
                                                                str(link)
                                                                .split("/?")[0]
                                                                .split("/")[-1]
                                                            )

                                                            each["post_tags"].append(
                                                                link
                                                            )

                                                        else:

                                                            each["post_links"].append(
                                                                link
                                                            )

                                                    post_attach_link = comment.xpath(
                                                        ".//div[@class='j83agx80 bvz0fpym c1et5uql']//a/@href"
                                                    )

                                                    if len(post_attach_link) > 0:

                                                        each[
                                                            "post_attach_link"
                                                        ] = post_attach_link[0]

                                                    post_image_link = comment.xpath(
                                                        ".//div[@class='i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm']//img/@src"
                                                    )

                                                    if len(post_image_link) > 0:

                                                        each[
                                                            "post_image_link"
                                                        ] = post_image_link[0]

                                                    post_image_alt = comment.xpath(
                                                        ".//div[@class='j83agx80 bvz0fpym c1et5uql']//img/@alt"
                                                    )

                                                    if len(post_image_alt) > 0:

                                                        post[
                                                            "post_image_alt"
                                                        ] = post_image_alt[0]

                                                    post_total_reactions = comment.xpath(
                                                        ".//span[@class='m9osqain e9vueds3 knj5qynh j5wam9gi jb3vyjys n8tt0mok qt6c0cv9 hyh9befq g0qnabr5']/text()"
                                                    )

                                                    if len(post_total_reactions) > 0:
                                                        each[
                                                            "post_total_reactions"
                                                        ] = post_total_reactions[0]

                                                    else:
                                                        each["post_total_reactions"] = 0

                                                    timestamps = comment.xpath(
                                                        ".//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl m9osqain gpro0wi8 knj5qynh']/span[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']/text()"
                                                    )

                                                    if len(timestamps) > 0:
                                                        each[
                                                            "timestamp"
                                                        ] = _convert_to_timestamp(
                                                            timestamps[0]
                                                        )

                                                    post_comments.append(each)

                                                # print(111)

                                                k += 1

                                j += 1

                i += 1

            # Stored extracted information to posts json files named by their own post ID

            # with open( "./posts/json/post_" + post["post_id"] + '_1.json', 'w+') as jsonfile:
            #     json.dump(post, jsonfile, ensure_ascii=False)

            # Post DB Check

            query = (
                "SELECT post_id FROM app_facebook_post_scraper WHERE post_id ='"
                + post["post_id"]
                + "' and group_id = '"
                + group
                + "'"
            )

            pg_conn.execute(query)

            result = pg_conn.fetchall()

            if not len(result) > 0:

                # Post DB

                columns = []
                values = []
                for key, val in post.items():
                    columns.append(key)
                    if type(val) == list:
                        val = ",".join(val).replace("'", "$#$")
                    elif val == None:
                        val = "null"
                    values.append(str(val).replace("'", "$#$"))

                query = (
                    'INSERT INTO app_facebook_post_scraper ("'
                    + '","'.join(columns)
                    + "\") VALUES ('"
                    + "','".join(values)
                    + "')"
                )

                # print(query)

                try:

                    pg_conn.execute(query)

                    pg_conn.commit()

                    print("INSERT POST SUCCESSFULLY !!!")

                except BaseException:

                    pg_conn.rollback()

                    print("ERROR !!!")
                    print(str(traceback.format_exc()))
                    print(query)

                # User DB

                query = (
                    "SELECT post_id, total_posts FROM app_facebook_user_scraper WHERE user_name ='"
                    + post_user_name
                    + "' and user_id = '"
                    + post["post_user_id"]
                    + "'"
                )

                pg_conn.execute(query)

                result = pg_conn.fetchall()

                user_db = {}

                if len(result) > 0:

                    if result[0]["post_id"] == None:
                        user_db["post_id"] = post["post_id"]
                    else:
                        user_db["post_id"] = (
                            result[0]["post_id"] + "," + post["post_id"]
                        )

                    user_db["total_posts"] = result[0]["total_posts"] + 1
                    user_db["updated_at"] = datetime.utcnow().timestamp()

                    columns = []
                    values = []
                    for key, val in user_db.items():
                        columns.append(key)
                        if type(val) == list:
                            val = ",".join(val).replace("'", "$#$")
                            print(val)
                        elif val == None:
                            val = "null"
                        values.append(str(val).replace("'", "$#$"))

                    query = (
                        'UPDATE app_facebook_user_scraper SET ("'
                        + '","'.join(columns)
                        + "\") = ('"
                        + "','".join(values)
                        + "') WHERE user_name ='"
                        + post_user_name
                        + "' and user_id = '"
                        + post["post_user_id"]
                        + "'"
                    )

                    # print(query)

                    try:

                        pg_conn.execute(query)

                        pg_conn.commit()

                        print("UPDATE USER SUCCESSFULLY !!!")

                    except BaseException:

                        pg_conn.rollback()

                        print("ERROR !!!")
                        print(str(traceback.format_exc()))
                        print(query)

                else:

                    user_db["user_name"] = post_user_name
                    user_db["post_id"] = post["post_id"]
                    user_db["total_posts"] = 1
                    user_db["total_reactions"] = 0
                    user_db["total_comments"] = 0
                    user_db["user_id"] = post["post_user_id"]
                    user_db["created_at"] = datetime.utcnow().timestamp()
                    user_db["updated_at"] = datetime.utcnow().timestamp()

                    columns = []
                    values = []
                    for key, val in user_db.items():
                        columns.append(key)
                        if type(val) == list:
                            val = ",".join(val).replace("'", "$#$")
                        elif val == None:
                            val = "null"
                        values.append(str(val).replace("'", "$#$"))

                    query = (
                        'INSERT INTO app_facebook_user_scraper ("'
                        + '","'.join(columns)
                        + "\") VALUES ('"
                        + "','".join(values)
                        + "')"
                    )

                    # print(query)

                    try:

                        pg_conn.execute(query)

                        pg_conn.commit()

                        print("INSERT USER SUCCESSFULLY !!!")

                    except BaseException:

                        pg_conn.rollback()

                        print("ERROR !!!")
                        print(str(traceback.format_exc()))
                        print(query)

            # with open( "./posts/json/post_" + post["post_id"] + '_2.json', 'w+') as jsonfile:
            #     json.dump(post_comments, jsonfile, ensure_ascii=False)

            for post_comment in post_comments:

                # print("NAME --- ", post_comment["post_user_name"])

                post_comment["post_id"] = post["post_id"]
                post_comment["created_at"] = datetime.utcnow().timestamp()
                post_comment["updated_at"] = datetime.utcnow().timestamp()

                query = (
                    "SELECT post_id FROM app_facebook_comment_scraper WHERE post_message ='"
                    + ",".join(post_comment["post_message"]).replace("'", "$#$")
                    + "' and post_comment_user_id = '"
                    + post_comment["post_comment_user_id"]
                    + "'"
                )

                pg_conn.execute(query)

                result = pg_conn.fetchall()

                if not len(result) > 0:

                    # Comment DB

                    columns = []
                    values = []

                    insert_comment = copy.deepcopy(post_comment)

                    del insert_comment["post_user_name"]

                    for key, val in insert_comment.items():
                        columns.append(key)
                        if type(val) == list:
                            val = ",".join(val).replace("'", "$#$")
                        elif val == None:
                            val = "null"
                        values.append(str(val).replace("'", "$#$"))

                    query = (
                        'INSERT INTO app_facebook_comment_scraper ("'
                        + '","'.join(columns)
                        + "\") VALUES ('"
                        + "','".join(values)
                        + "')"
                    )

                    # print(query)

                    try:

                        pg_conn.execute(query)

                        pg_conn.commit()

                        print("INSERT COMMENT SUCCESSFULLY !!!")

                    except BaseException:

                        pg_conn.rollback()

                        print("ERROR !!!")
                        print(str(traceback.format_exc()))
                        print(query)

                    # User DB

                    # print(post_comment["post_comment_user_id"])

                    query = (
                        "SELECT post_comment_id, total_comments FROM app_facebook_user_scraper WHERE user_name ='"
                        + post_comment["post_user_name"]
                        + "' and user_id = '"
                        + post_comment["post_comment_user_id"]
                        + "'"
                    )

                    pg_conn.execute(query)

                    result = pg_conn.fetchall()

                    user_db = {}

                    if len(result) > 0:

                        if result[0]["post_comment_id"] == None:
                            user_db["post_comment_id"] = post_comment["post_id"]
                        elif (
                            post_comment["post_id"] not in result[0]["post_comment_id"]
                        ):
                            user_db["post_comment_id"] = (
                                result[0]["post_comment_id"]
                                + ","
                                + post_comment["post_id"]
                            )

                        user_db["total_comments"] = result[0]["total_comments"] + 1
                        user_db["updated_at"] = datetime.utcnow().timestamp()

                        columns = []
                        values = []
                        for key, val in user_db.items():
                            columns.append(key)
                            if type(val) == list:
                                val = ",".join(val).replace("'", "$#$")
                            elif val == None:
                                val = "null"
                            values.append(str(val).replace("'", "$#$"))

                        query = (
                            'UPDATE app_facebook_user_scraper SET ("'
                            + '","'.join(columns)
                            + "\") = ('"
                            + "','".join(values)
                            + "') WHERE user_name ='"
                            + post_comment["post_user_name"]
                            + "' and user_id = '"
                            + post_comment["post_comment_user_id"]
                            + "'"
                        )

                        # print(query)

                        try:

                            pg_conn.execute(query)

                            pg_conn.commit()

                            print("UPDATE USER SUCCESSFULLY !!!")

                        except BaseException:

                            pg_conn.rollback()

                            print("ERROR !!!")
                            print(str(traceback.format_exc()))
                            print(query)

                    else:

                        user_db["user_name"] = post_comment["post_user_name"]
                        user_db["post_comment_id"] = post["post_id"]
                        user_db["total_posts"] = 0
                        user_db["total_reactions"] = 0
                        user_db["total_comments"] = 1
                        user_db["user_id"] = post_comment["post_comment_user_id"]
                        user_db["created_at"] = datetime.utcnow().timestamp()
                        user_db["updated_at"] = datetime.utcnow().timestamp()

                        columns = []
                        values = []
                        for key, val in user_db.items():
                            columns.append(key)
                            if type(val) == list:
                                val = ",".join(val).replace("'", "$#$")
                            elif val == None:
                                val = "null"
                            values.append(str(val).replace("'", "$#$"))

                        query = (
                            'INSERT INTO app_facebook_user_scraper ("'
                            + '","'.join(columns)
                            + "\") VALUES ('"
                            + "','".join(values)
                            + "')"
                        )

                        # print(query)

                        try:

                            pg_conn.execute(query)

                            pg_conn.commit()

                            print("INSERT USER SUCCESSFULLY !!!")

                        except BaseException:

                            pg_conn.rollback()

                            print("ERROR !!!")
                            print(str(traceback.format_exc()))
                            print(query)

        # break
