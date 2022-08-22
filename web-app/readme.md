## To run React for Front-end

```bash
$ # Open terminal
$ cd react-front/my-app
$ npm install [<lacking packages> ...]
$ npm start
```

> Features

- `Up-to-date dependencies`
- Database: `sqlite`
- UI-Ready app, Django Native ORM
- `Session-Based authentication`, Forms validation

<br />

<br />
## ✨ Start the app in Docker

> **Step 1** - Download the code from the GH repository (using `GIT`)

```bash
$ # Get the code
$ git clone https://github.com/app-generator/django-volt-dashboard.git
$ cd django-volt-dashboard
```

<br />

> **Step 2** - Edit `.env` and remove or comment all `DB_*` settings (`DB_ENGINE=...`). This will activate the `SQLite` persistance.

```txt
DEBUG=True

# Deployment SERVER address
SERVER=.appseed.us

# For MySql Persistence
# DB_ENGINE=mysql            <-- REMOVE or comment for Docker
# DB_NAME=appseed_db         <-- REMOVE or comment for Docker
# DB_HOST=localhost          <-- REMOVE or comment for Docker
# DB_PORT=3306               <-- REMOVE or comment for Docker
# DB_USERNAME=appseed_db_usr <-- REMOVE or comment for Docker
# DB_PASS=<STRONG_PASS>      <-- REMOVE or comment for Docker

```

<br />

> **Step 3** - Start the APP in `Docker`

```bash
$ docker-compose up --build
```

Visit `http://localhost:85` in your browser. The app should be up & running.

<br />

## ✨ How to use it

> Download the code

```bash
$ # Get the code
$ git clone https://github.com/app-generator/django-volt-dashboard.git
$ cd django-volt-dashboard
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
$ virtualenv env
$ source env/Scripts/activate
$ pip3 install -r requirements.txt
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
