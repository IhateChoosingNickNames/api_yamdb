# Проект "YaMDb"

### Описание:
Проект YaMDb собирает отзывы пользователей на произведения.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone ххх
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
Когда вы запустите проект, по адресу http://127.0.0.1:8000/redoc/ будет доступна документация для api_yamdb.
Документация представлена в формате Redoc.

### Стэк технологий:
    Django,
    Django Rest Framework (DRF)
