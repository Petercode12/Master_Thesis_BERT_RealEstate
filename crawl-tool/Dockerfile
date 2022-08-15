# FROM python:3.9

# ENV FLASK_APP run.py

# # COPY manage.py gunicorn-cfg.py requirements.txt .env ./
# # COPY app app
# # COPY authentication authentication
# # COPY core core
# # COPY configuration configuration
# COPY . .


# RUN pip3 install -r requirements.txt

# RUN python3 manage.py makemigrations

# # EXPOSE 5005
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]

# syntax=docker/dockerfile:1
FROM ubuntu:18.04

# Install machine dependencies
RUN apt update \
  && apt install -y unzip curl wget git make build-essential g++ openjdk-8-jdk 
# RUN apt update \
#   && apt-get install fonts-liberation libgbm1 libgtk-4-1 libxkbcommon0 xdg-utils

RUN apt update \
  && echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list \
  && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && apt update \
  && apt install -y google-chrome-stable
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR

RUN apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR
ENV PATH $CHROMEDRIVER_DIR:$PATH

RUN apt-get update\
    && apt-get install cron\
    && service cron start\
    && echo "PATH=/opt/someApp/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/chromedriver\n0 17 * * * DISPLAY=:0 . /code/jobs/management/commands/test.sh " | crontab -

RUN apt-get update && \
  apt-get install -y \
    libgtk2.0-0 \
    libnotify-dev \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libasound2 \
    xvfb

RUN apt install -y python3.8 python3-pip python3-setuptools


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt requirements.txt
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install virtualenv
RUN virtualenv /opt/env
RUN . /opt/env/bin/activate && python3.8 -m pip install -r requirements.txt
COPY . .
RUN . /opt/env/bin/activate && python3.8 manage.py makemigrations

CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
