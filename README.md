# YamDb

Description: API for YamDb

Used technologies:
-
    - python 3.7.9
    - django 2.2.16
    - djangorestframework 3.12.4
    - simplejwt 4.7.2
    - django-filters 21.1
    - sqlite3

Features:
-
    - Authorization via email adress
    - Diffrent roles for users: common user, modertor, admin
    - Manage users and content
    - Cusomize your profile
    - Create reviews for titles
    - Rate titles
    - Comment reviews


Instructions: 
1. Install requirements:
    # pip install -r requirements.txt
2. Go to ../api_yamdb/ migrate:
    # python manage.py migrate
3. Fill the DB with prepared CSV-files:
    # python manage.py fill_db
4. Runserver:
    # python manage.py runserver
After that site is available at your localhost url (most common case: http://127.0.0.1:8000/)

Examples of endpoints:
-
    - GET http://127.0.0.1:8000/api/v1/titles/{title_id}/
    - POST http://127.0.0.1:8000/api/v1/titles/
    - DELETE http://127.0.0.1:8000/api/v1/posts/1/
    - PUT http://127.0.0.1:8000/api/v1/posts/1/

Examples of responses:
-
- GET title:
{
"id": 0,
"name": "string",
"year": 0,
"rating": 0,
"description": "string",
"genre": [
{
"name": "string",
"slug": "string"
}
],
"category": {
"name": "string",
"slug": "string"
}
}
- POST title:
{
"name": "string",
"year": 0,
"description": "string",
"genre": [
"string"
],
"category": "string"
}

All available endpoints and responses you can find in documentation:

    # http://127.0.0.1:8000/redoc (or your own localhost url)
