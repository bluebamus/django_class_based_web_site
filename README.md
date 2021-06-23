# django_function_based_web_site

This site made for understanding how to use django functional programing.

# How to use

## export mode

Development mode

1. enter command "export DJANGO_SETTINGS_MODULE=django_basic.settings.dev"
2. python manage.py makemigrations
3. python manage.py migrate
4. python manage.py runserver 0.0.0.0:8000

Product mode

1. enter command "export DJANGO_SETTINGS_MODULE=django_basic.settings.prod"
2. python manage.py makemigrations
3. python manage.py migrate
4. python manage.py runserver 0.0.0.0:8000

## modify manage.py and wsgi.py mode

> manage.py and wsgi.py update like bellow

Development mode

- os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_basic.settings.dev')

Product mode

- os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_basic.settings.prod')

# What kind of any guide examples for Django?

1. Make a view only using FBV.
2. Using manytomanyfiled. There is only "related_name" option example and no "throught" option example in this app.
3. "form" and "modelform" are used differently. you can understand both cases in the board's forms.py.
4. Manytomanyfield is of type "select" in modelform. So if you want it as input type, you need to override it with "**init**" function. And the "required" option is the same.
5. When developing the actual service, we do not delete data from the database Use the state delete tag to handle it. Shows how easy it is to model a board using the model from the Inheritance of helpers app.
6. This project handles logins, writes, updates, deletes, replies, session handling, tags, likes, thumbnails, file uploads and more.
7. Developers can create environments for tests, products, AWS deployments, etc. with separate "config" files and "env" files.

- This project doesn't use django's "user" model. Using Custom model.
