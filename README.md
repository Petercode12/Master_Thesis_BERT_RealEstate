## To run React for Front-end

```bash
$ # Open terminal
$ cd web-app/react-front/my-app
$ npm install [<lacking packages> ...]
$ npm start
```
<br />

### 👉 Set Up for `Unix`, `MacOS`

> Install modules via `VENV`

```bash
$ virtualenv env
$ source env/Scripts/activate
$ pip3 install -r requirements.txt
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

### 👉 Set Up for `Windows`

> Install modules via `VENV` (windows)

```
$ cd web-app
$ virtualenv env
$ source env/Scripts/activate
$ pip install -r requirements.txt
$ python -m pip install django-cors-headers
$ pip install psycopg2
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
