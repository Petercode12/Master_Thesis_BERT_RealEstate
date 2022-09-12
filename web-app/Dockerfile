#### 1. Get Linux
# FROM ubuntu:18.04

# ### 2. Get Java via the package manager
# RUN apt update \
#   && apt install -y unzip curl wget git make build-essential g++ openjdk-8-jdk 

# ### 3. Get Python, PIP

# RUN apt install -y python3.8 python3-pip python3-setuptools \
# && python3.8 -m ensurepip \
# && pip3 install --upgrade pip setuptools \
# if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
# if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
# rm -r /root/.cache

# ### Get Flask for the app
# RUN pip install --trusted-host pypi.python.org flask

# ####
# #### OPTIONAL : 4. SET JAVA_HOME environment variable, uncomment the line below if you need it

# #ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk"


# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# WORKDIR /code
# COPY requirements.txt .
# RUN pip3 install --upgrade pip
# RUN pip3 install -r requirements.txt

# #pip
# # RUN python3.8 -m pip install --upgrade pip

# # RUN python3.8 -m pip install --upgrade setuptools
# # RUN python3.8 -m pip install ez_setup

# # RUN python3.8 -m pip install virtualenv
# # RUN virtualenv /opt/env
# # RUN . /opt/env/bin/activate && python3.8 -m pip install -r requirements.txt


# COPY . .
# RUN python3.8 manage.py migrate
# # RUN python3.8 -m pip install virtualenv
# # RUN virtualenv /opt/env
# # RUN . /opt/env/bin/activate && python3.8 -m pip install -r requirements.txt
# # COPY . .
# # RUN . /opt/env/bin/activate && python3.8 manage.py migrate

# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]



#FROM openjdk:slim
FROM python:3.9
COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8

ENV JAVA_HOME /usr/local/openjdk-8

RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# running migrations
RUN python manage.py migrate

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]





#/// org
# FROM python:3.9

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# COPY requirements.txt .
# # install python dependencies
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# # running migrations
# RUN python manage.py migrate

# # gunicorn
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]

