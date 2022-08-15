# How to run local this repos

* Note: You must use Linux or WSL to run.

## Install Database
- Postgres
- MongoDB

## Install Dependencies

```
 pip3 install -r requirements.txt
```
## Set up file config corresponding to your database setting
- Folder configurations

## Running Django
- python3 manage.py makemigrations
- python3 manage.py migrate
- python3 manage.py createsuperuser (for the first time)
- python3 manage.py runserver

## Running crontab 
- First, go to the main docker container then execuce
```
  docker exec -it {docker_id} bash
```
- Second, update apt and install some necessary libraries for the kernel
```
  apt-get update
  apt-get install cron
  apt-get install vim
  service cron start
```
- Third, setting crontab like this (mandatory)

```
PATH=/opt/someApp/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

* * * * * sh /code/jobs/management/commands/shell_vieclam.sh 
```
Notes: * * * * * can changed depening on our purpose.


- Last but not least, you can change crontab in shell_vieclam.sh



Enjoy
