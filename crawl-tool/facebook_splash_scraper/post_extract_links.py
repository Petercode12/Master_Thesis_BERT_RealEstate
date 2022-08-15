from bs4 import BeautifulSoup
from datetime import datetime

import sys
import time
import json


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


# Get groups list

with open("./groups/groups_facebook_1.txt", "r") as f:
    groups = str(f.read()).split(",")

for url in groups:

    group = str(url.split("/")[-1])

    with open("./groups/html/group_html_" + group + ".html", "r") as f:
        contents = f.read()

        soup = BeautifulSoup(contents, "lxml")

        links = soup.find_all("div", {"class": "_52jc _5qc4 _78cz _24u0 _9s6"})

        output_links = []

        for link_xpath in links:

            tag_a = link_xpath.find("a", recursive=False)

            link = tag_a["href"]

            if link == "#":
                break

            if "permalink" not in str(link):
                link = "https://facebook.com" + link.split("&refid")[0]

                post = str(link.split("&id=")[-1])

            else:

                link = link.split("/?")[0]

                post = str(link.split("/")[-1])

            times = tag_a.findAll(text=True, recursive=True)[0]

            times = _convert_to_timestamp(times)

            result = {"post": post, "link": link.replace("m.", ""), "timestamp": times}

            output_links.append(result)

            # break

        with open("./groups/json/group_posts_" + group + ".json", "w+") as jsonfile:
            json.dump(output_links, jsonfile, ensure_ascii=False)
