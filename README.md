## To run React for Front-end

```bash
$ # Open terminal
$ cd web-app/react-front/my-app
$ npm install [<lacking packages> ...]
$ npm start
```

<br />

## Database settings

```txt
DEBUG=True

# Deployment SERVER address
SERVER=.appseed.us

# For MySql Persistence
# DB_ENGINE=mysql            
# DB_NAME=appseed_db         
# DB_HOST=localhost          
# DB_PORT=3306               
# DB_USERNAME=appseed_db_usr 
# DB_PASS=<STRONG_PASS>      

```

<br />

### 👉 Set Up for `Windows`

> Install modules via `VENV` (windows)

```
$ cd web-app
$ virtualenv env
$ source env/Scripts/activate
$ pip install -r requirements.txt
```

<br />

> Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> Start the app

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`.

<br />
