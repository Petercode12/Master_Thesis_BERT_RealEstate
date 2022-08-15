# =========================================================================
#  Title:  Extract neede features through xpath from posts html files that
#  Author: Huỳnh Ngọc Thiện
#  Date:   Jan 9 2021
# =========================================================================

from scrapy.utils.project import get_project_settings
from enum import Enum
from datetime import datetime, timedelta

import lxml.html
import json
import os
import time
import traceback
import logging
import psycopg2
import psycopg2.extras
from datetime import datetime

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

# Reactions

from enum import Enum


class Reaction(Enum):
    LIKE = 0
    LOVE = 1
    HUG = 2
    LAUGH = 3
    WOW = 4
    SAD = 5
    ANGRY = 6


# Icon class in Facebook

reaction_dict = {
    "_59aq img sp_Vpco9KTVY4D sx_a46c85": "LIKE",
    "_59aq img sp_Vpco9KTVY4D sx_c78bb2": "LOVE",
    "_59aq img sp_Vpco9KTVY4D sx_3451d3": "HUG",
    "_59aq img sp_Vpco9KTVY4D sx_b837fa": "LAUGH",
    "_59aq img sp_Vpco9KTVY4D sx_582354": "WOW",
    "_59aq img sp_Vpco9KTVY4D sx_012864": "SAD",
    "_59aq img sp_Vpco9KTVY4D sx_5ed83a": "ANGRY",
}

# LIKE = "_59aq img sp_Vpco9KTVY4D sx_a46c85"
# LOVE = "_59aq img sp_Vpco9KTVY4D sx_c78bb2"
# HUG = "_59aq img sp_Vpco9KTVY4D sx_3451d3"
# LAUGH = "_59aq img sp_Vpco9KTVY4D sx_b837fa"
# WOW = "_59aq img sp_Vpco9KTVY4D sx_582354"
# SAD = "_59aq img sp_Vpco9KTVY4D sx_012864"
# ANGRY = "_59aq img sp_Vpco9KTVY4D sx_5ed83a"

# This will setup settings variable to get constant from settings.py such as SCROLLS (scrolling number)

settings = get_project_settings()

# Get groups list

with open("./groups/groups_facebook_1.txt", "r") as f:
    groups = str(f.read()).split(",")

# Now we will go through group lists to get group IDs, then loop through them to access to posts list json and from there, we will get each post ID to access their own html file to extract xpath like the following codes

for url in groups:

    group = str(url.split("/")[-1])

    with open("./groups/json/group_posts_" + group + ".json", "r") as jsonfile:
        posts = json.load(jsonfile)

    for post in posts:

        # Check if post was crawled and stored into html file or not

        the_file = (
            "./groups/reaction/reaction_html_" + group + "_" + post["post"] + ".html"
        )

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

            now = datetime.utcnow().timestamp

            # Start extracting informaiton

            users = htmls.xpath("//div[contains(@class,'_1uja')]")

            print("users --- ", users)

            for user in users:

                print("user --- ", user)

                reaction_db = {}
                user_db = {}

                user_link = user.xpath(".//a/@href")[0]

                # if "facebook" not in str(user_link):
                #     user_link = "https://facebook.com" + user_link

                user_id = user_link.split("?")[0].split("/")[-1]

                print("link --- ", user_link)
                print("id --- ", user_id)

                user_name = user.xpath(".//text()")[0]

                print("name --- ", user_name)

                user_reaction = user.xpath("./i/@class")[0]

                print("reaction --- ", user_reaction)

                user_reaction_id = Reaction[reaction_dict[user_reaction]].value

                print("reaction id --- ", user_reaction_id)

                # Reaction DB Check

                query = (
                    "SELECT post_id FROM app_facebook_reaction_scraper WHERE post_id ='"
                    + post["post"]
                    + "' and post_user_id = '"
                    + user_id
                    + "'"
                )

                pg_conn.execute(query)

                result = pg_conn.fetchall()

                if len(result) > 0:
                    continue

                # Reaction DB

                reaction_db["post_id"] = post["post"]
                reaction_db["post_user_id"] = user_id
                reaction_db["like_reaction"] = user_reaction_id
                reaction_db["created_at"] = datetime.utcnow().timestamp()
                reaction_db["updated_at"] = datetime.utcnow().timestamp()

                columns = []
                values = []
                for key, val in reaction_db.items():
                    columns.append(key)
                    values.append(str(val))

                query = (
                    'INSERT INTO app_facebook_reaction_scraper ("'
                    + '","'.join(columns)
                    + "\") VALUES ('"
                    + "','".join(values)
                    + "')"
                )

                # print(query)

                print("INSERT SUCCESSFULLY !!!")

                pg_conn.execute(query)

                pg_conn.commit()

                # User DB

                query = (
                    "SELECT post_reaction_id, total_reactions FROM app_facebook_user_scraper WHERE user_name ='"
                    + user_name
                    + "' and user_id = '"
                    + user_id
                    + "'"
                )

                pg_conn.execute(query)

                result = pg_conn.fetchall()

                if len(result) > 0:

                    if result[0]["post_reaction_id"] == None:
                        user_db["post_reaction_id"] = post["post"]
                    else:
                        user_db["post_reaction_id"] = (
                            result[0]["post_reaction_id"] + "," + post["post"]
                        )

                    user_db["total_reactions"] = result[0]["total_reactions"] + 1
                    user_db["updated_at"] = datetime.utcnow().timestamp()

                    columns = []
                    values = []
                    for key, val in user_db.items():
                        columns.append(key)
                        values.append(str(val))

                    query = (
                        'UPDATE app_facebook_user_scraper SET ("'
                        + '","'.join(columns)
                        + "\") = ('"
                        + "','".join(values)
                        + "') WHERE user_name ='"
                        + user_name
                        + "' and user_id = '"
                        + user_id
                        + "'"
                    )

                    # print(query)
                    print("UPDATE SUCCESSFULLY !!!")

                    pg_conn.execute(query)

                    pg_conn.commit()

                else:

                    user_db["user_name"] = user_name
                    user_db["post_reaction_id"] = post["post"]
                    user_db["total_posts"] = 0
                    user_db["total_reactions"] = 1
                    user_db["total_comments"] = 0
                    user_db["user_id"] = user_id
                    user_db["created_at"] = datetime.utcnow().timestamp()
                    user_db["updated_at"] = datetime.utcnow().timestamp()

                    columns = []
                    values = []
                    for key, val in user_db.items():
                        columns.append(key)
                        values.append(str(val))

                    query = (
                        'INSERT INTO app_facebook_user_scraper ("'
                        + '","'.join(columns)
                        + "\") VALUES ('"
                        + "','".join(values)
                        + "')"
                    )

                    # print(query)
                    print("INSERT SUCCESSFULLY !!!")

                    pg_conn.execute(query)

                    pg_conn.commit()

                # break

        # break
