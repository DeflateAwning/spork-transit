# Spork Transit

## Motivation

My biggest goals are:
1. fix the fucked up time estimations bc buses "vanish" periodically
2. show every single possible route anytime you're trying to navigate, and let the user decide based on as much data as possible which one they wanna take
    * to evaluate stops for errands and things, for example
    * because people can run/walk fast if they're late
3. Push notifications of service changes, with text diffs of services messages.

First tasks:
* Create a map with easy selection of up to 10 routes, which shows all buses live and with a historical time slider.
* Create a table with easy selection of routes, which shows ETAs (based on schedule, updates, and positions/schedule)
* Create a route-finding algo, esp. for train-to-train transfers
* Have an easy way to lookup the bus number of any bus, for cases where you've lost property on a bus (lost-and-found)

Other goals:
* Optimize routes reliably by earliest arrival time.
* Optimize routes by metrics like "longest time sheltered" if it's raining
* Show the temperature in the app
* Voice alerts of where a bus is, for if you're running for a bus/need to leave soon/running for a bus
* Provide standardized tips, like "X with arms to signal that you don't want to board", or "waive if you want to board"

Low-priority goals:
* Make a stats page
    * Total Routes
    * Number of Active Buses at any point


## Features

### Back-end

* User Management
    * Registration
    * Login
    * Session Management
    * Password Recovery
    * Roles
* Database Support
    * MySQL
    * SQLite
    * MongoDB (incomplete)
* Mail
* Migrations (Powered by `Flask-Migrate`)
* Deployment
    * Support for Git-powered release on on `PythonAnywhere`

### Front-end

* `Bootstrap`-powered clean front-end
* Elegant themes powered by https://bootswatch.com/
* Ability to change themes on the fly
* Sample Front-end Components (TODO)

## Requirements

* For package requirements, check `requirements.txt`
* Mail functionality requires SMTP access.
* For `PythonAnywhere` deployment, an account on https://www.pythonanywhere.com/ is required.
    * `PythonAnywhere` free accounts do not support non-HTTP(S) ports, this results in
       `MongoDB`, `
* MySQL access required if MySQL is used as backend server.

## Setup

Getting started with the basic application is straightforward.

* Install the requirements from the `requirements.txt`,

```bash
$ pip3 install -r requirements.txt
```

* Copy `settings.sample.py` to `settings.py` and update it as required.

Most of the settings can also be specified through environment variables.
There are inline explanations in the settings file if the variables are not self-explanatory.

## Run

Run the application using,

````bash
$ python server.py
````

OR

```bash
$ export FLASK_APP="server:webapp"
$ export FLASK_DEBUG=1
$ flask run
```

```ps1
$env:FLASK_APP = 'server:webapp';
$env:FLASK_DEBUG = '1';
flask run
```

(Other WSGI-based deployments are also possible. e.g. `gunicorn`)

### Database Support

By default, SQLite3 database will be used. To use MySQL, update credentials
either through `settings.py` or through environment variables.
In `settings.py`, set `USE_SQLITE` to `False` and `USE_MYSQL` to `True`.

Support for PostgreSQL, although not explicitly added, is easy to figure out.
It can be achieved in a similar manner to MySQL support by installing the necessary driver
and using the proper `database_uri` for `SQLAlchemy`.

MongoDB support may be added in the future, although it's not too difficult to figure it out.

### Mail

If SMTP credentials are added, mail support will be enabled. This would enable password recovery
by receiving a link for password reset, as well as a welcome mail after registration.

Contents of these emails can be modified by editing templates in `tempaltes/security/email`

### PythonAnywhere Support

* Create a free account on https://www.pythonanywhere.com/
* Generate a token
* Clone your repository on the server
* Set-up your application by setting propery WSGI paths
* Once your application is running, for future updates, you can use "Update" and "Reload" buttons from `Admin` tab to update your application.
* For `PythonAnywhere` free accounts, only SMTP permitted is `smtp.gmail.com`.

## Contribute

Aim of this project is to provide a basic skeleton for development of simple, beautiful and functional web applications.

Feel free to contribute towards that end by,

* Providing new features
* Improving current features
* Improving code quality
* Adding documentation

## License

GNU GPL v3
